import sys
import os
from .cmd import Cmd


class RunCmd(Cmd):
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
        sys.path.append(self.pkg)
        if len(self.files) == 0:
            import pkg
            if pkg.DEFAULT_FILE:
                os.system(f"{sys.executable} {pkg.DEFAULT_FILE}")
            else:
                print("the DEFAULT_FILE variable is empty")
        else:
            _file = os.path.abspath(self.files)
            import pkg

            if _file in pkg.LIST_FILE:
                os.system(f"{sys.executable} {_file}")
            else:
                print("the file must be in LIST_FILE")



