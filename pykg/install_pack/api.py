import requests
import bs4
import jk_pypiorgapi 
from errors.errors_api import UrlNotFound, SiteError
from errors.errors_pack import MultiplePackageFound, PackageNotFound





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





