# init_cmd : the code that will run when pykg init
# re.match : verifies that the regex is valid at the given string
# regex : python module with regex utils
#   path: pykg/utils/regex.py
# input_conf : python module based on input
#   path: pykg/utils/input_conf.py
# input_conf.validate : see file pykg/utils/input_conf.py


import os
from utils.input_conf import InputStyle
from utils.input_conf import (ValidateRequired, ValidateOptionel,
                              ValidateEmail, ValidateGit,
                              ValidateVersion, ValidateFilePy)
from utils.data import dict_to_namedtuple
from .cmd import Cmd


class InitCmd(Cmd):

    name = 'init'
    help = 'create a pkg.py with info'
    arguments = [{
        "name": "path_pkg",
        "option": {
            "required": False,
            "default": None
        }
    }]

    def main(self):
        path = self.path_pkg if bool(self.path_pkg) else os.getcwd()
        print('pykg init... \n')
        print('configuration : \n\n ')

        form = Form()
        dict_ = form.render()
        if bool(dict_):
            struct = dict_to_namedtuple(dict_)
            content = f'''
                AUTHOR = '{struct.author}'
                PKG_NAME = '{struct.project_name}'
                VERSION = '{struct.version}'
                EMAIL = '{struct.email}'
                DEFAULT_FILE = '{struct.main_file}'
                PACKAGE = []
                LIST_FILE = []
                DESCRIPTION = '{struct.description}'
                GIT_REPO = '{struct.git_repo}'
                PWD = '{os.path.abspath(path)}'  '''

            print("\n\n")
            print(content)
            ok = Ok()
            res = ok.render()
            if res:
                if res['ok'] == 'No':
                    init_cmd(path)
                else:
                    os.system(f'touch {path}/pkg.py')
                file = open(f'{path}/pkg.py', 'w')
                file.write(content)
                file.close()


class Form(InputStyle):
    form = [
        {
            'type': 'input',
            'name': 'author',
            'message': 'Author(optionel): ',
            'validator': ValidateOptionel

        },
        {
            'type': 'input',
            'name': 'email',
            'message': 'Email(optionel): ',
            'validator': ValidateEmail
        },
        {
            'type': 'input',
            'name': 'project_name',
            'message': 'your project name: ',
            'validator': ValidateRequired
        },
        {
            'type': 'input',
            'name': 'version',
            'message': 'Version(optionel): ',
            'validator': ValidateVersion,
            'default': '1.0.0'
        },
        {
            'type': 'input',
            'name': 'main_file',
            'message': 'Main File(optionel): ',
            'validator': ValidateFilePy
        },
        {
            'type': 'input',
            'name': 'description',
            'message': 'description: ',
        },
        {
            'type': 'input',
            'name': 'git_repo',
            'message': 'Git Repo(optionel)',
            'validator': ValidateGit
        }
    ]


class Ok(InputStyle):
    form = [{
        'type': 'list',
        'name': 'ok',
        'message': 'is ok',
        'choices': [
            {'name': 'Yes'},
            {'name': 'No'}
        ]
    }]

