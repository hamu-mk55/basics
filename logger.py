import os
import time
import datetime
from logging import (getLogger, Logger, Formatter,
                     FileHandler, StreamHandler,
                     DEBUG, INFO, WARNING, ERROR, CRITICAL)


class CustomLogger(Logger):
    def __init__(self,
                 log_dir: str = './log',
                 level: str = 'debug',
                 filename: str = 'log_',
                 file_unit: str = 'month',
                 console_out: bool = True,
                 file_out: bool = True,
                 log_serial: str = 'MyLogger'):

        super().__init__(log_serial)

        # Set Params
        self.log_dir = log_dir
        self.level = self._return_level(level)
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

        _fmt = '%(asctime)s,%(msecs)03d,[%(levelname).4s],%(lineno)d,%(message)s'
        self.format = Formatter(_fmt, datefmt=_date_fmt)

        # Setup Othres
        self.setLevel(self.level)

        if self.file_out:
            os.makedirs(self.log_dir, exist_ok=True)

        self._setup_handlers()

    def _log(self, level, msg, args, **kwargs):
        """
        Overwrite logger functions
        Before logging, check if date is changed
        """

        # check date
        self._check_time_id()

        # Call Logger-function
        stacklevel = kwargs.get("stacklevel", 1)
        kwargs["stacklevel"] = stacklevel + 1

        super()._log(level, msg, args, **kwargs)

    def _setup_handlers(self):
        # Set time_id
        self.time_id = self._get_time_id()

        # Initialize handlers
        for _handler in self.handlers[:]:
            self.removeHandler(_handler)

        # Set File-Output
        if self.file_out:
            self.log_file = f'{self.log_dir}/{self.filename}{self.time_id}.log'
            os.makedirs(self.log_dir, exist_ok=True)

            fh = FileHandler(self.log_file)
            fh.setLevel(self.level)
            fh.setFormatter(self.format)
            self.addHandler(fh)

        # Set Console-Output
        if self.console_out:
            sh = StreamHandler()
            sh.setLevel(self.level)
            sh.setFormatter(self.format)
            self.addHandler(sh)

    @staticmethod
    def _return_level(level: str):
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

    def _get_time_id(self):
        if self.file_unit == 'month':
            _time_id = datetime.datetime.now().strftime('%Y%m')
        else:
            _time_id = datetime.datetime.now().strftime('%Y%m%d')

        return _time_id

    def _check_time_id(self):
        _time_id = self._get_time_id()
        if _time_id != self.time_id:
            self._setup_handlers()


def example():
    app = CustomLogger(level='info',
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
        # app.exception('test_ex')
        app.log(INFO, 'test_log')

        time.sleep(60 * 30)


if __name__ == '__main__':
    example()
