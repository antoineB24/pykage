import requests
import bs4
import os
from errors import UrlNotFound, SiteError, MultiplePackageFound, PackageNotFound
from system import get_exantension

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
    path = os.path.abspath(path_pkg)
    module_src = get_module_url_src(module_name)

    list_src = get_all_url(module_src["href"])
    zipped = []
    ext_poss = ["zip", "tar.gz"]
    for src in list_src:
        ext = get_exantension(src["text"])
        if ext.find('.tar.gz') != -1:
            zipped.append({**src, "ext" : "tar.gz"})
        elif ext.find('.zip') != -1:
            zipped.append({**src, "ext": "zip"})

    #print(zipped)
    first_z = zipped[-1]
    os.system(f"curl {first_z['href']} > {path}/{first_z['text']}")
    os.system(f"tar -xzvf {path}/{first_z['text']}")
    #os.system(f"mv {path}/{first_z['text']} {path}/{'-'.join(first_z['text'].split('.')[:-1])}")
    print(first_z['text'])
    if first_z["ext"] == "zip":
        os.system(f"cd {first_z['text'][:-4]}; pip install .")
    elif first_z["ext"] == "tar.gz":
        os.system(f"cd {first_z['text'][:-7]}; pip install .")











