"""
Basic flask API using dictionaries and an sql data base.
Allows user to search for books using id, date published, and author name
--------------------------------------------------
Created by: Derek Marshall
github: https://github.com/DerekMarshall855
"""

import flask
from flask import request, jsonify
import sqlite3

app = flask.Flask(__name__)
app.config["DEBUG"] = True

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

@app.route('/', methods=['GET'])
def home():
    return '''<h1>First Flask API By Derek Marshall</h1>
                <p>This is the first API Derek Marshall has developed in Flask</p>'''

@app.route('/api/v1/resources/books/all', methods=['GET'])
def api_all():
    conn = sqlite3.connect('books.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_books = cur.execute('SELECT * FROM books;').fetchall()
    
    return jsonify(all_books)

@app.errorhandler(404)
def page_not_found(err):
    return "<h1>404</h1><p>Resource could not be found</p>", 404

@app.route('/api/v1/resources/books', methods=['GET'])
def api_id():
    query_params = request.args

    bid = query_params.get('id')
    published = query_params.get('published')
    author = query_params.get('author')

    query = "SELECT * FROM books WHERE"
    to_filter = []

    if not (bid or published or author):
        return page_not_found(404)
    if bid: 
        query += ' id=? AND'
        to_filter.append(bid)
    if published:
        query += ' published=? AND'
        to_filter.append(published)
    if author:
        query += ' author=? AND'
        to_filter.append(author)
    
    query = query[:-4] + ';'  # Remove AND from end of query

    conn = sqlite3.connect('books.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    print(query, to_filter)

    results = cur.execute(query, to_filter).fetchall()

    return jsonify(results)

app.run()