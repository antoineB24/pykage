from command.base_cmd import BaseCommand
from files.file import PyFile
from files.toml_parse import PyProject
from pathlib import Path
import sys

class RunCommand(BaseCommand):
    name = "run"
    help = "execute the python default file given in pkg.py or execute file given in LIST_FILE"
    option = [{
        "name": ("-p", "--pkg"),
        "option": {
            "type": str,
            "help": "the  path"
        }
    }]
    arguments = [{
        "name": "files",
        "option": {
            "type": str,
            "required": False,
            "nargs": -1
        }
    }]

    def main(self):
        files = self.files 
        path_pkg = self.pkg if self.pkg else "."
        pyproject = PyProject(path_pkg, True)
        if len(files) == 0:
            if pyproject.get_var_file("default_file"):
                PyFile(pyproject.get_var_file("default_file")).run()
        else:
            for f in [Path(i).absolute() for i in files]:
                PyFile(f).run()
                

