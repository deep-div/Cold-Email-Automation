import logging
from logging.handlers import RotatingFileHandler
import os
import json
from datetime import datetime

# ----------------------------
# Configuration
# ----------------------------
LOG_DIR = "app/logs"  # Change path for Windows if needed
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE_INFO = os.path.join(LOG_DIR, "app_info.log")
LOG_FILE_ERROR = os.path.join(LOG_DIR, "app_error.log")

MAX_BYTES = 10 * 1024 * 1024  # 10 MB
BACKUP_COUNT = 7               # Keep last 7 files

# ----------------------------
# JSON Formatter
# ----------------------------
class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "correlation_id": getattr(record, "correlation_id", None),
            "exception": getattr(record, "exception", None)
        }
        return json.dumps(log_record)

# ----------------------------
# Log Filters
# ----------------------------
class InfoFilter(logging.Filter):
    def filter(self, record):
        return record.levelno == logging.INFO

class ErrorFilter(logging.Filter):
    def filter(self, record):
        return record.levelno >= logging.WARNING  # WARNING, ERROR, CRITICAL

# ----------------------------
# Logger setup
# ----------------------------
logger = logging.getLogger("app_logger")
logger.setLevel(logging.INFO)

if not logger.handlers:
    # INFO handler: only INFO messages
    info_handler = RotatingFileHandler(
        LOG_FILE_INFO, maxBytes=MAX_BYTES, backupCount=BACKUP_COUNT, encoding="utf-8"
    )
    info_handler.setFormatter(JsonFormatter())
    info_handler.addFilter(InfoFilter())
    logger.addHandler(info_handler)

    # ERROR handler: WARNING + ERROR + CRITICAL
    error_handler = RotatingFileHandler(
        LOG_FILE_ERROR, maxBytes=MAX_BYTES, backupCount=BACKUP_COUNT, encoding="utf-8"
    )
    error_handler.setFormatter(JsonFormatter())
    error_handler.addFilter(ErrorFilter())
    logger.addHandler(error_handler)


