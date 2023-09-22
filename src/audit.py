import logging
import logging.handlers
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

LOG_FORMAT = "%(asctime)s:%(name)s:%(levelname)s - %(message)s"
CONSOLE_LOG_FORMAT = "%(levelname)s - %(message)s"
logging.basicConfig(
    level=logging.ERROR,
    format=LOG_FORMAT,
)
CURRENT_DIRECTORY: Path = Path(__file__).parent
BASE_DIRECTORY = CURRENT_DIRECTORY.parent


def make_path_absolute(path: str, base_dir: Path = BASE_DIRECTORY) -> Path:
    if os.path.isabs(path):
        path = Path(path)
    else:
        path = base_dir.joinpath(path)
    return path


@dataclass
class LoggingSetup:
    name: str
    console_level: int = logging.ERROR
    file_level: int = logging.INFO
    console_format: str = CONSOLE_LOG_FORMAT
    file_format: str = LOG_FORMAT
    file_name: Optional[str] = None
    max_file_size_in_bytes: int = 1024 * 1024
    file_backup_count: int = 16
    log_directory: Path = make_path_absolute("logs", BASE_DIRECTORY)
    os.makedirs(log_directory, exist_ok=True)

    def get_effective_log_level(self):
        return min(self.console_level, self.file_level)


def get_logger(log_config: LoggingSetup) -> logging.Logger:
    """
    Create a logger and return.
    Arguments:
        log_config: configuration object of a logger
    Return:
        logger: the created logger
    """
    logger = logging.getLogger(
        name=log_config.name
    )
    if logger.handlers:
        logger.warning("This logger is already set up")
        return logger

    logger.setLevel(log_config.get_effective_log_level())
    logger.propagate = False
    stream_formatter = logging.Formatter(log_config.console_format)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(stream_formatter)
    stream_handler.setLevel(log_config.console_level)

    logger.addHandler(stream_handler)
    if log_config.file_name is None:
        log_config.file_name = log_config.name.lower() + ".log"
        logging.warning(
            "No file specified, defaulting to '%s'" % log_config.file_name
        )

    file_name = log_config.log_directory.joinpath(log_config.file_name)
    file_formatter = logging.Formatter(log_config.file_format)

    file_handler = logging.handlers.RotatingFileHandler(
        file_name, maxBytes=log_config.max_file_size_in_bytes,
        backupCount=log_config.file_backup_count
    )
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(log_config.file_level)

    logger.addHandler(file_handler)
    logger.debug("Logger %s has been created" % logger.name)
    return logger


def get_logger_by_name(name: str):
    log_config = LoggingSetup(name=name)
    return get_logger(log_config)
