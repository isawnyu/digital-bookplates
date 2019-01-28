# Imports

import pandas

from collections import Counter
from pprint import pprint

import pickle

# Pandas expects this file to be encoded as UTF-8 (and possibily to have Unix (LF)-style line breaks. Open csv in Textwrangler vel sim and change this is read_csv generates an error.

df = pandas.read_csv('../data/shelflist.csv')

# Keep only needed columns

df = df[['BSN','Z13_AUTHOR', 'Z13_TITLE', 'Z13_IMPRINT', 'Z30_NOTE_INTERNAL']]

# Add column for 'featured' titles

df['featured'] = df.apply(lambda x: 0, axis=1)

# Rename columns

df = df.rename(columns={'BSN': 'bsn',
                        'Z13_AUTHOR': 'author',
                        'Z13_TITLE': 'title',
                        'Z13_IMPRINT': 'imprint',
                        'Z30_NOTE_INTERNAL': 'collection'
                       }
              )

# Drop rows without collection info

df = df.dropna(subset=['collection'])

# Helper function to normalize collection data

def clean_collection(string):
    cleaned = string

    # Remove punctuation with translate
    punctuation ="\"#$%&\'()+,-/:;<=>@[\]^_`{|}~.?!«»—"
    translator = str.maketrans({key: " " for key in punctuation})
    cleaned = cleaned.translate(translator)

    cleaned = cleaned.replace('Collection', '')

    return cleaned.strip()

# Clean collection column

df['collection'] = df['collection'].apply(lambda x: clean_collection(x))

# Get eligible DBP collections

min_threshold = 100
excluded_categories = ['Mesopotamian', 'Bobst transfer']

dbp_elig = Counter(df['collection'])
dbp_elig = {x : dbp_elig[x] for x in dbp_elig if dbp_elig[x] >= min_threshold and x not in excluded_categories}
dpb_elig = list(dbp_elig.keys())

df = df[df['collection'].isin(dpb_elig)]

# Dump json-like object as pickle to data folder
# e.g.
# [
#     {
#         'bsn': '002057948',
#         'author': 'Newberry, Percy E. (Percy Edward), 1869-1949.',
#         'title': 'El Bersheh / ',
#         'imprint': 'London ; Boston : Egypt Exploration Fund, [1893-1894?]',
#         'collection': 'May',
#         'featured': 1,
#     }, ...
# ]

dbp_data = list(df.T.to_dict().values())
pickle.dump( dbp_data, open('../data/dbp_data.p', 'wb'))
