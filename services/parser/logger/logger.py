import os
import logging
from logging.handlers import RotatingFileHandler

class CustomFormatter(logging.Formatter):
    def format(self, record):
        s = super().format(record)
        # List of internal LogRecord attributes that we don't want to include
        internal_attributes = ['message', 'asctime', 'msecs', 'created', 'relativeCreated', 'exc_info',
                               'exc_text', 'args', 'filename', 'funcName', 'levelname', 'levelno',
                               'lineno', 'module', 'pathname', 'process', 'processName',
                               'stack_info', 'thread', 'threadName', 'name', 'exc_text', 'msg', 'taskName']
        extras = []
        for key, value in record.__dict__.items():
            if key not in internal_attributes:
                extras.append(f'\n\t{key}: {value}')
        if extras:
            s += ''.join(extras)
        return s


def setup_logger():
    logs_dir = 'logs'
    os.makedirs(logs_dir, exist_ok=True)

    # Set up logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # Set up console handler
    console_handler = logging.StreamHandler()
    console_format = CustomFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')  # Added `%(asctime)s`
    console_handler.setFormatter(console_format)
    console_handler.setLevel(logging.INFO)

    # Set up file handler
    log_file_path = os.path.join(logs_dir, 'app.log')  # Path to the log file
    file_handler = RotatingFileHandler(log_file_path, maxBytes=1024 * 1024, backupCount=5)
    file_format = CustomFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_format)
    file_handler.setLevel(logging.DEBUG)

    # Add handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
