import sys
import os
sys.path.append(os.path.abspath('.'))
from utils.errors import PKGNotFound  # pkg error when file pkg.py not found
from utils.api import install_module, install_multiple_module
import utils.tree_ast as tree_ast
import ast


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

    if len(pkg_list) > 1:
        install_multiple_module('packagespy', *pkg_list)
    else:
        install_module(pkg_list[0], 'packagespy')

    tree_ast.append_list_ast(tree, "PACKAGE", tree_ast.transform_elt_iter_to_type_ast(pkg_list))

    with open(f'{path_pkg}/pkg.py', 'w') as pkg_w:
        pkg_w.write(tree_ast.make_source_from_ast(tree))


if __name__ == '__main__':
    with open('pkg.py') as p:
        body = p.read()
    tree = tree_ast.make_tree_ast(body)

    tree_ast.append_list_ast(tree, "PACKAGE", [ast.Num(6), ast.Num(6)])
    print(tree_ast.make_source_from_ast(tree))
