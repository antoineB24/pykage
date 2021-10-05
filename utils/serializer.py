import pickle
import os
import pathlib
from system import get_end_path, touch_if_no_exists, remove_extension

def str_to_bin(s):
    return ' '.join([i[2:] for i in map(bin,bytearray(s))])

def dump_binary_file(file, new_file):
    with open(file) as l1:
        body = l1.read()

    with open(new_file, 'wb+') as w1:
        w1.write(str_to_bin(body))


def dumps_binary_file(file):
    with open(file, 'rb') as l1:
        body = l1.read()

    return str_to_bin(body)

def dump_binary_dir(dir, new_file):
    body = {'dir': {}}
    body['dir']['name'] = get_end_path(dir)
    body['dir']['files'] = {}

    path_bfs_dump_file = new_file

    touch_if_no_exists(path_bfs_dump_file)
    print(dir)
    for i in os.listdir(dir):
        if i == "__pycache__": continue
        ic = os.path.join(dir, i)
        ic = os.path.abspath(ic)
        print(ic)
        body['dir']['files'][f"{remove_extension(f'file_{ic}')}.bfs"] = dumps_binary_file(ic)

    with open(path_bfs_dump_file, "wb") as file:
        pickle.dump(body, file)



if __name__ == '__main__':
    dump_binary_dir("utils", "k.bfs")





