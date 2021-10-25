import os 
import sys
import subprocess
import pathlib
from regex.file_re import REGEX_FILE_PY
from errors.errors_file import UnknowTypeFile
import re

def get_exentension(file):
    step = file.split('.')
    if len(step) < 2:
        return None

    return '.'.join(step[1:len(step)])

def get_end_path(path):
    list_decouped = path.split('/')
    list_filter = list(filter(bool, list_decouped))
    return list_filter[-1]


def touch_if_no_exists(file: str, mode_binary: bool=False):
    new = not os.path.exists(file)
    open(file, 'a+').close()
    return new


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




class PyFile:
    EXTENSION_FILE_PY = ".py"
    EXECUTABLE_PYTHON = sys.executable

    @staticmethod
    def create_file_if_no_exist(file):
        path = pathlib.Path(file)
        if path.exists():
            return False 
        else:
            path.touch()
            return True

    def __init__(self, file) -> None:
        self._file = file 
        self._path = pathlib.Path(self._file)
        self._python_path = []
        """
        if not re.match(REGEX_FILE_PY, self._file):
            raise UnknowTypeFile("unknow type file: %s" % self._file)"""

    def run(self, *args):
        subprocess.check_call([self.EXECUTABLE_PYTHON, self._file, *args])

    def add_pythonpath(self, path):
        self._python_path.append(path)
        os.environ["PYTHONPATH"] += ":" + path

    def get_absolute_path(self):
        return self._path.absolute()
    
    def get_path(self):
        return self._path 

    def get_file(self):
        return self._file
    
    def get_executable(self):
        return self.EXECUTABLE_PYTHON
    
    def set_executable(self, epython):
        self.EXECUTABLE_PYTHON = epython
    
    def __str__(self) -> str:
        return f"<PyFile path={self._path} file={self._file} type=py-file"

    def __repr__(self) -> str:
        return repr(str(self))