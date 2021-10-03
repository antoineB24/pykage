import sys
import subprocess
import os
import zipfile
import tarfile
import pkg_resources
from pkg_resources import DistributionNotFound, VersionConflict


def should_install_requirement(requirement):
    should_install = False
    try:
        pkg_resources.require(requirement)
    except (DistributionNotFound, VersionConflict):
        should_install = True
    return should_install


def install_packages(requirement_list):
    try:
        requirements = [
            requirement
            for requirement in requirement_list
            if should_install_requirement(requirement)
        ]
        if len(requirements) > 0:
            subprocess.check_call([sys.executable, "-m", "pip", "install", *requirements])
        else:
            print("Requirements already satisfied.")

    except Exception as e:
        print(e)


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
