
# init_cmd : the code that will run when pykg init
# re.match : verifies that the regex is valid at the given string
# regex : python module with regex utils
#   path: pykg/utils/regex.py
# input_conf : python module based on input
#   path: pykg/utils/input_conf.py
# input_conf.validate : see file pykg/utils/input_conf.py


import re
import os
from utils.regex import (
 REGEX_FILE_PY,
 REGEX_VERSION_NUMBER,
 REGEX_EMAIL,
 REGEX_GIT_PROJECT
)
from utils.input_conf import validate

def init_cmd(path):
    print('pykg init... \n')
    print('configuration : \n\n ')

    author = input('Author(optionel): ')
    email = input('Email(optionel): ')
    if email:
        email = validate(
            'Email',
            lambda v: re.match(REGEX_EMAIL, v),
            'optionel',
            email
        )
    name_project = input('your project name: ')
    name_project = validate(
        'you project name',
        lambda v: (
            bool(v) and not v[0].isdigit() 
        ),
        'required',
        name_project
    )

    version = input('version (default=1.0.0): ')
    if version:
        version = validate(
            'version',
            lambda v: re.match(REGEX_VERSION_NUMBER, v),
            'default=1.0.0',
            version
        )
    else:
        version = '1.0.0'

    main_file = input('main file (optionel): ')
    if main_file:
        main_file = validate(
            'main file',
            lambda v: re.match(REGEX_FILE_PY, v),
            'optionel',
            main_file
        )

    description = input("descriptions(optionel): ")
    git_repostery = input('git ripostery(optionel): ')
    if git_repostery:
        git_repostery = validate(
            'git repostery',
            lambda v: re.match(REGEX_GIT_PROJECT, v),
            'optionel',
            git_repostery
        )

    contenue = f'''
AUTHOR = '{author}'
PKG_NAME = '{name_project}'
VERSION = '{version}'
EMAIL = '{email}'
DEFAULT_FILE = '{main_file}'
PACKAGE = []
LIST_FILE = []
DESCRIPTION = '{description}'
GIT_REPO = '{git_repostery}'
PWD = '{os.path.abspath(path)}'  '''

    print("\n\n")
    print(contenue)
    if not input("is OK ? ").startswith('y'):
        init_cmd(path)
    else:
        os.system(f'touch {path}/pkg.py')
    file = open(f'{path}/pkg.py', 'w')
    file.write(contenue)
    file.close()
