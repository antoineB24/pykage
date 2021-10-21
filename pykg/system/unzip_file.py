import zipfile
import tarfile
import os
import click
from clint.textui import progress

def unzip_file_zip(file, dest='.'):
    dest_abspath = os.path.abspath(dest)
    verbose = ''
    with zipfile.ZipFile(file, 'r') as zf:
        for member in progress.bar(zf.infolist(), expected_size=len(zf.infolist())):
            try:
                zf.extract(member, dest)
            except zipfile.error as e:
                pass

    return verbose


def unzip_file_targz(file, dest='.'):
    dest_abspath = os.path.abspath(dest)

    tar = tarfile.open(file, 'r:gz')
    for member in progress.bar(tar.getmembers(), expected_size=len(tar.getmembers())):
        tar.extract(member, dest)
    tar.close()
    return tar.tarinfo



def unzip_file(file, ext, dest='.'):
    if ext == 'tar.gz':
        unzip_file_targz(file, dest)
    elif ext == "zip":
        unzip_file_zip(file, dest)

