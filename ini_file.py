import os
import configparser
from logging import getLogger, Logger


class DefaultParams:
    def __init__(self,
                 name: str,
                 section: str,
                 key: str,
                 default_val: str | float,
                 param_type: str):
        self.name = name
        self.section = section
        self.key = key
        self.default_val = default_val
        self.type = param_type


class IniFile:
    def __init__(self,
                 inifile: str = None,
                 logger: Logger = None):
        self.inifile = inifile
        self.default_params_list: list[DefaultParams] = []

        if logger is not None:
            self.logger = logger
        else:
            self.logger = getLogger(__name__)

    def load_inifile(self) -> None:
        self.logger.info(f'load inifile')

        if not os.path.isfile(self.inifile):
            _msg = f'No ini-file: {self.inifile}'
            self.logger.error(_msg)
            raise FileNotFoundError(_msg)

        _config = configparser.ConfigParser()
        _config.read(self.inifile)
        for _params in self.default_params_list:
            if _params.type == 'float':
                try:
                    _val = float(_config.get(_params.section, _params.key))
                except Exception as err:
                    self.logger.error(f'load_inifile: {_params.name}')
                    self.logger.error(f'load_inifile: {err}')
                    raise ValueError(err)

                exec(f'{_params.name} = {_val}')

            elif _params.type == 'str':
                try:
                    _val = _config.get(_params.section, _params.key)
                except Exception as err:
                    self.logger.error(f'load_inifile: {_params.name}')
                    self.logger.error(f'load_inifile: {err}')
                    raise ValueError(err)

                exec(f'{_params.name} = "{_val}"')

            else:
                _msg = f'load_inifile: illegal type: {_params.name}'
                self.logger.error(_msg)
                raise ValueError(_msg)

    def set_default_params(self) -> None:
        self.logger.info(f'set default')

        for _params in self.default_params_list:
            if _params.type == 'float':
                exec(f'{_params.name} = {_params.default_val}')

            elif _params.type == 'str':
                exec(f'{_params.name} = "{_params.default_val}"')
            else:
                _msg = f'load_inifile: illegal type: {_params.name}'
                self.logger.error(_msg)
                raise ValueError(_msg)

    def show_params(self) -> None:
        for _params in self.default_params_list:
            _val = eval(_params.name)

            _msg = f'{_params.name} = {_val}'
            self.logger.info(_msg)
            print(_msg)

    def remake_inifile(self,
                       inifile: str,
                       default_flg: bool = True) -> None:
        self.logger.info(f'remake inifile: {inifile}')

        _config = configparser.ConfigParser()

        _section_pre = None
        for _params in self.default_params_list:
            if _params.section != _section_pre:
                _config.add_section(_params.section)
                _section_pre = _params.section

            if default_flg:
                _config.set(_params.section, _params.key, str(_params.default_val))
            else:
                _val = eval(_params.name)
                _config.set(_params.section, _params.key, str(_val))

        with open(inifile, 'w') as fw:
            _config.write(fw)


class ExampleIniFile(IniFile):
    def __init__(self,
                 inifile: str = 'config.ini',
                 logger: Logger = None):
        super().__init__(inifile=inifile, logger=logger)

        # Define parameters as None (Recommend for IntelliSense)
        self.str = None
        self.float = None
        # self.err = None

        # Define parameters
        self.default_params_list = [
            DefaultParams(name='self.str', section='Example', key='str', default_val='val', param_type='str'),
            DefaultParams(name='self.float', section='Example2', key='float', default_val=10, param_type='float'),
            # DefaultParams(name='self.err', section='Example2', key='err', default_val=10, param_type='floa')
        ]


if __name__ == '__main__':
    app = ExampleIniFile()
    app.set_default_params()
    app.load_inifile()
    app.show_params()
    app.remake_inifile('config.ini', default_flg=False)
