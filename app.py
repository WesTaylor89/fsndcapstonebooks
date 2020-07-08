import os
from flask import Flask, request, jsonify, abort
from flask_cors import CORS
from models import Book, db, setup_db, BookSigning
from auth import AuthError, requires_auth
from datetime import datetime
from helper_functions import db_dummy_data

""" 
Creates app, contains all endpoints and error handlers
"""

def create_app():
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    CORS(app, resources={r"*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,PATCH')
        return response

    # -----------------------
    # Populates DB with dummy data
    # -----------------------

    # db_dummy_data()

    # -----------------------
    # GET '/home'
    # Home page route that returns all books in the DB
    # -----------------------

    @app.route("/")
    @app.route("/home", methods=["GET"])
    def home():
        try:
            books = Book.query.order_by(Book.date_added.desc())
            books_list = []
            for book in books:
                books_list.append(book.book_detail())

            return jsonify({
                'success': True,
                'books': books_list
            }), 200
        except:
            abort(400)

    # -----------------------
    # POST '/books/author'
    # Returns a list of books with authors who match a search string.
    # -----------------------

    @app.route("/books/author", methods=["POST"])
    @requires_auth(permission="search:books")
    def books_by_author(payload):
        try:
            search_data = request.get_json()['searchTerm']
            books = Book.query.filter(Book.author.ilike(f'%{search_data}%')).all()
            books_list = []
            for book in books:
                books_list.append(book.book_detail())

            return jsonify({
                'success': True,
                'books': books_list
            }), 200
        except:
            abort(400)

    # -----------------------
    # POST '/books/title'
    # Returns a list of books with titles who match a search string.
    # -----------------------

    @app.route("/books/title", methods=["POST"])
    @requires_auth(permission="search:books")
    def books_by_title(payload):
        try:
            search_data = request.get_json()['searchTerm']
            books = Book.query.filter(Book.title.ilike(f'%{search_data}%')).all()
            books_list = []
            for book in books:
                books_list.append(book.book_detail())

            return jsonify({
                'success': True,
                'books': books_list
            })
        except:
            abort(400)

    # -----------------------
    # POST '/books/new'
    # Posts a new book to the database
    # -----------------------

    @app.route("/books/new", methods=["POST"])
    @requires_auth(permission="post:new_book")
    def new_book(payload):
        data = request.get_json()
        try:
            new = Book(title=data['title'],
                       author=data['author'],
                       genre=data['genre'],
                       description=data['description'])
            db.session.add(new)
            db.session.commit()

            return jsonify({
                'success': True,
                'book': new.book_detail()
            }), 200
        except:
            abort(400)

    # -----------------------
    # PATCH '/books/<int:book_id>'
    # Updates a chosen book in the database with new data.
    # -----------------------

    @app.route("/books/<int:book_id>", methods=["PATCH"])
    @requires_auth(permission="patch:books")
    def edit_book(payload, book_id):
        data = request.get_json()

        chosen_book = Book.query.filter(Book.id == book_id).one_or_none()
        if chosen_book is None:
            abort(404)

        try:
            new_title = data['title']
            new_author = data['author']
            new_genre = data['genre']
            new_description = data['description']
            if new_title:
                chosen_book.title = new_title
            elif new_author:
                chosen_book.author = new_author
            elif new_genre:
                chosen_book.genre = new_genre
            elif new_description:
                chosen_book.description = new_description

            db.session.commit()

            updated_book = Book.query.filter(Book.id == book_id).first()

            return jsonify({
                "success": True,
                "book": [updated_book.book_detail()]
            }), 200
        except:
            abort(400)

    # -----------------------
    # DELETE '/books/<int:book_id>'
    # Deletes the selected book from the DB
    # -----------------------

    @app.route("/books/<int:book_id>", methods=["DELETE"])
    @requires_auth(permission="delete:book")
    def delete_book(payload, book_id):
        try:
            chosen_book = Book.query.filter(Book.id == book_id).one_or_none()
            if chosen_book is None:
                abort(404)

            db.session.delete(chosen_book)
            db.session.commit()

            return jsonify({
                "success": True,
                "deleted": book_id
            }), 200
        except:
            abort(400)

    # -----------------------
    # GET '/books/booksignings'
    # Returns a list of upcoming book signings. Returns author, title and start time.
    # -----------------------

    @app.route("/books/booksignings", methods=["GET"])
    @requires_auth("search:books")
    def booksignings(payload):
        try:
            upcoming_booksignings_obj = db.session.query(BookSigning).join(Book)\
                .filter(BookSigning.start_time > datetime.now()).all()
            # print(upcoming_booksignings_obj)

            upcoming_booksignings = []
            for booksigning in upcoming_booksignings_obj:
                upcoming = ({
                    "book_title": booksigning.book.title,
                    "book_author": booksigning.book.author,
                    "booksigning_start_time": booksigning.start_time
                })
                upcoming_booksignings.append(upcoming)

            # print(upcoming_booksignings)

            return jsonify({
                "success": True,
                "upcoming_signings": upcoming_booksignings
            }), 200
        except:
            return abort(400)

    # -----------------------
    # Error handler for 400 error
    # -----------------------

    @app.errorhandler(400)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
        }), 400

    # -----------------------
    # Error handler for 404 error
    # -----------------------

    @app.errorhandler(404)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not found"
        }), 404

    # -----------------------
    # Error handler for auth error
    # -----------------------

    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error['description']
        }), error.status_code

    return app


"""
Run App
"""

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
