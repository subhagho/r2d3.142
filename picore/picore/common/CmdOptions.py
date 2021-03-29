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

    def add_option(self, name, option, aliases=None, required=False, description=None):
        option = CmdOption(name, option, aliases, required)
        if description:
            option.description = description

        self.options[option.name] = option

    def get_option(self, name):
        if name in self.options:
            return self.options[name]
        return None

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
        args_ns = parser.parse_args()
        args = vars(args_ns)
        self.read_options(args)

    def read_static(self, cmd):
        parser = argparse.ArgumentParser()
        for key in self.options:
            option = self.options[key]
            if option.aliases:
                aliases = ' '.join(option.aliases)
                parser.add_argument(option.option, aliases, required=option.required, help=option.description)
            else:
                parser.add_argument(option.option, required=option.required, help=option.description)
        args_ns = parser.parse_args(cmd)
        args = vars(args_ns)
        self.read_options(args)

    def read_options(self, args):
        for key in self.options:
            option = self.options[key]
            k = None
            kk = option.option.replace('-', '')
            if kk in args:
                k = kk
            if not k and option.aliases:
                for ok in option.aliases:
                    kk = ok.replace('-', '')
                    if kk in args:
                        k = kk
                        break
            if k:
                self.options[key].value = args[k]