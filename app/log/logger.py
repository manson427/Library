from loguru import logger

logger.add(
    "log/debug.txt",
    level="DEBUG",
    enqueue=True,
    rotation="1 week",
    compression="zip",
    colorize=True,
    format="{time} {level} {message}",
)
