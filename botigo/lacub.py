import requests

payload = {
    'key': app.config['LACUB_API_KEY'],
    'SERVICE': 'WFS',
    'VERSION': '1.1.1',
    'REQUEST': 'GetFeature',
    'TYPENAME': 'TB_CHEM_L',
    'SRSNAME': 'EPSG:4326'
}

response = requests.get('http://data.lacub.fr/wfs', params=payload)
