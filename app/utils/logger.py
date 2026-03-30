import logging
from app.config import settings


def get_logger(name: str) -> logging.Logger:
    """
    Returns a configured logger instance
    """

    logger = logging.getLogger(name)

    if logger.handlers:
        return logger  # Avoid duplicate handlers

    logger.setLevel(settings.LOG_LEVEL)

    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s] - %(message)s"
    )

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger