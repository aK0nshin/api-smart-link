import logging

from api_smart_link.settings import build_config, storage

_MANAGER_LOGGER = logging.getLogger(__name__)


class UndefinedLoggerException(Exception):
    """Raised when can't find variable in environment"""
    pass


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class LogManager(object, metaclass=Singleton):
    ROOT_NAME = ''
    FALLBACK_LEVEL = logging.WARNING
    BASE_LOGGER = None
    LOG_FORMAT = '%(asctime)s \t [%(levelname)s | %(filename)s:%(lineno)s] \t %(message)s'

    _loggers = dict()
    _moduleToLevel = dict()

    def __init__(self, app_name: str, log_level: str = logging.WARNING, module_to_level: dict = None,
                 log_format: str = None):
        _MANAGER_LOGGER.addHandler(self.stream_handler())
        _MANAGER_LOGGER.setLevel(logging.INFO)

        self.ROOT_NAME = app_name
        self.FALLBACK_LEVEL = log_level
        if log_format:
            self.LOG_FORMAT = log_format
        if module_to_level:
            self._moduleToLevel = {**self._moduleToLevel, **module_to_level}

        self.BASE_LOGGER = self._init_base_logger()
        for module in self._moduleToLevel:
            self._init_new_logger(module)

    def _reset_logger_level(self, logger_name: str, logger: logging.Logger):
        if logger_name in self._moduleToLevel:
            logger.setLevel(self._moduleToLevel[logger_name])
        else:
            logger.setLevel(self.BASE_LOGGER.level)

    def _init_base_logger(self):
        logger = logging.getLogger(self.ROOT_NAME)
        logger.addHandler(self.stream_handler())
        logger.setLevel(self.FALLBACK_LEVEL)
        return logger

    def _init_new_logger(self, module_name: str):
        logger = logging.getLogger(module_name)
        self._reset_logger_level(module_name, logger)
        if not module_name.startswith(self.BASE_LOGGER.name):
            logger.addHandler(self.stream_handler())
        self._loggers[module_name] = logger
        return logger

    def formatter(self):
        return logging.Formatter(self.LOG_FORMAT)

    def stream_handler(self):
        handler = logging.StreamHandler()
        handler.setFormatter(self.formatter())
        return handler

    def set_level(self, module_name: str, level: str):
        if module_name not in self._loggers:
            raise UndefinedLoggerException(f'Logger with  name {module_name!r} is not defined')
        self._moduleToLevel[module_name] = level
        self._reset_logger_level(module_name, self._loggers[module_name])

    def set_base_level(self, level: str = None):
        if not level:
            level = self.FALLBACK_LEVEL
        self.BASE_LOGGER.setLevel(level)
        _MANAGER_LOGGER.info(f'Base log level set to {level!r}')
        for k, v in self._loggers.items():
            self._reset_logger_level(k, v)

    def get_logger(self, module_name: str = None):
        if not module_name:
            return self.BASE_LOGGER
        if module_name in self._loggers:
            return self._loggers.get(module_name)
        return self._init_new_logger(module_name)


build_config()

external = {
    'aiohttp.client': storage.config.log_level,
    'aiohttp.server': storage.config.log_level,
    'aiohttp.web': storage.config.log_level,
}

log_manager = LogManager('api_smart_link', storage.config.log_level, module_to_level=external)
