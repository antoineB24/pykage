
from utils.errors import PKGNotFound # pkg error when file pkg.py not found
from utils.api import install_module, install_multiple_module
import sys # for sys.path



def install_args_cmd(path_pkg, pkg_list):
    """
    install all the given packages and add the expenses to pkg.py
    --------------------------------------------------------------
    path_pkg : str
    the path of pkg.py

    pkg_list : list
    the list of packages to be installed
    """
    
    try:
        with open(f'{path_pkg}/pkg.py') as pkg:
            body = pkg.read()
    except FileNotFoundError:
        raise PKGNotFound(f"pkg file not found ({path_pkg}/pkg.py)")
    else:
        print(body)

    if len(pkg_list) > 1:
        install_multiple_module('packagespy', *pkg_list)
    else:
        install_module(pkg_list[0], 'packagespy')

