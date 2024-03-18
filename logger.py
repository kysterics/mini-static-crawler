import logging
import time
from datetime import timedelta, datetime
from tqdm import tqdm

from pathlib import Path
import os
import inspect


class LogFormatter():
    def __init__(self):
        self.start_time = time.time()

    def format(self, record):
        """ overriding the default logging.Formatter because it uses time.strftime
            which has no support for microseconds, and datetime.strftime does
        """
        elapsed_seconds = round(record.created - self.start_time)

        prefix = "%s | %s ║ %s" % (
            time.strftime('%x %X') + datetime.fromtimestamp(record.created).strftime('.%f')[:4],
            timedelta(seconds=elapsed_seconds),
            record.levelname,
        )
        message = record.getMessage()
        message = message.replace('\n', '\n' + ' ' * (len(prefix) + 3))
        return "%s ║ %s" % (prefix, message) if message else ''

    def reset_time(self):
        self.start_time = time.time()


class ChildProcessHandler(logging.StreamHandler):
    def __init__(self, message_queue):
        self.message_queue = message_queue
        logging.StreamHandler.__init__(self)

    def emit(self, record):
        self.message_queue.put(record)


def setup_logger_child_process(message_queue):
    # create logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    logger.handlers = []

    # create queue handler
    child_process_handler = ChildProcessHandler(message_queue)
    child_process_handler.setLevel(logging.INFO)
    logger.addHandler(child_process_handler)


class TqdmHandler(logging.StreamHandler):
    def __init__(self):
        logging.StreamHandler.__init__(self)

    def emit(self, record):
        msg = self.format(record)
        tqdm.write(msg)


def setup_tqdm_logger():
    # create logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.propagate = False
    logger.handlers = []

    # create tqdm handler
    tqdm_handler = TqdmHandler()
    tqdm_handler.setLevel(logging.DEBUG)  # logging.INFO
    tqdm_handler.setFormatter(LogFormatter())
    logger.addHandler(tqdm_handler)

    return logger


def setup_std_logger():
    # create logger
    logger = logging.getLogger(datetime.now().strftime('%f'))
    logger.setLevel(logging.DEBUG)
    logger.propagate = False
    logger.handlers = []

    return logger


class TqdmLogger():
    def __init__(self, mode='a'):
        if not isinstance(mode, str):
            raise TypeError("argument 'mode' must be str")
        if mode in {'a', 'c'}:
            self.logger = setup_tqdm_logger()
            self.formatter = LogFormatter()
            self.ext = 'log'
        elif mode == 'f':
            self.logger = setup_std_logger()
            self.formatter = None
            self.ext = ''
        else:
            raise ValueError(f"invalid mode: '{mode}'")

        self.level = ''
        self.mode = mode

    def setup_file_handler(self, filename, filepath, ext):
        if filename is None:
            filename = self.level
        if ext is None:
            ext = self.ext
        if ext:
            ext = '.' + ext

        # create directory for logs
        stack = inspect.stack()
        the_method = stack[3][0].f_code.co_name
        base_dir = Path(__file__).parent.absolute()
        sub_dir = os.path.join(base_dir, filepath)
        os.makedirs(sub_dir, exist_ok=True)

        # create file handler
        file_handler = logging.FileHandler(f'{sub_dir}/{the_method}__{filename}{ext}', "a")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(self.formatter)

        return file_handler

    def wrapper(self, log_func, filename, filepath, ext):
        if self.mode == 'c':
            log_func()
            return

        file_handler = self.setup_file_handler(filename, filepath, ext)
        self.logger.addHandler(file_handler)
        log_func()
        self.logger.removeHandler(file_handler)
        file_handler.close()

    def debug(self, msg, *args, filename=None, filepath='logs', ext=None):
        self.level = 'DEBUG'
        self.wrapper(lambda: self.logger.debug(msg, *args), filename, filepath, ext)

    def info(self, msg, *args, filename=None, filepath='logs', ext=None):
        self.level = 'INFO'
        self.wrapper(lambda: self.logger.info(msg, *args), filename, filepath, ext)

    def warning(self, msg, *args, filename=None, filepath='logs', ext=None):
        self.level = 'WARNING'
        self.wrapper(lambda: self.logger.warning(msg, *args), filename, filepath, ext)

    def error(self, msg, *args, filename=None, filepath='logs', ext=None):
        self.level = 'ERROR'
        self.wrapper(lambda: self.logger.error(msg, *args), filename, filepath, ext)

    def critical(self, msg, *args, filename=None, filepath='logs', ext=None):
        self.level = 'CRITICAL'
        self.wrapper(lambda: self.logger.critical(msg, *args), filename, filepath, ext)

    def exception(self, msg, *args, filename=None, filepath='logs', ext=None):
        self.level = 'EXCEPTION'
        self.wrapper(lambda: self.logger.exception(msg, *args), filename, filepath, ext)

    d = debug
    i = info
    w = warning
    e = error
    c = critical
    x = exception

