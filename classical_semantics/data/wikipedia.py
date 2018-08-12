import functools
import itertools 
import re

from bs4 import BeautifulSoup
import requests


@functools.lru_cache()
def soup(url):
    """Return a soup object of the page's content."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')
    except requests.HTTPError:
        return None
  

@functools.lru_cache()
def text(soup):
    """Return main text for a given soup object."""
    if soup is None:
        return ''
  
    paragraphs = soup.find(attrs={"class": "mw-parser-output"}).find_all('p')
    all_text = ' '.join(list(itertools.chain.from_iterable(para.stripped_strings for para in paragraphs)))
    return re.sub('\[\d*\]', '', all_text)
