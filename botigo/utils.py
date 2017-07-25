import re
import unicodedata

import requests
import bs4

from botigo import mocks

REGEX_ESCAPE_MULTIPLE_SPACES = re.compile(r'\s+')

url = mocks.URLS['tram']['Ligne B'][
    'BORDEAUX Berges de la Garonne / BORDEAUX La Cité du Vin']['TALENCE Barrière Saint-Genès']

response = requests.get(url)
html = response.content

soup = bs4.BeautifulSoup(html, 'html.parser')
departure_times = [
    REGEX_ESCAPE_MULTIPLE_SPACES.sub(' ', tag.get_text().strip())
    for tag in soup.find_all('span', attrs={'class': 'inline-left'})
]


def to_ascii_chars(string):
    """ Replace special characters by ascii characters.
    Example:
        >>> string = 'ça fonctionne plutôt bien'
        >>> to_ascii_chars(string)
        ... 'ca fonctionne plutot bien'
    """
    return (unicodedata
            .normalize('NFKD', string)
            .encode('ascii', 'ignore')
            .decode('utf-8'))
