import requests

from botigo import app

payload = {
    'key': app.config['LACUB_API_KEY'],
    'SERVICE': 'WPS',
    'VERSION': '1.0.0',
    'REQUEST': 'Execute',
    'IDENTIFIER': 'saeiv_arret_passages'
}

response = requests.get('http://data.lacub.fr/wps', params=payload)
