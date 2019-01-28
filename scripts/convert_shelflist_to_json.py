
# Imports

import pandas as pd

from collections import Counter
from pprint import pprint

import pickle

# Pandas expects this file to be encoded as UTF-8 (and possibily to have Unix (LF)-style line breaks. Open csv in Textwrangler vel sim and change this is read_csv generates an error.

df = pd.read_csv('../app/static/data/shelflist.csv')

# Keep only needed columns

df = df[['BSN','Z13_AUTHOR', 'Z13_TITLE', 'Z13_IMPRINT', 'Z30_NOTE_INTERNAL']]

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

# Helper function to normalize bsns

def normalize_bsn(bsn):
    bsn = str(bsn)
    if len(bsn) < 9:
        bsn = "0" * (9-len(bsn)) + bsn
    return bsn

# Fix bsn length

df['bsn'] = df['bsn'].apply(lambda x: normalize_bsn(x))

# Get featured bsns

with open('../app/static/data/featured.txt') as f:
    featured_bsns = f.read().splitlines()

# Helper function for add featured bsns

def add_featured(bsn):
    if bsn in featured_bsns:
        return 1
    else:
        return 0

df['featured'] = df['bsn'].apply(lambda x: add_featured(x))

# Get eligible DBP collections

min_threshold = 100
excluded_categories = ['Mesopotamian', 'Bobst transfer', "LP", "Persian"]

dbp_elig = Counter(df['collection'])
dbp_elig = {x : dbp_elig[x] for x in dbp_elig if dbp_elig[x] >= min_threshold and x not in excluded_categories}
dpb_elig = list(dbp_elig.keys())

df = df[df['collection'].isin(dpb_elig)]

# Remove nan

df = df.where((pd.notnull(df)), None)

# Drop dupes

df.drop_duplicates(keep='first', inplace=True)

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
pickle.dump( dbp_data, open('../app/static/data/dbp_data.p', 'wb'))

print("Conversion complete!")
