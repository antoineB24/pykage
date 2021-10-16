class PKGNotFound(FileNotFoundError): pass


class MultiplePackageFound(IndexError): pass


class PackageNotFound(IndexError): pass


class UrlNotFound(NameError): pass


class SiteError(NameError): pass


class InvalidFormatFile(SyntaxError): pass


class InvalidTypeAst(TypeError): pass
