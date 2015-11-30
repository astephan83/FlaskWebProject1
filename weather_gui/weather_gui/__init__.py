"""
The flask application package.
"""

from flask import Flask
from flask.ext import flask_jsglue
app = Flask(__name__)
jsglue = flask_jsglue.JSGlue(app)

import weather_gui.views
