import argparse


class CmdOption:
    name = ''
    option = ''
    aliases = []
    value = None
    required = False
    description = ''

    def __init__(self, name, option, aliases=None, required=False):
        self.name = name
        self.option = option
        if aliases is not None:
            self.aliases = aliases
        self.required = required


class CmdOptions:
    options = {}

    def add_option(self, name, option, aliases=None, required=False):
        option = CmdOption(name, option, aliases, required)
        self.options[option.name] = option

    def read(self):
        parser = argparse.ArgumentParser()
        for key in self.options:
            option = self.options[key]
            if option.aliases:
                aliases = ' '.join(option.aliases)
                parser.add_argument(option.option, aliases, action='store', required=option.required,
                                    help=option.description)
            else:
                parser.add_argument(option.option, action='store', required=option.required, help=option.description)
        args = parser.parse_args()
        for key in self.options:
            if args[key]:
                self.options[key].value = args[key]

    def read_static(self, cmd):
        parser = argparse.ArgumentParser()
        for key in self.options:
            option = self.options[key]
            if option.aliases:
                aliases = ' '.join(option.aliases)
                parser.add_argument(option.option, aliases, required=option.required, help=option.description)
            else:
                parser.add_argument(option.option, required=option.required, help=option.description)
        args = parser.parse_args(cmd)
        for key in self.options:
            if args[key]:
                self.options[key].value = args[key]
