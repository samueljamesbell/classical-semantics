import functools
import itertools 

from bs4 import BeautifulSoup
from keras.utils import to_categorical
from nltk.tokenize import word_tokenize
import requests


def composers(path):
    with open(path, 'r') as f:
        next(f)  # Skip headers
        for composer_id, line in enumerate(f):
            yield (composer_id, *line.strip().split('|'))
      

@functools.lru_cache()
def soup(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')
    except requests.HTTPError:
        return None
  

@functools.lru_cache()
def text(soup):
    if soup is None:
        return ''
  
    paragraphs = soup.find(attrs={"class": "mw-parser-output"}).find_all('p')
    all_text = ' '.join(list(itertools.chain.from_iterable(para.stripped_strings for para in paragraphs)))
    return re.sub('\[\d*\]', '', all_text)


@functools.lru_cache()
def tokens(text):
    return word_tokenize(text)


@functools.lru_cache()
def tokens_by_composer_id(path):
    return {c[0]: tokens(text(soup(c[-1]))) for c[0] in composers(path)}


def data_generator(token_ids_by_composer_id, window_size, vocab_size):
    assert window_size % 2 == 0, 'window_size must be even'

    offset = window_size // 2
  
    for composer_id, token_ids in itertools.cycle(composers.items()):
        num_tokens = len(token_ids)
    
        if num_tokens <= window_size:
            continue
    
        target_idx = random.randint(offset, (num_tokens - offset) - 1)
    
        target_id = token_ids[target_idx]
      
        context_window = token_ids[target_idx-offset:target_idx] + token_ids[target_idx+1:target_idx+offset+1]
    
        yield (composer_id,
	       context_window,
	       to_categorical(target_id, num_classes=vocab_size))
    

def batch(data, batch_size=32):
    while True:
        batch = itertools.islice(data, batch_size)
    
        x_1 = []
        x_2 = []
        y = []
    
        for item in batch:
            composer_id, context_window, target_ids = item
      
            x_1.append(composer_id)
            x_2.append(context_window)
            y.append(target_ids)
      
        yield [np.array(x_1), np.array(x_2)], np.array(y)

