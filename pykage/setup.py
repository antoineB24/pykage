from cx_Freeze import setup, Executable
files = {"include_files": [
                       "command/",
                       ], "packages": []}

setup(
 name="pykage",
 version="0.1.5",
 description="npmjs en python",
 options={'build_exe': files},
 executables=[Executable("pykage.py", base=None)])

