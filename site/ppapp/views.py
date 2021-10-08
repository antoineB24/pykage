from flask import Flask, render_template
from utils.api import get_list_module, get_module_url_src, get_all_url
import json

app = Flask(__name__)

app.config.from_object('config')

@app.route('/')
def home():
    return json.dumps(get_list_module())

@app.route('/<module_name>/')
def get_module_name(module_name):
    return json.dumps(get_all_url(get_module_url_src(module_name)["href"]))


if __name__ == "__main__":
    app.run()
