import logging
import sys

def get_logger(name: str = "app_logger") -> logging.Logger:
    level = logging.INFO

    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:  # Avoid duplicate handlers
        # Stream Handler (STDOUT)
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setLevel(level)

        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
        )
        stream_handler.setFormatter(formatter)

        logger.addHandler(stream_handler)

    return logger


logger = get_logger()
