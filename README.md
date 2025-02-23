# Image Processing System

A scalable system for processing image data from CSV files using FastAPI and MongoDB.

## Features

- Asynchronous CSV file processing
- Image compression and optimization (50% quality reduction)
- Status tracking with unique request IDs
- Webhook notifications for process completion
- RESTful API endpoints

## System Architecture

```ascii
+----------------+      +-----------------+      +------------------+
|    Client      | ---> | FastAPI Server  | ---> |     MongoDB      |
+----------------+      +-----------------+      +------------------+
        |                        |
        |                        v
        |             +------------------+
        |             |  Image Processor  |
        |             +------------------+
        |                        |
        |                        v
        |             +------------------+
        |             |  Webhook Notifier |
        |             +------------------+
```

## Project Structure

```ascii
image_processing/
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes/
│   │   │   ├── upload.py
│   │   │   ├── status.py
│   │   │   └── webhook.py
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   │   └── logger.py
│   ├── db/
│   │   ├── mongodb.py
│   │   └── models.py
│   ├── services/
│   │   ├── csv_processor.py
│   │   ├── image_processor.py
│   │   └── webhook_handler.py
│   ├── schemas/
│   │   ├── request.py
│   │   └── response.py
├── tests/
├── .env
├── requirements.txt
└── main.py
```

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/nabobery/image-csv-processor
cd image-csv-processor
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\\Scripts\\activate  # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

```bash
cp .env.example .env
```

Edit the `.env` file with your MongoDB URI, database name, API key, webhook secret, and image storage path.

```env
MONGODB_URI=mongodb://localhost:27017
DATABASE_NAME=image_processing
IMGUR_CLIENT_ID=imgur_client_id
API_KEY=your_api_key
WEBHOOK_SECRET=your_webhook_secret
IMAGE_STORAGE_PATH=/path/to/storage
```

### 5. Run the Application

```bash
uvicorn app.main:app --reload
```

The server will start at `http://127.0.0.1:8000`.

## API Endpoints

### 1. Upload CSV File

Upload a CSV file containing image URLs for processing.

- **Endpoint:** `POST /api/v1/upload`
- **Content-Type:** `multipart/form-data`

```http
POST /api/v1/upload
Content-Type: multipart/form-data
file: @your_file.csv
```

Example CSV (`your_file.csv`):

```csv
product_name,image_url
product1,http://example.com/image1.jpg
product2,http://example.com/image2.png
```

- **Request Body:**

```json
{
  "request_id": "uuid-string",
  "message": "Processing started"
}
```

- **Response:**

```json
{
  "request_id": "uuid-string",
  "status": "received"
}
```

### 2. Get Processing Status

Check the status of a processing request using the request ID.

- **Endpoint:** `GET /api/v1/status/{request_id}`

```http
GET /api/v1/status/uuid-string
```

- **Response:**

```json
{
  "request_id": "uuid-string",
  "status": "processing|completed|failed",
  "products": [
    {
      "serial_number": 1,
      "product_name": "SKU1",
      "input_urls": ["url1", "url2"],
      "output_urls": ["processed-url1", "processed-url2"],
      "processing_status": "completed"
    }
  ]
}
```

### 3. Configure Webhook

Configure a webhook URL to receive notifications on specific events.

- **Endpoint:** `POST /api/v1/webhook/configure`
- **Content-Type:** `application/json`

```http
POST /api/v1/webhook/configure
Content-Type: application/json
```

- **Request Body:**

```json
{
  "webhook_url": "https://your-webhook-url.com",
  "events": ["processing.completed"]
}
```

- **Response:**

```json
{
  "message": "Webhook configured successfully"
}
```

## Error Handling

The API returns standard HTTP status codes for errors:

- 400: Bad Request (e.g., invalid input)
- 404: Not Found (e.g., request ID not found)
- 500: Internal Server Error (e.g., database connection error)

Example error response:

```json
{
  "detail": "Request ID not found"
}
```

## Advanced Configuration

### Environment Variables

- `MONGODB_URI`: MongoDB connection string.
- `DATABASE_NAME`: Name of the MongoDB database.
- `IMGUR_CLIENT_ID`: Client id for uploading images to imgur
- `API_KEY`: API key for authentication.
- `WEBHOOK_SECRET`: Secret key for verifying webhook signatures.
- `IMAGE_STORAGE_PATH`: Local path for storing processed images.

### Webhooks

The system supports webhook notifications for the following events:

- `processing.started`: When image processing starts.
- `processing.completed`: When image processing completes.
- `processing.failed`: When image processing fails.

## Contributing

Contributions are welcome! Please submit a pull request with your changes.

## License

[MIT](LICENSE)
