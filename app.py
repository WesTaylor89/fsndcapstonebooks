from flask import Flask, request, jsonify, abort
from flask_cors import CORS
from models import Book, db, setup_db, BookSigning
from auth import AuthError, requires_auth
from datetime import datetime


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

    @app.route("/books/author", methods=["POST"])
    @requires_auth(permission="search:books")
    def books_by_author(payload):
        try:
            search_data = request.get_json()['searchTerm']
            books = Book.query.filter(Book.author.ilike(f'%{search_data}%')).all().order_by(
                Book.date_added.desc())
            books_list = []
            for book in books:
                books_list.append(book.book_detail())

            return jsonify({
                'success': True,
                'books': books_list
            }), 200
        except:
            abort(400)

    @app.route("/books/title", methods=["POST"])
    @requires_auth(permission="search:books")
    def books_by_title(payload):
        try:
            search_data = request.get_json()['searchTerm']
            books = Book.query.filter(Book.title.ilike(f'%{search_data}%')).all().order_by(
                Book.date_added.desc())
            books_list = []
            for book in books:
                books_list.append(book.book_detail())

            return jsonify({
                'success': True,
                'books': books_list
            })
        except:
            abort(400)

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

    @app.route("/books/<int:book_id>", methods=["PATCH"])
    @requires_auth(permission="patch:books")
    def edit_book(book_id, payload):
        data = request.get_json()

        chosen_book = Book.query.filter(Book.id == book_id).one_or_none()

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

    @app.route("/books/<int:book_id>", methods=["DELETE"])
    @requires_auth("delete:book")
    def delete_book(book_id, payload):
        try:
            chosen_book = Book.query.filter(Book.id == book_id).one_or_none()

            db.delete(chosen_book)

            return jsonify({
                "success": True,
                "deleted": book_id
            }), 200
        except:
            abort(400)

    @app.route("/books/booksignings", methods=["GET"])
    @requires_auth("search:books")
    def booksignings():
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

    '''
        Error handler for 400
    '''

    @app.errorhandler(400)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
        }), 400

    '''
        Error handler for 404
    '''

    @app.errorhandler(404)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not found"
        }), 404

    '''
        Error handler for AuthError
    '''

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


"""
Populates DB with dummy data
"""

# book1 = Book(title="Harry Potter",
#              author="J.K.Rowling",
#              genre="Fantasy",
#              description="Books about wizards")
#
# book2 = Book(title="Lord of the rings",
#              author="J.R.R.Tolkien",
#              genre="Fantasy",
#              description="Elves, Trolls, Goblins etc")
#
# book3 = Book(title="Jamie's kitchen",
#              author="Jamie Oliver",
#              genre="Cook Book",
#              description="Jamie's favourite recipes")
#
# book4 = Book(title="If it Bleeds",
#              author="Stephen King",
#              genre="Horror",
#              description="4 Stories in 1 book")
#
# book5 = Book(title="History of World War 2",
#              author="Chris McNab",
#              genre="History",
#              description="Events of 1939-1945")
#
# db.session.add(book1)
# db.session.add(book2)
# db.session.add(book3)
# db.session.add(book4)
# db.session.add(book5)
# db.session.commit()

# booksigning1 = BookSigning(start_time="2020-07-20 14:00:00",
#                            book_id="1")
#
# booksigning2 = BookSigning(start_time="2020-07-22 14:00:00",
#                            book_id="2")
#
# booksigning3 = BookSigning(start_time="2020-07-22 16:00:00",
#                            book_id="2")
#
# db.session.add(booksigning1)
# db.session.add(booksigning2)
# db.session.add(booksigning3)
# db.session.commit()
