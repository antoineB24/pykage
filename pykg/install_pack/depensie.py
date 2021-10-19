import pkg_resources

def get_dependencies_from_module(package):
    package = pkg_resources.working_set.by_key[package]
    return [str(i) for i in package.requires()]

