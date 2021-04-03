import configparser
import logging
import logging.config
import os.path as path
import picore.common.CmdOptions as options
import picore.common.Config as cfg

__CONFIG_SECTION_FILES__ = 'CONFIGS'
__CONFIG_SECTION_DEFAULT__ = 'CORE'
__CONFIG_DEFAULT_KEY_LOG_CONFIG__ = 'logger.config'
__DEFAULT_LOGGER_NAME__ = 'picore'

sys_config_parser = configparser.ConfigParser()
__configs = {}
cmd_options = options.CmdOptions()


def init(config=None):
    cf = None

    if not config:
        global cmd_options
        cmd_options.add_option('config', '-c', ['--config'])
        cmd_options.read()
        co = cmd_options.get_option('config')
        if not co:
            cf = 'core.ini'
        else:
            cf = co.value
            if cf and not path.isfile(cf):
                raise Exception('Invalid configuration file specified. [path=' + str(cf) + ']')

    else:
        cf = config
        if not path.isfile(config):
            raise Exception('Invalid configuration file specified. [path=' + str(cf) + ']')

    if cf and path.isfile(cf):
        sys_config_parser.read(cf)
        if sys_config_parser.has_section(__CONFIG_SECTION_FILES__):
            values = sys_config_parser.items(__CONFIG_SECTION_FILES__)
            for key, value in values:
                read_config(key, value)

        if sys_config_parser.has_section(__CONFIG_SECTION_DEFAULT__):
            init_logger()


def init_logger():
    if sys_config_parser.has_option(__CONFIG_SECTION_DEFAULT__, __CONFIG_DEFAULT_KEY_LOG_CONFIG__):
        log_config = sys_config_parser.get(__CONFIG_SECTION_DEFAULT__, __CONFIG_DEFAULT_KEY_LOG_CONFIG__)
        if log_config:
            if not path.isfile(log_config):
                raise Exception('Logging configuration file not found. [path=' + log_config + ']')

            logging.config.fileConfig(log_config)
            __logger = logging.getLogger(__DEFAULT_LOGGER_NAME__)


def read_config(name, file):
    config = cfg.Config(file)
    __configs[name] = config


def get_config(name):
    if name in __configs:
        return __configs[name]
    return None


def get_logger():
    return logging.getLogger(__DEFAULT_LOGGER_NAME__)
