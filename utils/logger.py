import logging
from config.settings import LOG_DIRECTORY_CONST , LOG_FILE_CONST, LOG_NAME
import os



def setup_logger(level):
    logger = logging.getLogger(LOG_NAME)
    logger.setLevel(level) 

    log_directory = LOG_DIRECTORY_CONST
    log_file = LOG_FILE_CONST

    if (logger.hasHandlers()):
        return logger

    log_path = os.path.join(log_directory,log_file)
    file_handler = logging.FileHandler(log_path,encoding='utf-8')

    formatter = logging.Formatter(fmt="%(asctime)s | %(levelname)s | %(name)s | " "%(filename)s:%(lineno)d | %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger