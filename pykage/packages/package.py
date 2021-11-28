import sys
import os, sh
from click.termui import secho
from files.file import touch_if_no_exists
import pkg_resources
import random
import pickle
import click
import requests
import time
from clint.textui import progress
from errors.errors_pack import PackageNotFound
from errors.errors_api import UrlNotFound, GitReposteryNotFound
from system.unzip_file import unzip_file
from regex.data_re import REGEX_GIT_PROJECT, is_valid_git_project, is_valid_url, get_name_from_git_repostery
from pkg_resources import DistributionNotFound, VersionConflict
from packaging.specifiers import SpecifierSet
from packaging.requirements import Requirement
from git.repo.base import Repo

EXT_BUILD = {"bdist_wheel": "whl", "sdist": ("tar.gz", "zip")}
get_end_ext = lambda h: h.split(".", len(h.split(".")) - 2)[-1] if list(
    filter(lambda a: a in ["tar", "gz"], h.split("."))) else h.split('.')[-1]
get_file = lambda h: ".".join(filter(lambda i: i not in ["zip", "tar", "gz"], h.split('.')))


def get_list_version_latest_from_context(list_version: list, spec: SpecifierSet) -> list:
    return list(spec.filter([*list_version]))


def install_package(mod, dest='.'):
    package = Package(mod)
    package.install_module(dest)


def install_multiple_package(*pack, **kwargs):
    click.secho("install packages: %s" % ' '.join(pack), fg="blue")
    for i in pack:
        install_package(i, kwargs["dest"])


class PackageLocation:
    pypi_json_project_url = "https://pypi.org/pypi/%s/json"

    def __init__(self, mod, loc=None) -> None:
        self._mod = mod
        if is_valid_git_project(loc):
            self._type = "git"
            self._url_source = loc
            self._url = None
            res_src = requests.get(self._url_source)
            if res_src.status_code == 404:
                raise GitReposteryNotFound(self._url_source) from None
            self._data = None
        elif is_valid_url(loc):
            self._type = "source"
            self._url_source = loc
            self._url = None
            res_src = requests.get(self._url_source)
            if res_src.status_code == 404:
                raise GitReposteryNotFound(self._url_source) from None
            self._data = None
            
        else:
            
            self._type = "pypi"
            self._url = self.pypi_json_project_url % mod
            res_pypi  = requests.get(self._url)
            self._url_source = None
            if res_pypi.status_code == 404:
                raise PackageNotFound("package not found: %s" % mod)
            self._data = res_pypi.json()

    def get_url(self):
        return self._url

    def get_module(self):
        return self._mod

    def get_url_source(self):
        return self._url_source
    
    def get_data(self):
        return self._data
    
    def get_type(self):
        return self._type


class Package:
    @staticmethod
    def is_install(module):
        cwd = os.getcwd()
        reader = open("pypack/pypack.lock", "rb")

        list_module_installed = pickle.load(reader)
        reader.close()

        return module in list_module_installed or not Package.should_install_requirement(module)

    @staticmethod
    def should_install_requirement(requirement):
        should_install = False
        try:
            pkg_resources.require(requirement)
        except (DistributionNotFound, VersionConflict):
            should_install = True
        return should_install

    def __init__(self, mod, spec_str=''):
        if is_valid_git_project(mod) or is_valid_url(mod):
            self._loc = PackageLocation(None, mod)
        else:
            self._loc = PackageLocation(mod)

        

    def get_depensie(self):
        mod_info = self._loc.get_data()
        depensie = mod_info["info"]["requires_dist"]
        if not depensie :
            return []
        depensie = [Requirement(i) for i in depensie]
        depensie = list(filter(lambda v: not bool(v.marker), depensie))
        dep = []
        for i in depensie:
            dep.extend(self.get_depensie(i))

        return dep

    def install_module(self, dest='.'):
        match self._loc.get_type():
            case "pypi" : 
                self.install_pip_module(dest)
            case "git" : 
                self.install_git_module(dest)
            case "source": self.install_source(dest)
            case _ : click.secho("ERROR" ,fg="red")
    
    def install_git_module(self, dest="."):
        if self._loc.get_type() == "git":
            click.secho("install git repostery : %s" % self._loc.get_url_source(), fg="blue")
            click.secho("clonning git repostery", fg="cyan")
            sh.cd("pypack/")
            sh.git("clone", self._loc.get_url_source())
            click.secho("\rOK", fg="green")
            print(click.style("installing...", fg="cyan"), end=" ")
            sh.cd(get_name_from_git_repostery(self._loc.get_url_source()))
            sh.pip("install", ".")
    
    def install_source(self, dest="."):
        if self._loc.get_type() == "source":
            click.secho("install from url source : %s" % self)
            print(click.style("fetching data...", fg="cyan"), end=" ")
            time.sleep(random.randint(1, 5))
            click.secho("OK", fg="green")
            print(click.style("installing package...", fg="cyan"), end=" ")
            sh.python3("-m",  "pip", "install", "--index-url",  self._loc.get_url_source(), "--src", dest)
            click.secho("OK", fg="green")

    def install_pip_module(self, src="."):
        if self._loc.get_type() == "pypi":
            sh.pip("install", self._loc.get_module(), "--no-deps", "--src", src)
            dep = self.get_depensie()
            click.secho("installing depnsie", fg="cyan")
            for i in dep:
                print(click.style("\tinstall %s" % i.name, fg="cyan"), end=" ")
                sh.pip("install", str(i), "--no-deps", "--src", src)
                click.secho("OK", fg="green")
            click.secho("OK", fg="green")


"""def install_packages(requirement_list):
    
    requirements = [
        requirement
        for requirement in requirement_list
        if is_install(requirement)
    ]
    if len(requirements) > 0:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-t", "pypackages/", *requirements])
    else:
        print("Requirements already satisfied.")

    reader = open('pypackages/lpkg.lock', 'rb')
    list_m = pickle.load(reader)
    reader.close()

    with open('pypackages/lpkg.lock', 'wb') as w1:
        pickle.dump(list_m + requirement_list, w1)"""
