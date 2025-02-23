import logging

class SingletonMeta(type):
    """Singleton metaclass to ensure only one instance of the logger exists."""
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Logger(metaclass=SingletonMeta):
    def __init__(self):
        self.logger = logging.getLogger("image_csv_processor")
        self.logger.setLevel(logging.DEBUG)  # Set the logging level
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def get_logger(self):
        return self.logger

# Initialize the singleton logger instance
logger = Logger().get_logger()