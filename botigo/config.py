import os

# Flask settings
# Secret key for generating tokens
SECRET_KEY = 'd0a3bc38-be11-11e6-a98e-ac293aa0f972'
# DEBUG has to be False in production for security reasons
DEBUG = True

# FB GRAPH API
FB_GRAPH_API_VERSION = float(os.environ.get('FB_GRAPH_API_VERSION'))
FB_ACCESS_TOKEN = os.environ.get('FB_ACCESS_TOKEN')
FB_VERIFY_TOKEN = os.environ.get('FB_VERIFY_TOKEN')

# LACUB API
LACUB_API_KEY = os.environ.get('LACUB_API_KEY')
