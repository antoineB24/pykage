
from cmd.init_cmd import init_cmd
import sys

args = sys.argv[1] if len(sys.argv) - 1 else None

if args == 'help':
    print("""
usage: main.py  cmd 

list cmd:
  init              créer un pkg.py
  install           installe les dependenses de pkg.py
  install lib       installe avec pip et ajoute comme depensie nom_du_module dans pkg.py
  run               executer le fichier python donné dans pkg.py(DEFAULT_FILE)
  run file          execute le fichier python dans pkg.py(LIST_FILE)
  add file          ajoute un fichier dans pkg.py(LIST_FILE)
  settings var val  ajoute/modifie une setting dans pkg.py
  remove file       supprime un fichier dans pkg.py(LIST_FILE)
  env name_env      créer un environement avec les depensies installé dans pkg.py
  activate          active l'env si l'env existe
  deactivate        desactive l'env si il est activé



optional arguments:
  -h, --help  show this help message and exit
  """)

