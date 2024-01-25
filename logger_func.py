import os
import time
import datetime
from logging import (getLogger, Logger, Formatter,
                     FileHandler, StreamHandler, handlers,
                     DEBUG, INFO, WARNING, ERROR, CRITICAL)


def _set_level(level: str)->int:
    if level.lower() == 'debug':
        return DEBUG
    elif level.lower() == 'info':
        return INFO
    elif level.lower() == 'warning':
        return WARNING
    elif level.lower() == 'error':
        return ERROR
    elif level.lower() == 'critical':
        return CRITICAL
    else:
        return WARNING


def _set_format()->Formatter:
    _date_fmt = '%m/%d,%H:%M:%S'
    _fmt = '%(asctime)s,%(msecs)03d,[%(levelname).4s][%(funcName)s][%(lineno)d], %(message)s'

    return Formatter(_fmt, datefmt=_date_fmt)


def make_logger(log_dir: str = './log',
                level: str = 'debug',
                file_name: str = 'mylogger',
                console_out: bool = True,
                file_out: bool = True,
                logger_id: str = 'MyLogger') -> Logger:
    # Set logger
    log_level = _set_level(level)
    log_formatter = _set_format()

    logger = getLogger(logger_id)
    logger.setLevel(log_level)

    # Set File-Output
    if file_out:
        os.makedirs(log_dir, exist_ok=True)

        fh = handlers.TimedRotatingFileHandler(
            f'{log_dir}/{file_name}.log',
            when="MIDNIGHT"
        )
        fh.setLevel(log_level)
        fh.setFormatter(log_formatter)
        logger.addHandler(fh)

    # Set Console-Output
    if console_out:
        sh = StreamHandler()
        sh.setLevel(log_level)
        sh.setFormatter(log_formatter)
        logger.addHandler(sh)

    return logger


def example():
    logger = make_logger()

    while True:
        logger.debug('test_debug')
        logger.info('test_info')
        logger.warning('test_warn')
        logger.error('test_err')
        logger.critical('test_crt')
        logger.log(INFO, 'test_log')

        time.sleep(30)


if __name__ == '__main__':
    example()
