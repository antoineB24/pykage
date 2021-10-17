import sys 
sys.path.append('..')

def load_command(click, group, cmd):
    for Object in cmd:
        obj = Object(click, group)
        obj.build()