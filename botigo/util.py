from bs4 import BeautifulSoup


def load_xml(string):
    ''' Convenience wrapper for the BeautifulSoup library. '''
    return BeautifulSoup(string, 'html.parser')


def extract_element(element, child):
    ''' Extract the content of a child element from an XML element. '''
    value = element.find(child)
    return value.string if value else ''
