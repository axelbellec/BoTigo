import requests
import bs4
import re

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
