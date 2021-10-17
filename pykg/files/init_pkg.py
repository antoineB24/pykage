import os
from console.input_conf import (InputStyle,
 ValidateEmail,
  ValidateFilePy,
   ValidateGit,
    ValidateOptionel,
     ValidateRequired,
      ValidateVersion)
from data.conversion import dict_to_namedtuple

def init_pkg(path):
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
                init_pkg(path)
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
