"""
Logger configuration.
Please read https://docs.python.org/3/howto/logging.html if you are not familiar
with logging package
"""
import copy
import datetime as dt
import functools
import logging
from typing import Any
from typing import Callable
from typing import TypeVar

RED = '\033[0;31m '
GREEN = '\033[0;92m '
BLUE = '\033[0;34m '
YELLOW = '\033[1;33m '
WHITE = '\033[1;37m '
NO_COLOR = ' \033[0m'

COLORS = {
    'CRITICAL': RED,
    'ERROR':    RED,
    'WARNING':  YELLOW,
    'INFO':     BLUE,
    'DEBUG':    WHITE,
    }


class ColoredFormatter(logging.Formatter):  # pragma: no cover
    """
    🌈
    """

    def format(self, record):
        """
        Add 🌈 to message in record
        """
        levelname = record.levelname
        color = COLORS[levelname]
        record = copy.copy(record)
        record.msg = color + str(record.msg) + NO_COLOR
        return super().format(record)


def set_logs_level(name: str, level: str):
    """
    Change log level for a particular logger (also affects logger's children
    if they do not have their own level)
    """
    logger = logging.getLogger(name)
    logger.setLevel(level.upper())


def get_logger(name: str):
    """
    Return logger with the given name. Also make sure that it will not print
    any logs unless it is configured explicitly
    """
    top_level_name = name.split('.')[0]
    top_level_logger = logging.getLogger(top_level_name)

    if not top_level_logger.handlers:
        top_level_logger.addHandler(logging.NullHandler())

    return logging.getLogger(name)


def configure_logger(name: str, level: str):
    """
    Configure logger with the given name (it will also affect all its children)
    with coloured output and some reasonable log format
    """
    # logging.captureWarnings(True)

    top_level_name = name.split('.')[0]
    top_level_logger = logging.getLogger(top_level_name)

    if (not top_level_logger.handlers
            or len(top_level_logger.handlers) == 1
            and isinstance(top_level_logger.handlers[0], logging.NullHandler)):
        log_format = ("%(levelname)-8s %(asctime)s %(name)-15s"
                      " %(message)s")

        formatter = ColoredFormatter(log_format)
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        top_level_logger.addHandler(stream_handler)

    local_logger = logging.getLogger(name)
    local_logger.setLevel(level.upper())


AnyCallable = TypeVar('AnyCallable', bound=Callable[..., Any])


def log_time(logger_name: str,
             log_level: str = 'debug',
             *, print_params: bool = False,
             ) -> Callable[[AnyCallable], AnyCallable]:  # pragma: no cover
    """
    Print function runtime to the logger with the given name. Optionally also
    print function params
    """

    def _decorator(func: AnyCallable) -> AnyCallable:
        logger = get_logger(logger_name)
        level_number = getattr(logging, log_level.upper())

        @functools.wraps(func)
        def _wrapped(*args, **kwargs):

            if print_params:
                logger.log(level_number,
                           f'Starting {func.__name__} with params {args}, '
                           f'{kwargs}')
            else:
                logger.log(level_number, f'Starting {func.__name__}')

            start = dt.datetime.now()
            result = func(*args, **kwargs)
            end = dt.datetime.now()

            logger.log(level_number, f'{func.__name__} runtime: {end - start}')

            return result

        return _wrapped

    return _decorator
