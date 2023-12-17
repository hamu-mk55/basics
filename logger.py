import os
import time
import datetime
from logging import (getLogger, Formatter, FileHandler, StreamHandler,
                     DEBUG, INFO, WARNING, ERROR, CRITICAL)


class MyLogger:
    def __init__(self,
                 log_dir: str = './log',
                 level: int = DEBUG,
                 filename: str = 'log_',
                 file_unit: str = 'month',
                 console_out: bool = True,
                 file_out: bool = True,
                 log_serial: str = 'MyLogger'):
        self.log_dir = log_dir
        self.level = level
        self.filename = filename
        self.file_unit = file_unit
        self.console_out = console_out
        self.file_out = file_out
        self.log_serial = log_serial

        self.log_file = None
        self.time_id = None

        # Setup Format
        if self.file_unit == 'month':
            _date_fmt = '%m/%d,%H:%M:%S'
        else:
            _date_fmt = '%H:%M:%S'

        _fmt = '%(asctime)s,%(msecs)03d,[%(levelname).4s],%(message)s'
        self.format = Formatter(_fmt, datefmt=_date_fmt)

        # Setup logger
        if self.file_out:
            os.makedirs(self.log_dir, exist_ok=True)
        self.logger = getLogger(self.log_serial)
        self.logger.setLevel(self.level)

        self.init()

    def __del__(self):
        pass

    def init(self):
        # Set time_id
        self.time_id = self._get_time_id()

        # Initialize handlers
        for _handler in self.logger.handlers[::-1]:
            self.logger.removeHandler(_handler)

        # Set File-Output
        if self.file_out:
            self.log_file = f'{self.log_dir}/{self.filename}{self.time_id}.log'
            os.makedirs(self.log_dir, exist_ok=True)

            fh = FileHandler(self.log_file)
            fh.setLevel(self.level)
            fh.setFormatter(self.format)
            self.logger.addHandler(fh)

        # Set Console-Output
        if self.console_out:
            sh = StreamHandler()
            sh.setLevel(self.level)
            sh.setFormatter(self.format)
            self.logger.addHandler(sh)

    def _get_time_id(self):
        if self.file_unit == 'month':
            _time_id = datetime.datetime.now().strftime('%Y%m')
        else:
            _time_id = datetime.datetime.now().strftime('%Y%m%d')

        return _time_id

    def _check_time_id(self):
        _time_id = self._get_time_id()
        if _time_id != self.time_id:
            self.init()

    def debug(self, msg):
        self._check_time_id()
        self.logger.debug(str(msg))

    def info(self, msg):
        self._check_time_id()
        self.logger.info(str(msg))

    def warning(self, msg):
        self._check_time_id()
        self.logger.warning(str(msg))

    def error(self, msg):
        self._check_time_id()
        self.logger.error(str(msg))

    def critical(self, msg):
        self._check_time_id()
        self.logger.critical(str(msg))

def example():
    app = MyLogger(level=INFO,
                   file_unit='day',
                   console_out=True,
                   file_out=True
                   )
    while True:
        app.debug('test_debug')
        app.info('test_info')
        app.warning('test_warn')
        app.error('test_err')
        app.critical('test_crt')
        app.logger.critical('test_crt')

        time.sleep(60*30)


if __name__ == '__main__':
    example()

