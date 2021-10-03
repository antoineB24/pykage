from utils.system import install_packages # see pykg/utils/system.py
from utils.type_help import Path, Vector, Any # see pykg/utils/type_help.py
from utils.errors import PKGNotFound # pkg error when file pkg.py not found
# import sys # for sys.path


def install_args_cmd(path_pkg : Path, pkg_list : Vector) -> Any:
    """
    install all the given packages and add the expenses to pkg.py
    --------------------------------------------------------------
    path_pkg : Path
    the path of pkg.py

    pkg_list : Vector
    the list of packages to be installed
    """
    
    try:
        with open(f'{path_pkg}/pkg.py') as pkg:
            body = pkg.read()
    except FileNotFoundError:
        raise PKGNotFound(f"pkg file not found ({path_pkg}/pkg.py)")
    else:
        print(body)



    install_packages(pkg_list)
