
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

def init_cmd():
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
            (v != '') and
            (not v[0].isdigit()) and
            (all([i in 'azertyuiopqsdfghjklmwxcvbn1234567890' for i in v]))
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
    git_repostery = validate(
        'git repostery',
        lambda v: re.match(REGEX_GIT_PROJECT, v),
        'optionel',
        git_repostery
    )

    contenue = f'''
    AUTHOR = {author}
    PKG_NAME = {name_project}
    VERSION = {version}
    EMAIL = {email}
    MAIN_FILE = {main_file}
    PACKAGE = []
    DESCRIPTION = {description}
    GIT_REPO = {git_repostery}
    '''

    print("\n\n")
    print(contenue)
    if not input("is OK ? ").startwith('y'):
        init_cmd()
    else:
        os.system('touch pkg.py')
    file = open('pkg.py', 'w')
    file.write(contenue)
    file.close()
