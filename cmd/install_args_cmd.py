import sys
import os
from utils.errors import PKGNotFound  # pkg error when file pkg.py not found
from utils.system import install_packages
import utils.tree_ast as tree_ast
import ast

sys.path.append(os.path.abspath('.'))


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
        with open(f'{path_pkg}/pkg.py') as pkg_r:
            body = pkg_r.read()
    except FileNotFoundError:
        raise PKGNotFound(f"pkg file not found ({path_pkg}/pkg.py)")
    else:
        tree = tree_ast.make_tree_ast(body)

    install_packages(pkg_list)

    tree_ast.append_list_ast(tree, "PACKAGE", tree_ast.transform_elt_iter_to_type_ast(pkg_list))

    with open(f'{path_pkg}/pkg.py', 'w') as pkg_w:
        pkg_w.write(tree_ast.make_source_from_ast(tree))
