from collections import namedtuple

def dict_to_namedtuple(d: dict):
    return namedtuple('GenericDict', d.keys())(**d)