from command.base_cmd import BaseCommand
from files.file import PyFile
import sys

class RunCommand(BaseCommand):
    name = "run"
    help = "execute the python default file given in pkg.py or execute file given in LIST_FILE"
    option = [{
        "name": ("-p", "--pkg"),
        "option": {
            "type": str,
            "help": "the pkg.py path"
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
        path_pkg = self.pkg
        sys.path.append(path_pkg)
        if len(files) == 0:
            import pkg 
            if pkg.DEFAULT_FILE:
                PyFile(pkg.DEFAULT_FILE).run()
        else:
            import pkg
            for f in files:
                if f in pkg.LIST_FILE:
                    PyFile(f).run()
                else:
                    print(f"{f} must be in LIST_FILE")
                

