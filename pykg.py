#! env/bin/python

from cmd.init_cmd import InitCmd
from cmd.install_cmd import InstallCmd
from cmd.run_cmd import RunCmd
from cmd.add_cmd import AddCmd
from cmd.cmd import load_cmd
import click


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


load_cmd(click, cli, (InitCmd, InstallCmd, AddCmd, RunCmd))

if __name__ == '__main__':
    cli()
