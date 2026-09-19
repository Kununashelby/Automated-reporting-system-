import logging
import os


def setup_logger(
    name="automated_reporting",
    log_file="logs/reporting.log"
):
    """
    Configure the application logger.
    """

    # Create logs directory
    log_directory = os.path.dirname(log_file)

    if log_directory:
        os.makedirs(log_directory, exist_ok=True)

    logger = logging.getLogger(name)

    # Prevent duplicate handlers
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    # File handler
    file_handler = logging.FileHandler(
        log_file,
        encoding="utf-8"
    )

    # Console handler
    console_handler = logging.StreamHandler()

    # Log format
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger