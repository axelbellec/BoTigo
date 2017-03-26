import datetime as dt
import requests

from botigo import config
from botigo import util

DATE_FORMAT = '%Y-%m-%d %H:%M:%S'


class LacubAPI(object):

    API_KEY = config.LACUB_API_KEY
    BASE_URL = 'http://data.lacub.fr'

    @classmethod
    def get_stops(cls):
        """ Retrieve all stops. """

        payload = {
            'KEY': cls.API_KEY,
            'SERVICE': 'WFS',
            'VERSION': '1.1.0',
            'REQUEST': 'GetFeature',
            'TYPENAME': 'bm:SV_ARRET_P',
            'SRSNAME': 'EPSG:4326'
        }

        response = requests.get('{}/wfs'.format(cls.BASE_URL), params=payload)
        stops = util.load_xml(response.content)
        return cls.normalize_stops(stops)

    @classmethod
    def get_lines(cls):
        # http://data.bordeaux-metropole.fr/wfs?key=[VOTRECLE]&REQUEST=GetFeature&SERVICE=WFS&VERSION=1.1.0&TYPENAME=bm:TB_CHEM_L&SRSNAME=EPSG:3945&PROPERTYNAME=NUMEXPLO,LONGCHEM,COULCHEM,NBPARJOH,NBPARJOE,RH_TB_LIGNE,CDATE,MDATE

        payload = {
            'KEY': cls.API_KEY,
            'SERVICE': 'WFS',
            'VERSION': '1.1.0',
            'REQUEST': 'GetFeature',
            'TYPENAME': 'bm:TB_CHEM_L',
            'SRSNAME': 'EPSG:4326'
        }

        response = requests.get('{}/wfs'.format(cls.BASE_URL), params=payload)
        lines = util.load_xml(response.content)
        return cls.normalize_lines(lines)

    @staticmethod
    def normalize_stops(stops):
        """ Normalize each feature parsed by BeautifulSoup. """

        extract = util.extract_element
        normalized = lambda stop: {
            'libelle': extract(stop, 'bm:libelle'),
            'gid': extract(stop, 'bm:gid'),
            'ident': extract(stop, 'bm:ident'),
            'groupe': extract(stop, 'bm:groupe'),
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

    @staticmethod
    def normalize_lines(lines):
        """ Normalize each feature parsed by BeautifulSoup. """

        extract = util.extract_element
        normalized = lambda line: {
            'nomcomch': extract(line, 'bm:nomcomch'),
            'nomcomli': extract(line, 'bm:nomcomli'),
            'gid': extract(line, 'bm:gid'),
            'ident': extract(line, 'bm:ident'),
            'idardeb': extract(line, 'bm:idardeb'),
            'idarfin': extract(line, 'bm:idarfin'),
            'sens': extract(line, 'bm:sens'),
            'numexplo': extract(line, 'bm:numexplo'),
            'rh_tb_ligne': extract(line, 'bm:rh_tb_ligne'),
            'type': extract(line, 'bm:type'),
            'cdate': dt.datetime.strptime(extract(line, 'bm:cdate'), DATE_FORMAT).isoformat(),
            'mdate': dt.datetime.strptime(extract(line, 'bm:mdate'), DATE_FORMAT).isoformat()
        }

        return [
            normalized(line)
            for line in lines.find_all('gml:featuremember')
        ]


if __name__ == '__main__':
    client = LacubAPI()
    stops = client.get_stops()
    print(len(stops))
