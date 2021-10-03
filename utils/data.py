import sys
import os


TIME_API_GET_SRC_MODULE = 49.047829816000004


def get_pkg_path():
    if os.path.exists(os.path.join(os.getcwd(), "pkg.py")):
        pkg_path = os.getcwd()
    else:
        try:
            os.environ["PKG_PATH"]
        except KeyError:
            print("define a var env PKG_PACK to the absolute path of pkg.py")
            sys.exit(1)
        else:
            pkg_path = os.environ["PKG_PATH"]
    return pkg_path
