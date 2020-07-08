import os
import unittest
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Book, BookSigning
from dotenv import load_dotenv

load_dotenv()

""" 
JWT's for authentication
"""

user_token = os.getenv('user_token')
admin_token = os.getenv('admin_token')


""" 
Unittest test class

---IMPORTANT---
To successfully run tests uncomment db.drop_all() in models.py. Comment this
out afterwards to run app in local environment.
"""

class BookShopAppTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.user_token_headers = {"Authorization": "Bearer {}".format(user_token)}
        self.admin_token_headers = {"Authorization": "Bearer {}".format(admin_token)}
        self.database_name = 'fsndcapstone_test'
        self.database_path = "postgres://Wes:password@localhost:5432/{}".format(
            self.database_name)
        setup_db(self.app, self.database_path)

        self.new_book = {
            'title': 'Harry1 Potter',
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

            # populate test db with dummy data

            book1 = Book(title="Harry Potter",
                         author="JKRowling",
                         genre="Fantasy",
                         description="Books about wizards")

            book2 = Book(title="Zarry Potter",
                         author="JKRowling",
                         genre="Fantasy",
                         description="Books about wizards")

            self.db.session.add(book1)
            self.db.session.add(book2)
            self.db.session.commit()

            booksigning = BookSigning(start_time="2020-07-22 14:00:00",
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
        # data = json.loads(res.data)

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
                                 json={"searchTerm": "JKRowling"})

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()['success'], True)

    def test_books_by_author_admin(self):
        res = self.client().post('/books/author',
                                 headers=self.admin_token_headers,
                                 json={"searchTerm": "JKRowling"})

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
                                 json={"searchTerm": "Harry"})

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()['success'], True)

    # -----------------------
    # POST '/books/new'
    # -----------------------

    def test_new_book(self):
        res = self.client().post('/books/new', json=self.new_book)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(res.get_json()['success'], False)
        self.assertEqual(res.get_json()['message'],
                         "Authorization header is expected.")

    def test_new_book_user(self):
        res = self.client().post('/books/new',
                                 headers=self.user_token_headers,
                                 json=self.new_book)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(res.get_json()['success'], False)
        self.assertEqual(res.get_json()['message'], "Permission not found")

    def test_new_book_admin(self):
        res = self.client().post('/books/new',
                                 headers=self.admin_token_headers,
                                 json=self.new_book)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()['success'], True)

    # -----------------------
    # PATCH '/books/<int:book_id>'
    # -----------------------

    def test_edit_book(self):
        res = self.client().patch('/books/1', json=self.edit_book)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(res.get_json()['success'], False)
        self.assertEqual(res.get_json()['message'],
                         "Authorization header is expected.")

    def test_edit_book_user(self):
        res = self.client().patch('/books/1',
                                  headers=self.user_token_headers,
                                  json=self.edit_book)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(res.get_json()['success'], False)
        self.assertEqual(res.get_json()['message'], "Permission not found")

    def test_edit_book_admin(self):
        res = self.client().patch('/books/1',
                                  headers=self.admin_token_headers,
                                  json=self.edit_book)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()['success'], True)

    # -----------------------
    # DELETE '/books/<int:book_id>'
    # -----------------------

    def test_delete_book(self):
        res = self.client().delete('/books/2')

        self.assertEqual(res.status_code, 401)
        self.assertEqual(res.get_json()['success'], False)
        self.assertEqual(res.get_json()['message'],
                         "Authorization header is expected.")

    def test_delete_book_user(self):
        res = self.client().delete('/books/2',
                                   headers=self.user_token_headers)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(res.get_json()['success'], False)
        self.assertEqual(res.get_json()['message'], "Permission not found")

    def test_delete_book_admin(self):
        res = self.client().delete('/books/2',
                                   headers=self.admin_token_headers)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()['success'], True)

    # -----------------------
    # GET '/books/booksignings'
    # -----------------------

    def test_get_booksignings(self):
        res = self.client().get('/books/booksignings')

        self.assertEqual(res.status_code, 401)
        self.assertEqual(res.get_json()['success'], False)
        self.assertEqual(res.get_json()['message'],
                         "Authorization header is expected.")

    def test_get_booksignings_user(self):
        res = self.client().get('/books/booksignings',
                                headers=self.user_token_headers)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()['success'], True)

    def test_get_booksignings_admin(self):
        res = self.client().get('/books/booksignings',
                                headers=self.admin_token_headers)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()['success'], True)


""" 
Run tests
"""

if __name__ == "__main__":
    unittest.main()
