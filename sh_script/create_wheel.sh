cd "$1"

python setup.py bdist_wheel

find dist/ -name "*.whl" -execdir cp '{}' $2 \;


