import os
from pathlib import Path

def is_env_py():
    try:
        os.environ["VIRTUAL_ENV"]
    except KeyError:
        return False 
    else:
        return True



