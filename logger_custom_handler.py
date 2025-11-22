import os
import time
import datetime
import logging
from logging import (getLogger, Logger, Formatter,
                     FileHandler, StreamHandler, handlers,
                     DEBUG, INFO, WARNING, ERROR, CRITICAL)


class CustomFileHandler(logging.Handler):
    def __init__(self,
                 log_dir='./log',
                 base_name='app.log',
                 rotation='day',
                 encoding='utf-8'):

        super().__init__()
        self.log_dir = log_dir
        self.base_name = base_name
        self.rotation = rotation
        self.encoding = encoding

        assert self.rotation in ('day', 'month')

        os.makedirs(self.log_dir, exist_ok=True)
        self.current_time_key = None
        self.stream = None
        self._update_logfile()

    def _get_time_key(self):
        now = datetime.datetime.now()
        if self.rotation == 'day':
            return now.strftime('%Y%m%d')
        elif self.rotation == 'month':
            return now.strftime('%Y%m')

    def _get_logfile_path(self, time_key):
        filename = f"{time_key}_{self.base_name}"
        return os.path.join(self.log_dir, filename)

    def _update_logfile(self):
        time_key = self._get_time_key()
        if self.current_time_key != time_key:
            if self.stream:
                self.stream.close()
            self.current_time_key = time_key
            log_path = self._get_logfile_path(time_key)
            self.stream = open(log_path, mode='a', encoding=self.encoding)

    def emit(self, record):
        try:
            self._update_logfile()
            msg = self.format(record)
            self.stream.write(msg + '\n')
            self.stream.flush()
        except Exception:
            self.handleError(record)

    def close(self):
        if self.stream:
            self.stream.close()
        super().close()


def _set_level(level: str) -> int:
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


def _set_format(date_fmt=None, fmt=None) -> Formatter:

    if date_fmt is None:
        date_fmt = '%m/%d,%H:%M:%S'

    if fmt is None:
        fmt = '%(asctime)s,%(msecs)03d,[%(levelname).4s][%(name)s][%(funcName)s][%(lineno)d], %(message)s'

    return Formatter(fmt, datefmt=date_fmt)


def setup_logger(log_dir: str = './log',
                 level: str = 'debug',
                 file_name: str = 'mylogger.log',
                 log_rotate: str = 'day',
                 console_out: bool = True,
                 file_out: bool = True,
                 fmt = None,
                 date_fmt=None):
    # Set logger
    log_level = _set_level(level)
    log_formatter = _set_format(fmt=fmt, date_fmt=date_fmt)
    log_id = file_name.split('.')[0]

    logger = getLogger(log_id)
    logger.setLevel(log_level)

    if not logger.handlers:
        # Set File-Output
        if file_out:
            os.makedirs(log_dir, exist_ok=True)

            fh = CustomFileHandler(log_dir=log_dir,
                                   base_name=file_name,
                                   rotation=log_rotate)

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
    logger = setup_logger()

    while True:
        logger.debug('test_debug')
        logger.info('test_info')
        logger.warning('test_warn')
        logger.error('test_err')
        logger.critical('test_crt')
        logger.log(INFO, 'test_log')

        try:
            raise Exception("test")
        except Exception as err:
            logger.exception(err)

        time.sleep(30)


if __name__ == '__main__':
    example()
