import os
from command.base_cmd import BaseCommand
from files.pkg_ast import PKG
from install_pack.install import Package

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
        pkg = PKG(path_pkg)

        if len(mod):
            list_package = mod
            pkg.append_list_package(*mod)
            pkg.save()
        else:
            list_package = pkg.get_list_package()

        for i in list_package:
            p = Package(i)
            p.install_module(dest="pypack")