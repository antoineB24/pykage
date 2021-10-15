import sys
import subprocess
import os
import zipfile
import tarfile
import pkg_resources
from pkg_resources import DistributionNotFound, VersionConflict
import pickle


def is_install(module):
    cwd = os.getcwd()
    new = touch_if_no_exists("pypackages/lpkg.lock", True)
    if new:
        writer = open("pypackages/lpkg.lock", "wb")
        pickle.dump([], writer)
        writer.close()
    reader = open("pypackages/lpkg.lock", "rb")
    list_module_installed = pickle.load(reader)
    reader.close()
    return module in list_module_installed or should_install_requirement(module)


def should_install_requirement(requirement):
    should_install = False
    try:
        pkg_resources.require(requirement)
    except (DistributionNotFound, VersionConflict):
        should_install = True
    return should_install


def install_packages(requirement_list):
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
        pickle.dump(list_m + requirement_list, w1)


def get_exentension(file):
    step = file.split('.')
    if len(step) < 2:
        return None

    return '.'.join(step[1:len(step)])


def unzip_file_zip(file, dest='.'):
    dest_abspath = os.path.abspath(dest)
    verbose = ''
    with zipfile.ZipFile(file, 'r') as zip:
        verbose = zip.filelist
        zip.extractall(dest_abspath)

    return verbose


def unzip_file_targz(file, dest='.'):
    dest_abspath = os.path.abspath(dest)

    tar = tarfile.open(file, 'r:gz')
    tar.extractall(dest_abspath)

    tar.close()
    return tar.tarinfo


def unzip_file(file, ext, dest='.'):
    if ext == 'tar.gz':
        unzip_file_targz(file, dest)
    elif ext == "zip":
        unzip_file_zip(file, dest)


def get_end_path(path):
    list_decouped = path.split('/')
    list_filter = list(filter(bool, list_decouped))
    return list_filter[-1]


def touch_if_no_exists(file, mode_binary=False):
    open(file, 'a+').close()
    vide = True
    mode = 'rb' if mode_binary else 'r'
    with open(file, mode) as f:
        if bool(f.read()):
            vide = False
    return vide


def remove_extension(filename):
    split_l = filename.split('.')

    if len(split_l) == 0:
        return filename

    del split_l[-1]
    return '.'.join(split_l)


def list_to_list_abspath(list):
    return [os.path.abspath(i) for i in list]


def get_end_abspath(path):
    step = path.split("\\")
    list_filter = list(filter(bool, step))
    return list_filter[-1]
