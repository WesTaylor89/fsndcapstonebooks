import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Book, BookSigning
from dotenv import load_dotenv

load_dotenv()

user_token = os.getenv('user_token')
admin_token = os.getenv('admin_token')


class BookShopAppTestCase(unittest.TestCase):

    def setup(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.user_token_headers = {
            "Authorization": "Bearer {}".format(user_token)}
        self.admin_token_headers = {
            "Authorization": "Bearer {}".format(admin_token)}
        self.database_name = 'bookshop_test'
        self.database_path = "postgres://Wes:password@localhost:5432/{}".format(
            self.database_name)
        setup_db(self.app, self.database_path)

        self.new_book = {
            'title': 'Harry Potter',
            'author': 'JKRowling',
            'genre': 'Fantasy',
            'description': 'Books'
        }

        self.edit_book = {
            'title': 'Barry Potter',
            'author': 'JKRowling',
            'genre': 'Fantasy',
            'description': 'Books'
        }

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)

            self.db.create_all()

            book1 = Book(title="Harry Potter",
                         author="JKRowling",
                         genre="Fantasy",
                         description="Books about wizards")

            self.db.session.add(book1)
            self.db.session.commit()

            booksigning = BookSigning(start_time="2020-23-07 14:00:00",
                                      book_id=1)

            self.db.session.add(booksigning)
            self.db.session.commit()

    def tearDown(self):
        pass

    # -----------------------
    # GET '/home'
    # -----------------------

    def test_home(self):
        res = self.client().get('/home')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()['success'], True)

    # -----------------------
    # POST '/books/author'
    # -----------------------

    def test_books_by_author_no_header(self):
        res = self.client().post('/books/author', json={"searchTerm": "JK"})

        self.assertEqual(res.status_code, 401)
        self.assertEqual(res.get_json()['success'], False)
        self.assertEqual(res.get_json()['message'],
                         "Authorization header is expected.")

    def test_books_by_author_user(self):
        res = self.client().post('/books/author',
                                 headers=self.user_token_headers,
                                 json={"searchTerm": "JK"})

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()['success'], True)

    def test_books_by_author_admin(self):
        res = self.client().post('/books/author',
                                 headers=self.admin_token_headers,
                                 json={"searchTerm": "JK"})

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()['success'], True)

    # -----------------------
    # POST '/books/title'
    # -----------------------

    def test_books_by_title_no_header(self):
        res = self.client().post('/books/author', json={"searchTerm": "Harry"})

        self.assertEqual(res.status_code, 401)
        self.assertEqual(res.get_json()['success'], False)
        self.assertEqual(res.get_json()['message'],
                         "Authorization header is expected.")

    def test_books_by_title_user(self):
        res = self.client().post('/books/author',
                                 headers=self.user_token_headers,
                                 json={"searchTerm": "Harry"})

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()['success'], True)

    def test_books_by_title_admin(self):
        res = self.client().post('/books/author',
                                 headers=self.admin_token_headers,
                                 json={"searchTerm": "JK"})

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()['success'], True)

    # -----------------------
    # POST '/books/new'
    # -----------------------

    def new_book(self):
        res = self.client().post('/books/new', json={self.new_book})

        self.assertEqual(res.status_code, 401)
        self.assertEqual(res.get_json()['success'], False)
        self.assertEqual(res.get_json()['message'],
                         "Authorization header is expected.")

    def new_book_user(self):
        res = self.client().post('/books/new',
                                 headers=self.user_token_headers,
                                 json={self.new_book})

        self.assertEqual(res.status_code, 401)
        self.assertEqual(res.get_json()['success'], False)
        self.assertEqual(res.get_json()['message'], "Inadequate permissions.")

    def new_book_admin(self):
        res = self.client().post('/books/new',
                                 headers=self.admin_token_headers,
                                 json={self.new_book})

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()['success'], True)

    # -----------------------
    # PATCH '/books/<int:book_id>'
    # -----------------------

    def edit_book(self):
        res = self.client().patch('/books/1', json={self.edit_book})

        self.assertEqual(res.status_code, 401)
        self.assertEqual(res.get_json()['success'], False)
        self.assertEqual(res.get_json()['message'],
                         "Authorization header is expected.")

    def edit_book_user(self):
        res = self.client().patch('/books/1',
                                  headers=self.user_token_headers,
                                  json={self.edit_book})

        self.assertEqual(res.status_code, 401)
        self.assertEqual(res.get_json()['success'], False)
        self.assertEqual(res.get_json()['message'], "Inadequate permissions.")

    def edit_book_admin(self):
        res = self.client().patch('/books/1',
                                  headers=self.admin_token_headers,
                                  json={self.edit_book})

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()['success'], True)

    # -----------------------
    # DELETE '/books/<int:book_id>'
    # -----------------------

    def delete_book(self):
        res = self.client().delete('/books/1')

        self.assertEqual(res.status_code, 401)
        self.assertEqual(res.get_json()['success'], False)
        self.assertEqual(res.get_json()['message'],
                         "Authorization header is expected.")

    def delete_book_user(self):
        res = self.client().delete('/books/1',
                                   headers=self.user_token_headers)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(res.get_json()['success'], False)
        self.assertEqual(res.get_json()['message'], "Inadequate permissions.")

    def delete_book_admin(self):
        res = self.client().delete('/books/1',
                                   headers=self.admin_token_headers)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()['success'], True)

    # -----------------------
    # GET '/books/booksignings'
    # -----------------------

    def get_booksignings(self):
        res = self.client().get('/books/booksignings')

        self.assertEqual(res.status_code, 401)
        self.assertEqual(res.get_json()['success'], False)
        self.assertEqual(res.get_json()['message'],
                         "Authorization header is expected.")

    def get_booksignings_user(self):
        res = self.client().get('/books/booksignings',
                                headers=self.user_token_headers)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(res.get_json()['success'], True)

    def get_booksignings_admin(self):
        res = self.client().get('/books/booksignings',
                                headers=self.admin_token_headers)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()['success'], True)


if __name__ == "__main__":
    unittest.main()
