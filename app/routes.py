from flask import render_template, url_for
import os.path

from app import app
# from .data import books

import pickle


import os

print(os.getcwd())

books = pickle.load(open('app/static/data/dbp_data.p', 'rb'))
images_ = [file.split('.')[0] for file in os.listdir('app/static/img') if file.endswith('.png')]

collection_names = sorted(list(set([book['collection'.lower()] for book in books])))

collections = []

for name in collection_names:
    collection = dict()
    collection['name'] = name
    if name.lower() in images_:
        collection['image'] = 'img/'+name+'.png'
    else:
        collection['image'] = 'img/generic.png'
    collections.append(collection)


@app.route('/')
@app.route('/index')
def index():
    # return render_template('index.html', title='Main', collections=collections, books=books, image_loc=image_loc)
    return render_template('index.html', title='Main', collections=collections)


@app.route('/<collection>')
def book_collections(collection):
    collection_books = [book for book in books if book['collection'].lower()==collection.lower()]
    image = f'{collection}.png'
    image_loc = url_for('static', filename=f'img/{image}')
    if not os.path.isfile(app.root_path+image_loc):
        image_loc = None
    return render_template('collection.html', title='Main', collections=[collection], books=collection_books, image_loc=image_loc)

@app.route('/full/<collection>')
def book_collections_full(collection):
    collection_books = [book for book in books if book['collection'].lower()==collection.lower()]
    print(type(collection_books[0]['author']))
    return render_template('collection_full.html', title='Main', collections=[collection], books=collection_books)
