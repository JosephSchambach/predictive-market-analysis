import logging
from typing import Literal

class Logger:
    def __init__(self, log_file='error.log', log_level=logging.ERROR):
        self.logger = logging.getLogger('custom_logger')
        if not self.logger.handlers:
            self.logger.setLevel(log_level)
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(log_level)
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

    def log(self, message, level: Literal['ERROR','CRITICAL'] = None):
        def _print_message(message, level):
            print_message = f"{level}: {message}"
            print(print_message)
        if not level:
            print(message)
        else:
            _print_message(message, level)
            if level == 'ERROR':
                self.logger.error(message)
            elif level == 'CRITICAL':
                self.logger.critical(message)

