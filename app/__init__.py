import os

from flask import Flask
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app._static_folder = 'static'
app.config.from_object(os.environ['APP_SETTINGS'])
bootstrap = Bootstrap(app)

from app import routes
