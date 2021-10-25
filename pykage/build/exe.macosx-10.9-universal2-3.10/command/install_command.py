import os
from packaging.requirements import Requirement
from command.base_cmd import BaseCommand
from packages.package import Package
from files.toml_parse import PyProject

class InstallCommand(BaseCommand):
    name = "install"
    help = "install depensie of pkg.py or install depensie of you takes"
    option = [{
        "name": ('-p', '--pyproject'),
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
        path_pyproject = self.pyproject if self.pyproject else os.getcwd()
        pyproject = PyProject(path_pyproject, True)

        

        if len(mod):
            
            list_package = {Requirement(i).name: str(Requirement(i).specifier) for i in mod}
            for i in mod:
                mod_requirement = Requirement(i)
                pyproject.set_var_package(mod_requirement.name, str(mod_requirement.specifier) if str(mod_requirement.specifier) else "latest")
                pyproject.save()
        else:
            list_package = pyproject.get_package_group()

            

        for i in list_package:
            p = Package(i, list_package[i])
            p.install_module(dest="pypack")