import sys
import os


def run_args_cmd(path_pkg, file):
    _file = os.path.abspath(file)
    sys.path.append(path_pkg)
    import pkg

    if _file in pkg.LIST_FILE:
        os.system(f"{sys.executable} _file")
    else:
        print("the file must be in LIST_FILE")
