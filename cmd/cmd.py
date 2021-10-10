import abc


class Callable(object):
    def __init__(self, f):
        self.f = f
        self.__name__ = f.__name__

    def __call__(self, *args, **kwargs):
        return self.f(*args, **kwargs)


def wrap_for_cython(f):
    return Callable(f)

class Cmd:
    option = []
    arguments = []

    def __init__(self, click_mod, group):
        self.group = group
        self.click = click_mod

    def recup_info(self, *args, **kwargs):
        for i in kwargs:
            setattr(self, i, kwargs[i])

        self.main()

    @abc.abstractmethod
    def main(self, *args, **kwargs):
        pass

    def build(self):
        self.recup_info = self.click.command(self.name, help=self.help)(self.recup_info)
        for i in self.option:
            self.recup_info = self.click.option(**i)(self.main)
        for a in self.arguments:
            self.recup_info = self.click.argument(a["name"], **a["option"])(self.main)
        self.recup_info = wrap_for_cython(self.recup_info)
        self.group.add_command(self.recup_info)
