import logging
import picore.common as common


class Logger:
    name = ''

    def __init__(self):
        name = common.__DEFAULT_LOGGER_NAME__

    def error(self, error):
        __logger = common.get_logger()
        if not __logger:
            print(error)
            return
        __logger.error(error)

        if isinstance(error, Exception):
            if __logger.isEnabledFor(logging.DEBUG):
                __logger.exception(error)

    def warn(self, mesg):
        __logger = common.get_logger()
        if not __logger:
            print(mesg)
            return

        __logger.warning(mesg)

    def info(self, mesg):
        __logger = common.get_logger()
        if not __logger:
            print(mesg)
            return
        __logger.info(mesg)

    def debug(self, mesg):
        __logger = common.get_logger()
        if not __logger:
            print(mesg)
            return
        __logger.debug(mesg)
