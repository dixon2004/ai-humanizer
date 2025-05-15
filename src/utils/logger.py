import logging.handlers
import logging
import os


class SyncLogger:

    def __init__(self, class_name: str, log_level: str = "INFO", log_path: str = "./logs", backup_count: int = 3):
        """
        Initialize the SyncLogger class and set up loggers.
        
        Args:
            class_name (str): The name of the class using the logger.
            log_level (str): The logging level (default is "INFO").
            log_path (str): Path where log files are stored (default is "./logs").
            backup_count (int): Number of backup log files to keep (default is 3).
        """
        self.class_name = class_name
        self.log_path = log_path
        self.backup_count = backup_count

        os.makedirs(self.log_path, exist_ok=True)

        self.log_level = getattr(logging, log_level.upper(), logging.INFO)
        
        self.formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        
        self.logger_info = self._setup_logger("infoLog", "info.log", self.log_level)
        self.logger_error = self._setup_logger("errorLog", "error.log", logging.ERROR)


    def _setup_logger(self, name: str, log_file: str, log_level: int) -> logging.Logger:
        """
        Set up and return a logger with both console and rotating file handlers.
        
        Args:
            name (str): The name of the logger.
            log_file (str): The name of the log file.
            log_level (int): The logging level.

        Returns:
            logging.Logger: Configured logger instance.
        """
        logger = logging.getLogger(name)

        if not logger.hasHandlers():
            logger.setLevel(log_level)

            console_handler = logging.StreamHandler()
            console_handler.setFormatter(self.formatter)
            logger.addHandler(console_handler)

            file_path = os.path.join(self.log_path, log_file)
            file_handler = logging.handlers.RotatingFileHandler(
                file_path, maxBytes=10 * 1024 * 1024, backupCount=self.backup_count
            )
            file_handler.setFormatter(self.formatter)
            logger.addHandler(file_handler)

            logger.propagate = False

        return logger


    def write_log(self, log_type: str, message: str) -> None:
        """
        Write a log message to the appropriate logger based on the log type.

        Args:
            log_type (str): The type of log message (e.g., "debug", "info", "warning", "error", "critical").
            message (str): The message to be logged.
        """
        loggers = {
            "debug": self.logger_info.debug,
            "info": self.logger_info.info,
            "warning": self.logger_error.warning,
            "error": self.logger_error.error,
            "critical": self.logger_error.critical
        }

        log_type = log_type.lower()
        log_func = loggers.get(log_type)

        if log_func:
            log_func(f"[{self.class_name}] {message}")
        else:
            self.logger_error.error(f"[{self.class_name}] Unknown log type: {log_type}")
