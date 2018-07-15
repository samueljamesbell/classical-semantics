
# coding: utf-8

# In[ ]:

import word2vec
import csv


# In[ ]:

csv.register_dialect('custom', delimiter='|')

def get_composer_names_from_file(filepath='../data/composers_freebase.csv'):
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f, dialect='custom')
        composer_names = [row['composer_name'] for row in reader]
        
    return composer_names

def write_composer_names_to_file(composer_names, filepath='../data/composer_names.txt'):
    with open(filepath, 'w') as f:
        for composer_name in composer_names:
            f.write('%s\n' % composer_name)
    


# In[ ]:

composer_names = get_composer_names_from_file()
write_composer_names_to_file(composer_names)


# In[ ]:

word2vec.word2vec('/Users/sam/Downloads/text8', '/Users/sam/Downloads/text8.bin', 
                  verbose=True,
                  read_vocab='../data/composer_names.txt')


# In[ ]:



