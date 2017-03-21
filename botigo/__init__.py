from flask import Flask, url_for

NAMESPACE = 'botigo'

app = Flask(NAMESPACE)

# Setup the application
app.config.from_object('botigo.config')

# Add the top level to the import path
import sys
sys.path.append('..')

# FIXME: unable to load env var in development mode
# import dotenv
# dotenv.load_dotenv(dotenv.find_dotenv())

from botigo import api
