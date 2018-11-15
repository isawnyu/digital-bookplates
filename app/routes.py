from flask import render_template, url_for
import os.path

from app import app
from .data import books

collections = sorted(list(set([book['collection'.lower()] for book in books])))

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Main', collections=collections, books=books, image_loc=image_loc)

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
    return render_template('collection_full.html', title='Main', collections=[collection], books=collection_books)
