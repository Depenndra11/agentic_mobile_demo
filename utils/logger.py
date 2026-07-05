import logging
from pathlib import Path


def get_logger(name="TestLogger"):

    log_dir = (
        Path(__file__).resolve().parent.parent
        / "logs"
    )

    log_dir.mkdir(exist_ok=True)

    log_file = log_dir / "test_execution.log"

    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s",
        "%Y-%m-%d %H:%M:%S"
    )

    file_handler = logging.FileHandler(
        log_file,
        encoding="utf-8"
    )

    console_handler = logging.StreamHandler()

    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger