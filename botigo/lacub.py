import datetime as dt
import requests

from botigo import config
from botigo import util

WFS_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
WPS_DATE_FORMAT = '%Y-%m-%dT%H:%M:%S'


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
    def get_paths(cls):

        payload = {
            'KEY': cls.API_KEY,
            'SERVICE': 'WFS',
            'VERSION': '1.1.0',
            'REQUEST': 'GetFeature',
            'TYPENAME': 'bm:TB_CHEM_L',
            'SRSNAME': 'EPSG:4326'
        }

        response = requests.get('{}/wfs'.format(cls.BASE_URL), params=payload)
        paths = util.load_xml(response.content)
        return cls.normalize_paths(paths)

    @classmethod
    def get_lines(cls):

        payload = {
            'KEY': cls.API_KEY,
            'SERVICE': 'WPS',
            'VERSION': '1.0.0',
            'REQUEST': 'Execute',
            'IDENTIFIER': 'SV_LIGNE_A'
        }

        response = requests.get('{}/wps'.format(cls.BASE_URL), params=payload)
        lines = util.load_xml(response.content)
        return cls.normalize_lines(lines)

    @classmethod
    def get_lines_paths(cls):

        payload = {
            'KEY': cls.API_KEY,
            'SERVICE': 'WPS',
            'VERSION': '1.0.0',
            'REQUEST': 'Execute',
            'IDENTIFIER': 'SV_CHEM_A'
        }

        response = requests.get('{}/wps'.format(cls.BASE_URL), params=payload)
        lines_paths = util.load_xml(response.content)
        return cls.normalize_lines_paths(lines_paths)

    @classmethod
    def get_path_stops(cls, gid):

        # http://data.bordeaux-metropole.fr/wps?key=SBXV78WZQ0&service=WPS&version=1.0.0&SRSNAME=EPSG:4326&request=execute&Identifier=saeiv_arrets_chemin&DATAINPUTS=gid=267436926
        payload = {
            'KEY': cls.API_KEY,
            'SERVICE': 'WPS',
            'VERSION': '1.0.0',
            'REQUEST': 'Execute',
            'IDENTIFIER': 'saeiv_arrets_chemin',
            'SRSNAME': 'EPSG:4326',
            'DATAINPUTS': 'GID={}'.format(gid)
        }

        response = requests.get('{}/wps'.format(cls.BASE_URL), params=payload)
        path_stops = util.load_xml(response.content)
        return cls.normalize_path_stops(path_stops)

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
            'cdate': dt.datetime.strptime(extract(stop, 'bm:cdate'), WFS_DATE_FORMAT).isoformat(),
            'mdate': dt.datetime.strptime(extract(stop, 'bm:mdate'), WFS_DATE_FORMAT).isoformat()
        }

        return [
            normalized(stop)
            for stop in stops.find_all('gml:featuremember')
        ]

    @staticmethod
    def normalize_paths(paths):
        """ Normalize each feature parsed by BeautifulSoup. """

        extract = util.extract_element
        normalized = lambda path: {
            'nomcomch': extract(path, 'bm:nomcomch'),
            'nomcomli': extract(path, 'bm:nomcomli'),
            'gid': extract(path, 'bm:gid'),
            'ident': extract(path, 'bm:ident'),
            'idardeb': extract(path, 'bm:idardeb'),
            'idarfin': extract(path, 'bm:idarfin'),
            'sens': extract(path, 'bm:sens'),
            'numexplo': extract(path, 'bm:numexplo'),
            'rh_tb_ligne': extract(path, 'bm:rh_tb_ligne'),
            'cdate': dt.datetime.strptime(extract(path, 'bm:cdate'), WFS_DATE_FORMAT).isoformat(),
            'mdate': dt.datetime.strptime(extract(path, 'bm:mdate'), WFS_DATE_FORMAT).isoformat()
        }

        return [
            normalized(path)
            for path in paths.find_all('gml:featuremember')
        ]

    @staticmethod
    def normalize_lines(lines):
        """ Normalize each feature parsed by BeautifulSoup. """

        extract = util.extract_element
        normalized = lambda line: {
            'gid': extract(line, 'bm:gid'),
            'libelle': extract(line, 'bm:libelle'),
            'active': extract(line, 'bm:active'),
            'type': extract(line, 'bm:type'),
            'cdate': dt.datetime.strptime(extract(line, 'bm:cdate'), WPS_DATE_FORMAT).isoformat(),
            'mdate': dt.datetime.strptime(extract(line, 'bm:mdate'), WPS_DATE_FORMAT).isoformat()
        }

        return [
            normalized(line)
            for line in lines.find_all('gml:featuremember')
        ]

    @staticmethod
    def normalize_lines_paths(lines_paths):
        """ Normalize each feature parsed by BeautifulSoup. """

        extract = util.extract_element
        normalized = lambda line_path: {
            'gid': extract(line_path, 'bm:gid'),
            'libelle': extract(line_path, 'bm:libelle'),
            'sens': extract(line_path, 'bm:sens'),
            'type': extract(line_path, 'bm:type'),
            'rs_sv_arret_p_nd': extract(line_path, 'bm:rs_sv_arret_p_nd'),
            'rs_sv_arret_p_na': extract(line_path, 'bm:rs_sv_arret_p_na'),
            'rs_sv_ligne_a': extract(line_path, 'bm:rs_sv_ligne_a'),
            'cdate': dt.datetime.strptime(extract(line_path, 'bm:cdate'), WPS_DATE_FORMAT).isoformat(),
            'mdate': dt.datetime.strptime(extract(line_path, 'bm:mdate'), WPS_DATE_FORMAT).isoformat()
        }

        return [
            normalized(line_path)
            for line_path in lines_paths.find_all('gml:featuremember')
        ]

    @staticmethod
    def normalize_path_stops(path_stops):
        """ Normalize each feature parsed by BeautifulSoup. """

        extract = util.extract_element
        normalized = lambda path_stop: {
            'gid': extract(path_stop, 'bm:gid'),
            'geom_o': extract(path_stop, 'bm:geom_o'),
            'ident': extract(path_stop, 'bm:ident'),
            'groupe': extract(path_stop, 'bm:groupe'),
            'libelle': extract(path_stop, 'bm:libelle'),
            'type': extract(path_stop, 'bm:type'),
            'ordre': extract(path_stop, 'bm:ordre')
        }

        return [
            normalized(path_stop)
            for path_stop in path_stops.find_all('gml:featuremember')
        ]


if __name__ == '__main__':
    client = LacubAPI()
    stops = client.get_stops()
    print(len(stops))
