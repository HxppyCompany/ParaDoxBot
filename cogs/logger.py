import time
import colorama
import inspect

levels = {
    'DEBUG': 0,
    'INFO': 1,
    'WARNING': 2,
    'ERROR': 3,
    'FATAL': 4
}

localtime = time.localtime()
f = colorama.Fore


class Logger:
    def __init__(self, level: str | int, strfmt: str, datefmt: str = '%Y/%m/%d %H:%M:%S'):
        """

        :param level: use level name to configure log level
        :param strfmt: use variables <date>, <level>, <message>, <module> to format log
        :param datefmt: use time format to format <date> variable
        :return: setup logger configuration
        """

        colorama.init()

        if (level := level.upper()) in levels.keys():
            self.level_num = int(levels[level])
        elif level in levels.values():
            self.level_num = int(level)
        else:
            raise ValueError(f'Invalid log level: {level}')

        if strfmt.strip() != '':
            self.strfmt = strfmt
        else:
            raise ValueError('Log format cannot be empty')

        try:
            time.strftime(datefmt, localtime)
            self.datefmt = datefmt
        except:
            raise ValueError(f'Invalid date format: {datefmt}')

    def debug(self, message):
        if self.level_num <= 0:
            print(self.format_log(0, message, inspect.currentframe().f_back.f_code.co_name))

    def info(self, message):
        if self.level_num <= 1:
            print(self.format_log(1, message, inspect.currentframe().f_back.f_code.co_name))

    def warning(self, message):
        if self.level_num <= 2:
            print(self.format_log(2, message, inspect.currentframe().f_back.f_code.co_name))

    def error(self, message):
        if self.level_num <= 3:
            print(self.format_log(3, message, inspect.currentframe().f_back.f_code.co_name))

    def fatal(self, message):
        if self.level_num <= 4:
            print(self.format_log(4, message, inspect.currentframe().f_back.f_code.co_name))

    def format_log(self, level, message, module):
        fmt = (self.strfmt.replace('<date>', time.strftime(self.datefmt, localtime)).
               replace('<message>', message).
               replace('<module>', module))

        match level:
            case 0:
                fmt = fmt.replace('<level>', f.LIGHTCYAN_EX + 'DEBUG')
            case 1:
                fmt = fmt.replace('<level>', f.LIGHTGREEN_EX + 'INFO')
            case 2:
                fmt = fmt.replace('<level>', f.LIGHTYELLOW_EX + 'WARNING')
            case 3:
                fmt = fmt.replace('<level>', f.LIGHTRED_EX + 'ERROR')
            case 4:
                fmt = fmt.replace('<level>', f.LIGHTMAGENTA_EX + 'FATAL')

        return fmt
