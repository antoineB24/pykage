from cmd.init_cmd import init_cmd
from cmd.install_cmd import install_cmd
from utils.regex import *
import os
import argparse
import sys

parser = argparse.ArgumentParser(prog='pykg')
parser.add_argument('cmd', help='votre cmd', nargs='+')
parser.add_argument('-pa', '--path', help='path', action="store_true")
args = parser.parse_args()

if args.cmd[0] == 'help':
    print("""
usage: main.py  cmd 

list cmd:
  init              create a pkg.py
  install           installs the dependenses of pkg.py
  install lib       install with pip and add as expense name_of_module in pkg.py
  run               execute the python file given in pkg.py (DEFAULT_FILE)
  run file          execute the python file in pkg.py (LIST_FILE)
  add file          add file to pkg.py (LIST_FILE)
  settings var val  add/modify a setting in pkg.py
  remove file       removes a file in pkg.py (LIST_FILE)
  env name_env      create an environment with the expenses installed in pkg.py
  activate          activates the env if the env exists
  deactivate        deactivates the env if it is activated



optional arguments:
  -h, --help  show this help message and exit
  """)

elif args.cmd[0] == "init":
    path = args.cmd[1] if len(args.cmd) - 1 else os.getcwd()
    init_cmd(path)
elif args.cmd[0] == "install" and len(args.cmd) == 1:
    if os.path.exists(os.path.join(os.getcwd(), "pkg.py")):
        pkg_path = os.getcwd()
    else:
        try:
            os.environ["PKG_PATH"]
        except KeyError:
            print("define a var env PKG_PACK to the absolute path of pkg.py")
            sys.exit(1)
        else:
            pkg_path = os.environ["PKG_PATH"]
    install_cmd(pkg_path)
