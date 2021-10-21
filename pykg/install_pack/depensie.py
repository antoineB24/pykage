import pkg_resources

def get_dependencies_from_module(package):
    package = pkg_resources.working_set.by_key[package]
    return [str(i) for i in package.requires()]

def _has_marker(req):
    return bool(req.marker)

def _has_extra(req):
    return _has_marker(req) and req.marker in "extra"

def is_requirement_important(req):
    return not _has_extra(req)

