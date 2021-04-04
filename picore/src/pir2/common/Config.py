import configparser
import os.path


class Config:
    filename = ""
    parser = None

    def __init__(self, filename):
        if filename:
            self.filename = filename
            self.load()
        else:
            raise Exception('No configuration file specified.')

    def load(self):
        if not os.path.isfile(self.filename):
            raise Exception('File not found : path=' + self.filename)

        self.parser = configparser.SafeConfigParser()
        self.parser.read(self.filename)

    def get(self, section):
        if not self.parser:
            raise Exception('Parser not initialized')
        if self.parser.has_section(section):
            return self.parser.items(section)
        return None

    def get_option(self, section, option):
        if not self.parser:
            raise Exception('Parser not initialized')
        if self.parser.has_section(section):
            if self.parser.has_option(section, option):
                return self.parser.get(section, option)
        return None
