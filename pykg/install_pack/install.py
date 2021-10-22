import sys
import os, sh
from errors.errors_pack import PKGNotFound
import files.tree_ast as tree_ast
from files.file import touch_if_no_exists
import pkg_resources
from pkg_resources import DistributionNotFound, VersionConflict
import subprocess
import pickle



def install_and_add_to_pkg(path_pkg, mod):
    from .api import install_package, install_multiple_package
    try:
        with open(f'{path_pkg}/pkg.py') as pkg_r:
            body = pkg_r.read()
    except FileNotFoundError:
        raise PKGNotFound(f"pkg file not found ({path_pkg}/pkg.py)")
    else:
        tree = tree_ast.make_tree_ast(body)
    # sh.mkdir("pypack")
    if len(mod) == 1:
        install_package(mod[0], dest="pypack")
    else:
        install_multiple_package(*mod, dest="pypack")

    tree_ast.append_list_ast(tree, "PACKAGE", tree_ast.transform_elt_iter_to_type_ast(mod))

    with open(f'{path_pkg}/pkg.py', 'w') as pkg_w:
        pkg_w.write(tree_ast.make_source_from_ast(tree))

def install_from_pkg(pkg_path):
    from .api import install_package, install_multiple_package
    sys.path.append(pkg_path)
    try:
        import pkg
    except ImportError:
        raise PKGNotFound("pkg.py not found")
    else:
        import pkg

    try:
        pkg.PACKAGE
        assert type(pkg.PACKAGE) == list
    except NameError:
        print("Error: the pkg.py is not valid")
    except AssertionError:
        print("PACKAGE do is a list")
    else:
        install_multiple_package(pkg.PACKAGE)




def install_packages(requirement_list):
    
    requirements = [
        requirement
        for requirement in requirement_list
        if is_install(requirement)
    ]
    if len(requirements) > 0:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-t", "pypackages/", *requirements])
    else:
        print("Requirements already satisfied.")

    reader = open('pypackages/lpkg.lock', 'rb')
    list_m = pickle.load(reader)
    reader.close()

    with open('pypackages/lpkg.lock', 'wb') as w1:
        pickle.dump(list_m + requirement_list, w1)
