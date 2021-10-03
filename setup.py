


from cx_Freeze import setup, Executable

# On appelle la fonction setup
setup(
    name = "pykg",
    version = "0.1",
    description = "l'équivalent de npm en python",
    executables = [Executable("pykg.py")],
)