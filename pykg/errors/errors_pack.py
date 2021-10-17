class PKGNotFound(FileNotFoundError): pass


class MultiplePackageFound(IndexError): pass


class PackageNotFound(IndexError): pass