import sys
import os
from utils.system import install_packages
from .cmd import Cmd


class InstallCmd(Cmd):

    def main(self, path_pkg):
        sys.path.append(path_pkg)
        import pkg

        try:
            pkg.PACKAGE
            assert type(pkg.PACKAGE) == list
        except NameError:
            print("Error: the pkg.py is not valid")
        except AssertionError:
            print("PACKAGE do is a list")
        else:
            install_packages(pkg.PACKAGE)


def install_cmd(path_pkg):
    sys.path.append(path_pkg)
    import pkg

    try:
        pkg.PACKAGE
        assert type(pkg.PACKAGE) == list
    except NameError:
        print("Error: the pkg.py is not valid")
    except AssertionError:
        print("PACKAGE do is a list")
    else:
        install_packages(pkg.PACKAGE)
