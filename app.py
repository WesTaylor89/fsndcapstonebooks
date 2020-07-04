from flask import Flask, request, jsonify
from flask_cors import CORS
from models import Book, db, setup_db
from auth import AuthError, requires_auth


def create_app():
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

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
            return jsonify({
                "success": False,
                "error": "Bad request"
            }), 400

    @app.route("/books/<string:author>", methods=["GET"])
    @requires_auth(permission="search:books")
    def books_by_author(author, payload):
        try:
            books = Book.query.filter(Book.author == author).order_by(
                Book.date_added.desc())
            books_list = []
            for book in books:
                books_list.append(book.book_detail())

            return jsonify({
                'success': True,
                'books': books_list
            }), 200
        except:
            return jsonify({
                "success": False,
                "error": "Bad request"
            }), 400

    @app.route("/books/<string:title>", methods=["GET"])
    @requires_auth(permission="search:books")
    def books_by_title(title, payload):
        try:
            books = Book.query.filter(Book.title == title).order_by(
                Book.date_added.desc())
            books_list = []
            for book in books:
                books_list.append(book.book_detail())

            return jsonify({
                'success': True,
                'books': books_list
            })
        except:
            return jsonify({
                "success": False,
                "error": "Bad request"
            }), 400

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
            return jsonify({
                "success": False,
                "error": "Bad request"
            }), 400

    @app.route("/books/<int:book_id>", methods=["PATCH"])
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
            return jsonify({
                "success": False,
                "error": "Bad request"
            }), 400

    @app.route("/books/<int:book_id>", methods=["DELETE"])
    def delete_book(book_id, payload):
        try:
            chosen_book = Book.query.filter(Book.id == book_id).one_or_none()

            db.delete(chosen_book)

            return jsonify({
                "success": True,
                "deleted": book_id
            }), 200
        except:
            return jsonify({
                "success": False,
                "error": "Bad request"
            }), 400

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


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
