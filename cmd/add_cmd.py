import sys
import os
from utils.tree_ast import make_tree_ast, transform_elt_iter_to_type_ast, append_list_ast, make_source_from_ast
from utils.system import list_to_list_abspath

def add_cmd(path, list_file):
    list_file = list_to_list_abspath(list_file)
    with open(path) as pkg_reader:
        content = pkg_reader.read()

    tree = make_tree_ast(content)

    append_list_ast(tree, "LIST_FILE", transform_elt_iter_to_type_ast(list_file))

    with open(path, 'w') as pkg_writer:
        pkg_writer.write(make_source_from_ast(tree))

    print('multiple file added to LIST_FILE: ', ' '.join(list_file))



