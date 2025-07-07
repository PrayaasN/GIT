import logging
import sys

def get_logger(name: str, log_file: str = "logs/app.log") -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Formatter with milliseconds
    formatter = logging.Formatter(
        fmt="%(asctime)s.%(msecs)03d - [%(levelname)s] - %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Stream (console) handler
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)

    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)

    # Avoid duplicate logs if handlers already added
    if not logger.handlers:
        logger.addHandler(stream_handler)
        logger.addHandler(file_handler)

    return logger