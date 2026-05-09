import logging
from config.settings import LOG_DIRECTORY_CONST , LOG_FILE_CONST, LOG_NAME
import os


class MyFormatter(logging.Formatter):
    def format(self, record):
        if record.levelno == logging.INFO:
            record.ip_target = getattr(record, 'ip_target', '')
            record.port_target = getattr(record,'port_target', '')
            
            self._style._fmt = "%(asctime)s - %(levelname)s - %(name)s - %(message)s  ip target : %(ip_target)s - port target : %(port_target)s"
            return super().format(record)
        elif record.levelno == logging.DEBUG:
            record.action = getattr(record, 'action', '')
            record.ip_port = getattr(record,'ip_port','')
            record.state = getattr(record,'state','') # fijarse 
            record.service = getattr(record,'service',None)
            # eliminar cuando se calcule automaticamente
            
            self._style._fmt = '%(asctime)s - %(levelname)s - %(action)s -> IP:Port %(ip_port)s - State : %(state)s - Service : %(service)s'
            return super().format(record)
        elif record.levelno == logging.ERROR:
            record.cause = getattr(record,'cause','')
            record.failed = getattr(record,'failed','')
            self._style._fmt = "%(asctime)s - %(levelname)s - %(cause)s -> %(failed)s "
            return super().format(record)
        elif record.levelno == logging.WARNING:
            self._style._fmt = "%(asctime)s - %(levelname)s"
            return super().format(record) 


def setup_logger(level):
    logger = logging.getLogger(LOG_NAME)
    logger.setLevel(level) 


    log_directory = LOG_DIRECTORY_CONST
    log_file = LOG_FILE_CONST

    if (logger.hasHandlers()):
        return logger

    log_path = os.path.join(log_directory,log_file)
    file_handler = logging.FileHandler(log_path,encoding='utf-8')

    formatter = MyFormatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S" )

    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger