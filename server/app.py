import os

from flask import Flask, jsonify, request, g
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


basedir = os.path.abspath(os.path.dirname(__file__))

DATABASE = 'book.db'
DEBUG = True

DATABASE_PATH = os.path.join(basedir, DATABASE)

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_PATH
SQLALCHEMY_TRACK_MODIFICATIONS = False

app = Flask(__name__)
app.config.from_object(__name__)
db = SQLAlchemy(app)
ma = Marshmallow(app)
CORS(app)


class Book(db.Model):
    __tablename__ = "book"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String)
    status = db.Column(db.String)
    rating = db.Column(db.String)

    def __init__(self, title, author, status, rating):
        self.title = title
        self.author = author
        self.status = status
        self.rating = rating


class BookSchema(ma.ModelSchema):
    class Meta:
        model = Book


book_schema = BookSchema()
books_schema = BookSchema(many=True)


@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    out = books_schema.dump(books).data
    return jsonify({'books': out})


@app.route('/books', methods=['POST'])
def add_book():
    post_data = request.get_json()
    title = post_data.get('title')
    author = post_data.get('author')
    status = post_data.get('status')
    rating = post_data.get('rating')

    if request.method == 'POST':
        new_book = Book(title, author, status, rating)
        db.session.add(new_book)

    db.session.commit()

    return book_schema.jsonify(new_book)


@app.route('/books/<id>', methods=['PUT'])
def update_book(id):
    book = Book.query.get(id)
    post_data = request.get_json()
    book.title = post_data.get('title')
    book.author = post_data.get('author')
    book.status = post_data.get('status')
    book.rating = post_data.get('rating')

    db.session.commit()

    return book_schema.jsonify(book)


@app.route('/books/<id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get(id)
    db.session.delete(book)
    db.session.commit()
    return book_schema.jsonify(book)


if __name__ == '__main__':
    app.run()
