import datetime as dt
import requests

from botigo import app
from botigo import util

DATE_FORMAT = '%Y-%m-%d %H:%M:%S'


class LacubAPI(object):

    def __init__(self):
        self.api_key = app.config['LACUB_API_KEY']
        self.base_url = 'http://data.lacub.fr'

    def get_stops(self):
        """ Retrieve all stops. """

        payload = {
            'KEY': self.api_key,
            'SERVICE': 'WFS',
            'VERSION': '1.1.0',
            'REQUEST': 'GetFeature',
            'TYPENAME': 'bm:SV_ARRET_P',
            'SRSNAME': 'EPSG:4326'
        }

        response = requests.get('{}/wfs'.format(self.base_url), params=payload)
        stops = util.load_xml(response.content)
        return self._normalize(stops)

    def _normalize(self, stops):
        """ Normalize each feature parsed by BeautifulSoup. """

        extract = util.extract_element
        normalized = lambda stop: {
            'libelle': extract(stop, 'bm:libelle'),
            'gid': extract(stop, 'bm:gid'),
            'latitude': float(extract(stop, 'gml:pos').split(' ')[0]),
            'longitude': float(extract(stop, 'gml:pos').split(' ')[1]),
            'type': extract(stop, 'bm:type'),
            'cdate': dt.datetime.strptime(extract(stop, 'bm:cdate'), DATE_FORMAT).isoformat(),
            'mdate': dt.datetime.strptime(extract(stop, 'bm:mdate'), DATE_FORMAT).isoformat()
        }

        return [
            normalized(stop)
            for stop in stops.find_all('gml:featuremember')
        ]


if __name__ == '__main__':
    client = LacubAPI()
    stops = client.get_stops()
    print(len(stops))
