import logging
from logging.handlers import RotatingFileHandler

def setup_logger(logger_name):
    # create log level
    default_logging_level = logging.DEBUG

    # create logger
    logger = logging.getLogger(logger_name)
    logger.setLevel(default_logging_level)

    # create formatter
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    # create a rotating log with a max size of 10MB and up to 5 backup files
    rotating_file_handler = RotatingFileHandler(f'{logger_name}.log', maxBytes=10*1024*1024, backupCount=3)
    rotating_file_handler.setLevel(default_logging_level)
    rotating_file_handler.setFormatter( formatter )

    # create console handler and set level to debug
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(default_logging_level)
    stream_handler.setFormatter(formatter)

    logger.addHandler(rotating_file_handler)
    logger.addHandler(stream_handler)

    logger.debug("Started Logger")
    return logger
