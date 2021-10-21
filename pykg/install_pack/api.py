import sys
import requests
import bs4
import os
import jk_pypiorgapi 
import sh
import click
import pickle
from clint.textui import progress
from errors.errors_api import UrlNotFound, SiteError
from errors.errors_pack import MultiplePackageFound, PackageNotFound
from files.file import get_exentension, touch_if_no_exists
from system.unzip_file import unzip_file
from .depensie import is_requirement_important
from packaging.specifiers import SpecifierSet
from packaging.requirements import Requirement
from .install import is_install




EXT_BUILD = {"bdist_wheel": "whl", "sdist": ("tar.gz", "zip")}
URL_SIMPLE_PYPI = "https://pypi.org/simple/"
URL_PYPI = "https://pypi.org/"

get_end_ext = lambda h : h.split(".", len(h.split("."))-2)[-1] if list(filter(lambda a:a in["tar", "gz"], h.split("."))) else h.split('.')[-1]
get_file = lambda h : ".".join(filter(lambda i: i not in ["zip", "tar", "gz"], h.split('.')))



def get_all_url(sitename, prefix_url='', suffix_url=''):
    """get all href in site"""
    resp = requests.get(sitename)
    if resp.status_code == 404:
        raise UrlNotFound("url not found: %s" % resp.url)
    elif resp.status_code == 500:
        raise SiteError("a error at %s" % sitename)

    soup = bs4.BeautifulSoup(resp.text, 'html.parser')
    urls = []

    for a in soup.find_all('a'):
        if a.has_attr("href"):
            urls.append({'href': prefix_url + a['href'] + suffix_url, 'text': a.text})

    return urls


def get_list_module():
    """get list module of pypi"""
    api = jk_pypiorgapi.PyPiOrgAPI()
    packageNames = api.listAllPackages()
    return [i[1] for i in packageNames]


def get_module_url_src(name_module):
    """get url source of module"""
    list_module = get_list_module()
    list_module_find = list(filter(lambda v: v["text"] == name_module, list_module))
    if len(list_module_find) > 1:
        raise MultiplePackageFound("find multiple package")
    elif len(list_module_find) < 1:
        raise PackageNotFound("not found: %s " % name_module)

    module = list_module_find[0]

    return module


def no_letter(string):
    return any(i.isalpha() for i in string)

def get_version_latest_from_context(list_version: list, spec: SpecifierSet) -> str:
    return list(spec.filter([*list_version]))[-1]

def install_package(mod, dest='.', latest=False):
    requirement = Requirement(mod)
    if requirement.marker:
        return
    mod = requirement.name
    if is_install(mod):
        click.secho("requirement installed: %s" % mod, fg="yellow")
        return 
    click.secho("install packages: %s" % mod, fg="blue")
    type_ext_pos = ("bdist_wheel", "sdist")
    ext_trans = {}
    api = jk_pypiorgapi.PyPiOrgAPI()
    
    
    
    info = api.getPackageInfoJSON(mod)
    source = info["releases"]
    version_list = list(source.keys())
    dep = info["info"]["requires_dist"]
    
    if not bool(requirement.specifier):
        version = "latest"
    else:
        spec = requirement.specifier
        version = get_version_latest_from_context(source, spec)
    if version == "latest":
        version = version_list[-1]
    
    list_src_v = source[version]
    if len(list_src_v) == 0:
        print("no source from version %s of %s" % (version, mod))
        return 1
    src_v = list_src_v[-1]
    file_name = src_v["filename"]
    url = src_v["url"]
    py_v = src_v["python_version"]
    type_extension = src_v["packagetype"]
    type_extension = EXT_BUILD[type_extension]
    type_extension = type_extension if type_extension == "whl" else get_end_ext(file_name)


    if no_letter(py_v):
        require_python_version = py_v
    else:
        require_python_version = ".".join(py_v[2:])

    binary_file = requests.get(url, stream=True)
    click.secho("downloads file:  %s" % file_name, fg="cyan")
    with open(f"{dest}/{mod}.{type_extension}", "wb") as zip:
        total_length = int(binary_file.headers.get('content-length'))
        for chunk in progress.bar(binary_file.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1): 
            if chunk:
                zip.write(chunk)
                zip.flush()
            
    
    if type_extension in ["tar.gz", "zip"]:
        click.secho(f"unzip the file: {mod}.{type_extension}", fg="cyan")
        unzip_file(f"{dest}/{mod}.{type_extension}", type_extension, dest)
        sh.rm(f"{dest}/{mod}.{type_extension}")
        new = touch_if_no_exists(f"{dest}/pypack.lock")
        if new:
            with open(f'{dest}/pypack.lock', "wb") as pypack_init:
                pickle.dump({}, pypack_init)
        pypack_body = open(f"{dest}/pypack.lock", "rb")
        body = pickle.load(pypack_body)
        pypack_body.close()
        filename = get_file(file_name)

        with open(f"{dest}/pypack.lock", "wb") as pypack:
            updated = {**body, filename: mod}
            pickle.dump(updated, pypack)
        if dep:
            click.secho("install depensie of %s: %s" % (mod, ' '.join(dep)), fg="cyan")
            for i in dep:
                if is_requirement_important(Requirement(i)):
                    install_package(i, dest=dest)
        
       
            


        click.secho(f"sucelly install {mod}", fg="green")
        
    else:
        sh.wheel("unpack", f"{dest}/{mod}.{type_extension}")
        sh.pip("install", f"{dest}/{mod}.{type_extension}")

def install_multiple_package( *pack, **kwargs):
    click.secho("install packages: %s" % ' '.join(pack), fg="blue")
    for i in pack:
        install_package(i, kwargs["dest"])



    

class PackageLocation:
    pypi_json_project_url = "https://pypi.org/pypi/%s/json"
    def __init__(self, mod, loc=None) -> None:
        self._mod = mod 
        if loc:
            self._url_source = loc 
            self._url = None
            res_src = requests.get(self._source)
            if res_src.status_code == 404:
                raise UrlNotFound(self._source) from None
        else:
            self._url = self.pypi_json_project_url % mod
            res_pypi = requests.get(self._url)
            self._url_source = None
            if res_pypi.status_code == 404:
                raise PackageNotFound("package not found: %s" % mod)
        
        
    def get_url(self):
        return self._url
    
    def get_module(self):
        return self._mod

    def get_url_source(self):
        return self._url_source


class Depensie:
    def __init__(self, mod) :
        self._mod = mod 

    



