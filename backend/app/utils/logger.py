"""
Logging configuration for ZeeMovies application
"""
import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler

# Create logs directory if it doesn't exist
LOGS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'logs')
os.makedirs(LOGS_DIR, exist_ok=True)

# Log file paths
API_LOG_FILE = os.path.join(LOGS_DIR, 'api.log')
ERROR_LOG_FILE = os.path.join(LOGS_DIR, 'error.log')
ACCESS_LOG_FILE = os.path.join(LOGS_DIR, 'access.log')

# Logging format
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

def setup_logger(name, log_file, level=logging.INFO):
    """
    Set up a logger with file and console handlers
    """
    formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
    
    # File handler with rotation (10MB max, keep 5 backups)
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    file_handler.setFormatter(formatter)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

# Create loggers
api_logger = setup_logger('api', API_LOG_FILE)
error_logger = setup_logger('error', ERROR_LOG_FILE, logging.ERROR)
access_logger = setup_logger('access', ACCESS_LOG_FILE)

def log_request(endpoint, method, status_code, response_time):
    """Log API request details"""
    access_logger.info(
        f"{method} {endpoint} - Status: {status_code} - Time: {response_time:.3f}s"
    )

def log_error(error_type, error_message, traceback_info=None):
    """Log error details"""
    error_logger.error(f"{error_type}: {error_message}")
    if traceback_info:
        error_logger.error(f"Traceback: {traceback_info}")

def log_startup():
    """Log application startup"""
    api_logger.info("=" * 80)
    api_logger.info(f"ZeeMovies API Server Starting - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    api_logger.info("=" * 80)

def log_shutdown():
    """Log application shutdown"""
    api_logger.info("=" * 80)
    api_logger.info(f"ZeeMovies API Server Shutting Down - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    api_logger.info("=" * 80)
