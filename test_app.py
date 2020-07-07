import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Book, BookSigning
from dotenv import load_dotenv

# load_dotenv()

# user_token = os.getenv('user_token')
# admin_token = os.getenv('admin_token')
user_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InB6UWFBZHFCbXhmTzdMRjdyRmt6QyJ9.eyJpc3MiOiJodHRwczovL3d0NTk3LmV1LmF1dGgwLmNvbS8iLCJzdWIiOiJGeTJnV0MxazBKRHFTUlJBbDlxVTZCQ0hzWEJybXp2dUBjbGllbnRzIiwiYXVkIjoiRlNORENhcHN0b25lIiwiaWF0IjoxNTk0MTQ5MjY2LCJleHAiOjE1OTQyMzU2NjYsImF6cCI6IkZ5MmdXQzFrMEpEcVNSUkFsOXFVNkJDSHNYQnJtenZ1Iiwic2NvcGUiOiJzZWFyY2g6Ym9va3MiLCJndHkiOiJjbGllbnQtY3JlZGVudGlhbHMiLCJwZXJtaXNzaW9ucyI6WyJzZWFyY2g6Ym9va3MiXX0.0-TBQFSCHyUAl84VJVCH6dfJbaufekXXh73uIEp9FCMWnanpeqjA61VqWZrw6e1v3_mno_yt1V7arW4HQgWZudfBYea7_Q2wtkzKTvYp1xPvPKEabhZYpUqKUc7_-Nk3S9uyD0QsolzWOuYVgSUDGlxGystLO6vVigIFjqScYUtxPG7Yqq8hvATUHu-thFGVrFwFWUsxOv7syI3FQ1dIOMfVBENFpYdBa8p2y3aw8aIzGlvQGV3kZpusfEHerlaIQH8KGqnSuv4PLqnWShIq0Ni7hacLXGM4DeUqOmcUUWgR1gBu50OozRfcUZkKk8XhYzDBZQZRNyBCmaMXdGMqJQ"
admin_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InB6UWFBZHFCbXhmTzdMRjdyRmt6QyJ9.eyJpc3MiOiJodHRwczovL3d0NTk3LmV1LmF1dGgwLmNvbS8iLCJzdWIiOiJGeTJnV0MxazBKRHFTUlJBbDlxVTZCQ0hzWEJybXp2dUBjbGllbnRzIiwiYXVkIjoiRlNORENhcHN0b25lIiwiaWF0IjoxNTk0MTQ4NzA1LCJleHAiOjE1OTQyMzUxMDUsImF6cCI6IkZ5MmdXQzFrMEpEcVNSUkFsOXFVNkJDSHNYQnJtenZ1Iiwic2NvcGUiOiJzZWFyY2g6Ym9va3MgcG9zdDpuZXdfYm9vayBkZWxldGU6Ym9vayBwYXRjaDpib29rcyIsImd0eSI6ImNsaWVudC1jcmVkZW50aWFscyIsInBlcm1pc3Npb25zIjpbInNlYXJjaDpib29rcyIsInBvc3Q6bmV3X2Jvb2siLCJkZWxldGU6Ym9vayIsInBhdGNoOmJvb2tzIl19.c_ZHCMtpV8-tXQOurqo7Ga084DHjdu6y-HQ1RK02MW2RJl3T6dvVH5F2hs800oB_4rd4ADrkatFdCCZLUPR8NggEwOe-92u1r_jgngv4S834BFR9vPMMDeYjvK29nZT2gfSDRK_UsiIvKxn4oo9uh8Hw-uBD_N2oCXgv9whG5YptpBBwTmJui8NwD2wpQeI14BYCNnvO68Ncnicn5dKL5d1_ZZSqoaGv1fXuJJIojUYRRlbrdKMEFkg41NtFQg7zCU8EkZaUxDjTK5jtTSr49kZrjjgqnTQAEJIyp36xKraLC5pTo8VqKcvkaLjTfCYQplpOMNDlLbUtcbpGyjHeXA"

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

            self.db.session.add(book1)
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
        res = self.client().delete('/books/1')

        self.assertEqual(res.status_code, 401)
        self.assertEqual(res.get_json()['success'], False)
        self.assertEqual(res.get_json()['message'],
                         "Authorization header is expected.")

    def test_delete_book_user(self):
        res = self.client().delete('/books/1',
                                   headers=self.user_token_headers)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(res.get_json()['success'], False)
        self.assertEqual(res.get_json()['message'], "Permission not found")

    def test_delete_book_admin(self):
        res = self.client().delete('/books/1',
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


if __name__ == "__main__":
    unittest.main()
