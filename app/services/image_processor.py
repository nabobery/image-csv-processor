import aiohttp
from PIL import Image
import io
from app.db.mongodb import get_collection
from app.db.models import ProcessingStatus
from app.services.webhook_handler import send_webhook_notification
from app.core.logger import logger
import traceback
from app.core.config import get_settings
import csv

settings = get_settings()

async def upload_to_imgur(image_data: bytes, title: str = "Simple upload", description: str = "This is a simple image upload in Imgur") -> str:
    headers = {
        'Authorization': f"Client-ID {settings.imgur_client_id}"
    }
    try:
        # Convert to JPEG if needed
        image = Image.open(io.BytesIO(image_data))
        if image.format != 'JPEG':
            output = io.BytesIO()
            image = image.convert('RGB')
            image.save(output, format='JPEG', quality=85)
            image_data = output.getvalue()

        async with aiohttp.ClientSession() as session:
            form_data = aiohttp.FormData()
            form_data.add_field('image', image_data, content_type='image/jpeg')
            form_data.add_field('type', 'image')
            form_data.add_field('title', title)
            form_data.add_field('description', description)
            
            async with session.post(
                'https://api.imgur.com/3/image',
                headers=headers,
                data=form_data
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return data['data']['link']
                raise Exception(f"Failed to upload image to Imgur: {response.status}")
    except Exception as e:
        logger.error(f"Error uploading to Imgur: {str(e)}\n{traceback.format_exc()}")
        raise

async def download_image(url: str) -> bytes:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.read()
    except Exception as e:
        logger.error(f"Error downloading image from {url}: {str(e)}\n{traceback.format_exc()}")
        raise

async def compress_image(image_data: bytes) -> bytes:
    try:
        image = Image.open(io.BytesIO(image_data))
        output = io.BytesIO()
        image.save(output, format=image.format, quality=50)
        return output.getvalue()
    except Exception as e:
        logger.error(f"Error compressing image: {str(e)}\n{traceback.format_exc()}")
        raise

async def process_images(request_id: str):
    collection = get_collection("requests")
    request = await collection.find_one({"request_id": request_id})
    
    try:
        # Update status to processing
        await collection.update_one(
            {"request_id": request_id},
            {"$set": {"status": ProcessingStatus.PROCESSING}}
        )
        logger.info(f"Started processing images for request: {request_id}")

        output_data = []  # Prepare to collect output data for CSV

        for product in request["products"]:
            output_urls = []
            for url in product["input_urls"]:
                try:
                    image_data = await download_image(url)
                    compressed_data = await compress_image(image_data)
                    output_url = await upload_to_imgur(compressed_data)
                    output_urls.append(output_url)
                except Exception as e:
                    logger.error(f"Error processing image {url}: {str(e)}\n{traceback.format_exc()}")
                    continue
            
            # Update product with output URLs
            await collection.update_one(
                {"request_id": request_id, "products.serial_number": product["serial_number"]},
                {
                    "$set": {
                        "products.$.output_urls": output_urls,
                        "products.$.processing_status": ProcessingStatus.COMPLETED
                    }
                }
            )

            # Collect data for CSV
            output_data.append({
                "S. No.": product["serial_number"],
                "Product Name": product["product_name"],
                "Input Image Urls": ", ".join(product["input_urls"]),
                "Output Image Urls": ", ".join(output_urls)
            })
        
        # Generate CSV data
        output_csv = io.StringIO()
        writer = csv.DictWriter(output_csv, fieldnames=["S. No.", "Product Name", "Input Image Urls", "Output Image Urls"])
        writer.writeheader()
        writer.writerows(output_data)
        
        # Store CSV data in the ProcessingRequest
        csv_string = output_csv.getvalue()
        await collection.update_one(
            {"request_id": request_id},
            {"$set": {"csv_data": csv_string, "status": ProcessingStatus.COMPLETED}}
        )

        logger.info(f"Completed processing images for request: {request_id}")
        
        # Send webhook notification
        # await send_webhook_notification(request_id)
        
    except Exception as e:
        logger.error(f"Error processing images for request {request_id}: {str(e)}\n{traceback.format_exc()}")
        await collection.update_one(
            {"request_id": request_id},
            {"$set": {"status": ProcessingStatus.FAILED}}
        )
        raise