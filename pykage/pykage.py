#! env/bin/python

from command.install_command import InstallCommand
from command.init_command import InitCommand
from command.add_command import AddCommand
from command.run_command import RunCommand
from command import load_command
import click



PYKAGE_LIST_ACTION = (
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


load_command(click, cli, [AddCommand, InstallCommand, InitCommand, RunCommand])

if __name__ == '__main__':
    cli()
