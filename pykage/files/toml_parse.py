import toml 
from pathlib import Path
from errors.errors_pack import TOMLNotFound
import pprint

class PyProject:
    def __init__(self, file, is_dir=False) -> None:
        self.path = Path(file) / "pkg.toml" if is_dir else Path(file)
        self.file = str(self.path)

        self._dict = self.load()
        if not self.path.exists():
            raise TOMLNotFound("pkg.toml not found")
        pprint.pprint(self._dict)


    def load(self):
        return toml.load(str(self.path))

    def get_package_group(self):

        return self._dict["pykg"]["package"]
    
    def get_var_package(self, var):
        return self._dict["pykg"]["package"][var]

    def get_project_group(self):
        return self._dict["pykg"]["project"]
    
    def get_var_project(self, var):
        return self._dict["pykg"]["project"][var]
    
    def get_file_group(self):
        return self._dict["pykg"]["file"]
    
    def get_var_file(self, var):
        return self._dict["pykg"]["file"][var]
    
    def set_var_package(self, var, value):
        self._dict["pykg"]["package"][var] = value
    
    def set_var_projet(self, var, value):
        self._dict["pykg"]["project"][var] = value
    
    def set_var_file(self, var, value):
        self._dict["pykg"]["package"][var] = value

    def append_file(self, file):
        self._dict["pykg"]["file"]["list_file"].append(file)
    
    def save(self):
        with open(self.file, "w") as file:
            toml.dump(self._dict, file)

