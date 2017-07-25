import os

from flask import Flask

# Init App
NAMESPACE = 'app'
app = Flask(NAMESPACE)

# Configure the application
app.config.from_object('botigo.config')

from botigo import views
