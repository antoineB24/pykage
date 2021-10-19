from command.base_cmd import BaseCommand
from install_pack.install import install_and_add_to_pkg, install_from_pkg
import os

class InstallCommand(BaseCommand):
    name = "install"
    help = "install depensie of pkg.py or install depensie of you takes"
    option = [{
        "name": ('-p', '--pkg'),
        "option": {
            "required": False
        }
    }]

    arguments = [{
        "name": "mod",
        "option": {
            "nargs": -1
        }
    }]

    def main(self):
        mod = self.mod
        path_pkg = self.pkg if self.pkg else os.getcwd()
        if len(mod):
            install_and_add_to_pkg(path_pkg, mod)
        else:
            install_from_pkg(path_pkg)