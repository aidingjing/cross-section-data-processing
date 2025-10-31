import logging
import os
from typing import Optional
from datetime import datetime


class LoggerUtil:
    _loggers = {}
    
    @staticmethod
    def setup_logger(
        name: str,
        log_file: Optional[str] = None,
        level: int = logging.INFO,
        log_format: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ) -> logging.Logger:
        if name in LoggerUtil._loggers:
            return LoggerUtil._loggers[name]
        
        logger = logging.getLogger(name)
        logger.setLevel(level)
        
        formatter = logging.Formatter(log_format)
        
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        if log_file:
            os.makedirs(os.path.dirname(log_file), exist_ok=True)
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(level)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        
        LoggerUtil._loggers[name] = logger
        return logger
    
    @staticmethod
    def get_logger(name: str) -> logging.Logger:
        if name not in LoggerUtil._loggers:
            return LoggerUtil.setup_logger(name)
        return LoggerUtil._loggers[name]
    
    @staticmethod
    def log_progress(logger: logging.Logger, current: int, total: int, message: str = ""):
        percentage = (current / total * 100) if total > 0 else 0
        logger.info(f"进度: {current}/{total} ({percentage:.2f}%) {message}")
    
    @staticmethod
    def log_error(logger: logging.Logger, error: Exception, context: str = ""):
        logger.error(f"{context}: {type(error).__name__}: {str(error)}", exc_info=True)
    
    @staticmethod
    def create_timestamped_filename(base_name: str, extension: str = "log") -> str:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{base_name}_{timestamp}.{extension}"
