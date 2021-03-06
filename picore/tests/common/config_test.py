import unittest

import os

import pir2.common.Config as Config
import pir2.common.Logger as Logger
import pir2.common as common


class ConfigTestCase(unittest.TestCase):
    CONST_CONFIG_FILE = '../resources/config_test.ini'
    __log = Logger.Logger()

    @classmethod
    def setUp(cls) -> None:
        wd = os.getcwd()
        print('Working Directory = [' + wd + ']')
        cf = wd + '/../resources/core.ini'
        common.init(cf)

    def test_config_load(self):
        config = Config.Config(self.CONST_CONFIG_FILE)
        section = config.get('wiki')
        self.assertIsNotNone(section)

        self.__log.info('Section [' + str(section).strip('[]') + ']')
        url = config.get_option('wiki', 'url')
        self.assertIsNotNone(url)
        self.__log.info('URL = [' + url + ']')
        vn = config.get_option('dummy', 'dummy')
        self.assertIsNone(vn)


if __name__ == '__main__':
    unittest.main()
