import os
from command.base_cmd import BaseCommand 
from files.tree_ast import make_source_from_ast, make_tree_ast, append_list_ast, transform_elt_iter_to_type_ast
from files.file import list_to_list_abspath

class AddCommand(BaseCommand):
    name = 'add'
    help = "add file to LIST_FILE"
    option = [{
        "name": ("-p", "--pkg"),
        "option": {
            "type": str,
            "help": "the pkg.py path",

        }
    }]

    arguments = [{
        "name": "files",
        "option": {
            "type": str,
            "required": False,
            "nargs": -1
        }
    }]

    def main(self):
        path = self.pkg if self.pkg else os.path.join(os.getcwd(), 'pkg.py')
        list_file = list_to_list_abspath(self.files)
        with open(path) as pkg_reader:
            content = pkg_reader.read()

        tree = make_tree_ast(content)

        append_list_ast(tree, "LIST_FILE", transform_elt_iter_to_type_ast(list_file))

        with open(path, 'w') as pkg_writer:
            pkg_writer.write(make_source_from_ast(tree))

        print('multiple file added to LIST_FILE: ', ' '.join(list_file))