from argparse import ArgumentParser


class Cmd:
    name = ''
    help = ""

    def __init__(self, argparse: ArgumentParser, **kwargs):
        self.argparse = argparse
        self.cmd = False
        self.data = kwargs
        self.parser = self.parse()

    def make_parser(self):
        self.argparse.add_argument(self.name, help=self.help)

    def parse(self):
        return self.argparse.parse_args()

    def run(self):
        parser = self.parse()
        if parser.cmd[0] == self.name:
            self.main(*parser.cmd[1:])
