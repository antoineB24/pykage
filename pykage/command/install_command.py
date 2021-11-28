import os
from packaging.requirements import Requirement
from command.base_cmd import BaseCommand
from packages.package import Package
from files.toml_parse import PyProject
from regex.data_re import is_valid_git_project, is_valid_url

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
        mod : tuple = self.mod
        path_pyproject = self.pyproject if self.pyproject else os.getcwd()
        pyproject = PyProject(path_pyproject, True)

        if len(mod):
            list_package = mod
            for p in range(len(mod)):
                if not (is_valid_url(mod[p]) or is_valid_git_project(mod[p])):
                    mod_requirement = Requirement(mod[p])
                    pyproject.set_var_package(mod_requirement.name, str(mod_requirement.specifier) if str(mod_requirement.specifier) else "latest")
                    pyproject.save()
                else:
                    pyproject.set_var_package(mod[p], mod[p])
                    pyproject.save()

        else:
            list_package = pyproject.get_package_group()

            
        print(list_package)
        for i in list_package:
            if is_valid_url(i) or is_valid_git_project(i):
                p = Package(i)
            else:
                p = Package(i, list_package[i])
            p.install_module(dest="pypack")
