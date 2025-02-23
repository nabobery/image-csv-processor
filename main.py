import uvicorn
from app.main import app
from app.core.logger import logger


if __name__ == "__main__":
    logger.info("Starting the application")
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)