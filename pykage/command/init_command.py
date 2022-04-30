from command.base_cmd import BaseCommand
from files.init_toml import init_toml
import pathlib

class InitCommand(BaseCommand):

    name = 'init'
    help = 'create a pkg.py with info'
    arguments = [{
        "name": "path_pkg",
        "option": {
            "required": False,
            "default": None
        }
    }]

    def main(self):
        path = self.path_pkg if bool(self.path_pkg) else pathlib.Path().resolve()
        init_toml(path)
