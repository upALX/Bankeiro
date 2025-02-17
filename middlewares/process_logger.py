import logging
import uuid
import os
from datetime import datetime


class MiddlewareLogger:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, log_dir: str = "logs", log_level: int = logging.INFO):
        if not hasattr(self, "_initialized"):
            self._initialized = False

        if self._initialized:
            return

        self.log_dir = log_dir
        self.log_level = log_level
        self.process_uuid = None
        self.logger = None

        os.makedirs(log_dir, exist_ok=True)

        self._initialized = True

    def start_process(self):
        """Starts a new logging process."""
        self.process_uuid = str(uuid.uuid4())
        process_name = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        log_file = os.path.join(self.log_dir, f"{process_name}_{self.process_uuid}.log")

        self.logger = logging.getLogger(self.process_uuid)
        self.logger.setLevel(self.log_level)

        if self.log_level != logging.DEBUG:
            file_handler = logging.FileHandler(log_file)
            formatter = logging.Formatter(
                fmt="%(asctime)s - %(levelname)s - %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        formatter = logging.Formatter(
            fmt="%(asctime)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        self.logger.info(f"Process started with UUID {self.process_uuid}.")

    def info(self, message: str):
        """Logs an informational message."""
        self._log(logging.INFO, message)

    def debug(self, message: str):
        """Logs a debug message."""
        self._log(logging.DEBUG, message)

    def warning(self, message: str):
        """Logs a warning message."""
        self._log(logging.WARNING, message)

    def error(self, message: str):
        """Logs an error message."""
        self._log(logging.ERROR, message)

    def _log(self, level: int, message: str):
        """Helper method to log a message."""
        if not self.logger:
            print("[WARNING] Logger not initialized. Automatically initializing logger.")
            self.start_process()
        self.logger.log(level, message)

    def end_process(self):
        """Ends the current process and clears the logger."""
        if self.logger:
            self.logger.info(f"Process with UUID {self.process_uuid} ended.")
            handlers = self.logger.handlers[:]
            for handler in handlers:
                self.logger.removeHandler(handler)
                handler.close()
            self.logger = None
            self.process_uuid = None
