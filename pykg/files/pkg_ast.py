from .tree_ast import append_list_ast, get_var_ast, make_source_from_ast, make_tree_ast, set_var_ast, transform_elt_iter_to_type_ast
from errors.errors_pack import PKGNotFound
from pathlib import Path

class PKG:
    def __init__(self, pkg, read_only=False) -> None:
        self._pkg = Path(pkg) / "pkg.py"
        if not self._pkg.exists():
            raise PKGNotFound("pkg not found")
        self._read_only = read_only
        pkg_reader = open(str(self._pkg))
        self._asm = make_tree_ast(pkg_reader.read())
        self._source = pkg_reader.read()
        pkg_reader.close()
    
    def get_source(self):
        return self._source
    
    def get_tree_ast(self):
        return self._asm
    
    def get_pkg_path(self):
        return self._pkg
    
    def append_list_package(self, *string: list[str]) -> None:
        append_list_ast(self._asm, "PACKAGE", transform_elt_iter_to_type_ast(string))
    
    def get_list_package(self):
        return get_var_ast(self._asm, "PACKAGE")

    def save(self):
        with open(self._pkg, "w") as pkg:
            pkg.write(make_source_from_ast(self._asm))
    


    