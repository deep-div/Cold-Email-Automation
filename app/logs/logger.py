import logging
from logging.handlers import RotatingFileHandler

def get_logger(name: str = "app_logger") -> logging.Logger:
    level= logging.DEBUG
    
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:  # Avoid duplicate handlers
        # File Handler (Rotating)
        file_handler = RotatingFileHandler(
            "app/logs/app.log",
            maxBytes=5 * 1024 * 1024,  # 5MB
            backupCount=2
        )
        file_handler.setLevel(level)

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)

        # Disable propagation to avoid root logger printing to console
        logger.propagate = False

    return logger

logger = get_logger()
