import pickle
import os
import pathlib
from system import get_end_path, touch_if_no_exists, remove_extension, get_end_abspath

def str_to_bin(s):
    return ' '.join([i[2:] for i in map(bin, bytearray(s))])

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
        body['dir']['files'][f"{ic}"] = dumps_binary_file(ic)

    with open(path_bfs_dump_file, "wb") as file:
        pickle.dump(body, file)



def loads_binary_file(file):
    with open(file, 'rb') as f1:
        body = f1.read()
        print(body)

    l = body.split(b' ')

    for i in range(len(l)):
        e=f"{l[i]}"
        #l[i] = chr(eval(e))

    return b''.join(l)

def load_binary_file(file):
    string = loads_binary_file(file)
    os.system(f"touch {remove_extension(file)}.txt")
    with open(f"{remove_extension(file)}.txt", 'w') as w1:
        w1.write(string)

def write(file, string, mode=''):
        with open(file, "w" + mode) as writer:
            writer.write(string)
def read(file, mode=''):
    with open(file, 'r'+mode) as reader:
        return reader.read()


def load_binary_dir(file):
    r1 = open(file, 'rb')
    body = pickle.load(r1)
    r1.close()

    dir = body['dir']
    name = dir["name"]
    files = dir["files"]
    for i in files:
        files[i] = loads_binary_file(i)

    os.mkdir(name)
    for i in files:
        os.system("touch %s/%s" % (name, i))
        write("%s/%s" % (name, i), files[i])




if __name__ == '__main__':
    #dump_binary_dir("pykg/cmd", "jjll.bfs")
    load_binary_dir("jjll.bfs")




