import sys
from loguru import logger


def setup_logger():
    logger.remove()
    console_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "<level>{message}</level>"
    )
    logger.add(sys.stdout, format=console_format, level="DEBUG", colorize=True)
    file_format = "{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {message}"
    logger.add(
        "logs/app.log",
        format=file_format,
        level="INFO",
        rotation="1 MB",
        retention="7 days",
    )
    return logger


app_logger = setup_logger()
