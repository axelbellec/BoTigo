import os


# Load the `.env` file at the root of the repository
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

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

# API AI
API_AI_DEV_ACCESS_TOKEN = os.environ.get('API_AI_DEV_ACCESS_TOKEN')
API_AI_CLIENT_ACCESS_TOKEN = os.environ.get('API_AI_CLIENT_ACCESS_TOKEN')

# GOOGLE MAPS API
GOOGLE_MAPS_DISTANCE_API = os.environ.get('GOOGLE_MAPS_DISTANCE_API')
GOOGLE_MAPS_GEOCODING_API = os.environ.get('GOOGLE_MAPS_GEOCODING_API')
