#! env/bin/python

from cmd.init_cmd import init_cmd
from cmd.install_cmd import install_cmd
from cmd.install_args_cmd import install_args_cmd
from cmd.run_cmd import run_cmd
from cmd.run_args_cmd import run_args_cmd
from cmd.add_cmd import add_cmd
from utils.data import get_pkg_path
import os
import click
import sys

PYKG_LIST_ACTION = (
    "init",
    "install",
    "add",
    "remove",
    "run",
    "settings",
    "env",
    "activate",
    "deactivate"
)


@click.group()
def cli():
    pass

@click.command()
@click.argument("path_pkg", required=False)
def init(path_pkg):
    init_cmd(path_pkg)

@click.command("help", help="show list cmd ")
def help_cmd():
    click.echo("""
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


@click.command("install", help="install depensie of pkg.py or install depensie of you takes")
@click.argument("name", nargs=-1)
def install(name):
    pkg_path = get_pkg_path()
    if len(name) == 0:
        install_cmd(pkg_path)
    else:
        install_args_cmd(pkg_path, name)




@click.command("run", help="execute the python default file given in pkg.py or execute file given in LIST_FILE")
@click.option("-p", "--pkg", type=str, help="the pkg.py path")
@click.argument("name_file", type=str, required=False)
def run(pkg, name_file):
    path = pkg if pkg else os.getcwd()
    if name_file:
        run_args_cmd(path, name_file)
    else:
        run_cmd(path)


@click.command("add" , help="add file to LIST_FILE")
@click.option("-p", "--pkg", type=str, help="the pkg.py path")
@click.argument("files", nargs=-1, required=True)
def add(pkg, files):
    path = pkg if pkg else os.path.join(os.getcwd(), 'pkg.py')
    add_cmd(path, files)


cli.add_command(help_cmd)
cli.add_command(install)
cli.add_command(init)
cli.add_command(run)
cli.add_command(add)


if __name__ == '__main__':
    cli()
