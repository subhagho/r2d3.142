import configparser
import logging
import logging.config

__CONFIG_SECTION_FILES__ = 'CONFIGS'
__CONFIG_SECTION_DEFAULT__ = 'DEFAULT'
__CONFIG_DEFAULT_KEY_LOGCONFIG__ = 'logger.config'
__DEFAULT_LOGGER_NAME__ = 'picore'

from picore import common

sys_config_parser = configparser.ConfigParser()
__configs = {}


def init():
    sys_config_parser.read('core.ini')
    if sys_config_parser.has_section(__CONFIG_SECTION_FILES__):
        values = sys_config_parser.items(__CONFIG_SECTION_FILES__)
        for key, value in values:
            read_config(key, value)

    if sys_config_parser.has_section(__CONFIG_SECTION_DEFAULT__):
        init_logger()


def init_logger():
    if sys_config_parser.has_option(__CONFIG_SECTION_DEFAULT__, __CONFIG_DEFAULT_KEY_LOGCONFIG__):
        log_config = sys_config_parser.get(__CONFIG_SECTION_DEFAULT__, __CONFIG_DEFAULT_KEY_LOGCONFIG__)
        if log_config:
            logging.config.fileConfig(log_config)
            __logger = logging.getLogger(__DEFAULT_LOGGER_NAME__)


def read_config(name, file):
    config = common.Config(file)
    __configs[name] = config


def get_config(name):
    return __configs[name]


def get_logger():
    return logging.getLogger(__DEFAULT_LOGGER_NAME__)

