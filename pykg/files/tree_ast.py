import ast
import codegen
from errors.errors_ast import InvalidTypeAst


def get_type_from_ast_type(ast_var):
    return type(ast_var.value)


def find_var_ast(tree, element):
    for i in tree.body:
        if i.targets[0].id == element:
            return i


def make_tree_ast(code):
    return ast.parse(code)


def make_source_from_ast(tree):
    return codegen.to_source(tree)


def set_var_ast(tree, name_var, value_var):
    ass = find_var_ast(tree, name_var)
    if type(ass.value) is ast.List:
        ass.value.elts = value_var
    elif type(ass.value) is ast.Constant:
        ass.value.s = value_var
    elif type(ass.value) is ast.Num:
        ass.value.n = value_var
    else:
        raise InvalidTypeAst("invalid type ast")


def append_list_ast(tree, name_var, e):
    v1 = get_var_ast(tree, name_var)
    if type(v1) != ast.List:
        raise InvalidTypeAst("not valid type: %s" % type(v1).__name__)

    set_var_ast(tree, name_var, [*v1.elts, *e])


def get_var_ast(tree, name_var):
    return find_var_ast(tree, name_var).value


def transform_num_to_ast_num(n):
    if type(n) != int:
        raise TypeError("not type int: %s", type(n).__name__)

    return ast.Num(n)


def transform_string_to_ast_string(s):
    if type(s) != str:
        raise TypeError("not type str: %s", type(s).__name__)

    return ast.Str(s)


def transform_elt_iter_to_type_ast(iterable):
    if type(iterable) not in (list, tuple, set):
        raise TypeError("invalid type iterable(list, tuple, set):  %s", type(iterable).__name__)

    new_iter = []
    for i in iterable:
        if type(i) == int:
            new_iter.append(transform_num_to_ast_num(i))
        elif type(i) == str:
            new_iter.append(transform_string_to_ast_string(i))
        else:
            raise TypeError("unknown type")
    return new_iter