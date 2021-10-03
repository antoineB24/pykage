import sys
import data
import requests
import bs4
import os
import animation
from .errors import UrlNotFound, SiteError, MultiplePackageFound, PackageNotFound
from .system import get_exentension, unzip_file
import time


URL_SIMPLE_PYPI = "https://pypi.org/simple/"
URL_PYPI = "https://pypi.org/"


def get_all_url(sitename, prefix_url='', suffix_url=''):
    resp = requests.get(sitename)
    if resp.status_code == 404:
        raise UrlNotFound("url not found: %s" % resp.url)
    elif resp.status_code == 500:
        raise SiteError("a error at api")

    soup = bs4.BeautifulSoup(resp.text, 'html.parser')
    urls = []

    for a in soup.find_all('a'):
        if a.has_attr("href"):
            urls.append({'href': prefix_url + a['href'] + suffix_url, 'text': a.text})

    return urls


def get_list_module():
    return get_all_url(URL_SIMPLE_PYPI, URL_PYPI)


def get_module_url_src(name_module):
    list_module = get_list_module()
    list_module_find = list(filter(lambda v: v["text"] == name_module, list_module))
    if len(list_module_find) > 1:
        raise MultiplePackageFound("find multiple package")
    elif len(list_module_find) < 1:
        raise PackageNotFound("not found: %s " % name_module)

    module = list_module_find[0]

    return module


def install_module(module_name, path_pkg):
    print('install package: %s' % module_name)
    path = os.path.abspath(path_pkg)
    module_src = get_module_url_src(module_name)
    list_src = get_all_url(module_src["href"])
    zipped = []

    for src in list_src:
        ext = get_exentension(src["text"])
        if ext.find('.tar.gz') != -1:
            zipped.append({**src, "ext": "tar.gz"})
        elif ext.find('.zip') != -1:
            zipped.append({**src, "ext": "zip"})

    # print(zipped)
    first_z = zipped[-1] # take the last version
    if first_z["ext"] == "zip":
        name = first_z['text'][:-4]
    elif first_z["ext"] == "tar.gz":
        name = first_z['text'][:-7]

    res_file = requests.get(first_z['href'], stream=True)
    with open(f'{path}/{first_z["text"]}', 'wb') as file:
        file.write(res_file.raw.read())

    unzip_file(f"{path}/{first_z['text']}", first_z['ext'], path)
    if first_z["ext"] in ["zip", "tar.gz"]:
        os.system(f"cd {path}/{name}; pip install . ")


def install_multiple_module(path_pkg, *list_module):
    print("install multiple module: %s", ','.join(list_module))
    for i in list_module:
        install_module(i, path_pkg)


