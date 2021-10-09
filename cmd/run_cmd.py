import sys
import os


def run_cmd(path_pkg):
    sys.path.append(path_pkg)
    import pkg
    if pkg.DEFAULT_FILE:
        os.system(f"{sys.executable} {pkg.DEFAULT_FILE}")
    else:
        print("the DEFAULT_FILE variable is empty")
