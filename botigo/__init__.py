from flask import Flask, url_for

NAMESPACE = 'botigo'

app = Flask(NAMESPACE)

# Setup the application
app.config.from_object('botigo.config')

# Add the top level to the import path
import sys
sys.path.append('..')

from botigo import api
