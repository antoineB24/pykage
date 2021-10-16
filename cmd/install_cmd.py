import sys
import os
from utils.system import install_packages
from utils.errors import PKGNotFound
import utils.tree_ast as tree_ast
from .cmd import Cmd


class InstallCmd(Cmd):
    name = "install"
    help = "install depensie of pkg.py or install depensie of you takes"
    option = [{
        "name": ('-p', '--pkg'),
        "option": {
            "required": False
        }
    }]

    arguments = [{
        "name": "mod",
        "option": {
            "nargs": -1
        }
    }]

    def main(self):
        mod = self.mod
        path_pkg = self.pkg
        sys.path.append(path_pkg)
        if len(mod) == 0:
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
        else:
            try:
                with open(f'{path_pkg}/pkg.py') as pkg_r:
                    body = pkg_r.read()
            except FileNotFoundError:
                raise PKGNotFound(f"pkg file not found ({path_pkg}/pkg.py)")
            else:
                tree = tree_ast.make_tree_ast(body)

            install_packages(mod)

            tree_ast.append_list_ast(tree, "PACKAGE", tree_ast.transform_elt_iter_to_type_ast(mod))

            with open(f'{path_pkg}/pkg.py', 'w') as pkg_w:
                pkg_w.write(tree_ast.make_source_from_ast(tree))



