import os
from console.input_conf import (InputStyle,
 ValidateEmail,
  ValidateFilePy,
   ValidateGit,
    ValidateOptionel,
     ValidateRequired,
      ValidateVersion)
from data.conversion import dict_to_namedtuple
import toml

def init_toml(path):
    print('pykg init... \n')
    print('configuration : \n\n ')

    form = Form()
    dict_ = form.render()
    if bool(dict_):
        struct = dict_to_namedtuple(dict_)
        content = f'''
[pykg.project]
name = '{struct.project_name}'
version = '{struct.version}'
email = '{struct.email}'
description = '{struct.description}'
git_repostery = '{struct.git_repo}'
pwd = '{os.path.abspath(path)}'
[pykg.package]
[pykg.file]
default_file = '{struct.main_file}'
list_file = []
'''

        print("\n\n")
        print(content)
        ok = Ok()
        res = ok.render()
        if res:
            if res['ok'] == 'No':
                init_toml(path)
            else:
                os.system(f'touch {path}/pkg.toml')
            file = open(f'{path}/pkg.toml', 'w')
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
