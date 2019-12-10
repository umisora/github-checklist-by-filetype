from flask import Flask

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

from main.view import api
from main.view import healthcheck
