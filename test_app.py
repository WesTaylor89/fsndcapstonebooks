import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Book, BookSigning
from dotenv import load_dotenv

load_dotenv()

# user_token = os.getenv('user_token')
# admin_token = os.getenv('admin_token')
user_token='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InB6UWFBZHFCbXhmTzdMRjdyRmt6QyJ9.eyJpc3MiOiJodHRwczovL3d0NTk3LmV1LmF1dGgwLmNvbS8iLCJzdWIiOiJGeTJnV0MxazBKRHFTUlJBbDlxVTZCQ0hzWEJybXp2dUBjbGllbnRzIiwiYXVkIjoiRlNORENhcHN0b25lIiwiaWF0IjoxNTk0MDU2NTI1LCJleHAiOjE1OTQxNDI5MjUsImF6cCI6IkZ5MmdXQzFrMEpEcVNSUkFsOXFVNkJDSHNYQnJtenZ1Iiwic2NvcGUiOiJzZWFyY2g6Ym9va3MiLCJndHkiOiJjbGllbnQtY3JlZGVudGlhbHMiLCJwZXJtaXNzaW9ucyI6WyJzZWFyY2g6Ym9va3MiXX0.SQ59qjH7aYJXJneahYoqLR2U-QjxsDsuV1HXFCfuvPOAZetX0ANWy9VAipH9gQhkUd3osBKMryrmPzfq62JdpVBioKGfTrhlJRIxtDmcCbyF1CQfYGJIKQECjav_EEKWvbalpL2UUX4zJyzvJ866wc7ZpTNxglVXkhCWlPrSZaihPTqguEpzRm6fDo9zFCuubiMGrY-YUJ1FiC1Y98ZVXRKKttCc2m4Tqr4l5h8z0f6zCKEf3Azgr4foehZH9PzmOlyF_SDwoY0KQnFut5EHuLFnSXxRFahhy-YKdfBP2CffPtkDaNipIGBSMSA_tmMSkoipBtuicRawV_eW3iSJ0A'
admin_token='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InB6UWFBZHFCbXhmTzdMRjdyRmt6QyJ9.eyJpc3MiOiJodHRwczovL3d0NTk3LmV1LmF1dGgwLmNvbS8iLCJzdWIiOiJGeTJnV0MxazBKRHFTUlJBbDlxVTZCQ0hzWEJybXp2dUBjbGllbnRzIiwiYXVkIjoiRlNORENhcHN0b25lIiwiaWF0IjoxNTk0MDU2NDc2LCJleHAiOjE1OTQxNDI4NzYsImF6cCI6IkZ5MmdXQzFrMEpEcVNSUkFsOXFVNkJDSHNYQnJtenZ1Iiwic2NvcGUiOiJzZWFyY2g6Ym9va3MgcG9zdDpuZXdfYm9vayBkZWxldGU6Ym9vayBwYXRjaDpib29rcyIsImd0eSI6ImNsaWVudC1jcmVkZW50aWFscyIsInBlcm1pc3Npb25zIjpbInNlYXJjaDpib29rcyIsInBvc3Q6bmV3X2Jvb2siLCJkZWxldGU6Ym9vayIsInBhdGNoOmJvb2tzIl19.FQELMkInT50oQ7dq8t92lpXc9sVJjUlGD7WfZzz14K6sGOvjBX1cTcqqDBpbE4Mf9WnOdCSEpHjpzQvPWEztJ7_Ohl_WN0Ri8yEGkI1uiK-2KMH70P2mNM2XiYWwFtiRf1O_eZSAKMmCFhb3hEMMio_nIA_dcqnOORujw_zOCvY8U6_l3hJxJOS5Psdf02DZeLZl1WgkIXi42vFZOkA6vPpovu9XDSJQoN6vEL1NfWnF8zXw9YHbOvNz1rzUnXKX9cvZz1JpfTW35HkmORdqUjNZUef1ieFvgA9tPpxFn5GD6-Iuiuq-iaxu6vJxw9OIY-aC5AM4Wi1ipkNnvb5Uqw'

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

            # book1 = Book(title="Harry Potter",
            #              author="JKRowling",
            #              genre="Fantasy",
            #              description="Books about wizards")
            #
            # self.db.session.add(book1)
            # self.db.session.commit()
            #
            # booksigning = BookSigning(start_time="2020-23-07 14:00:00",
            #                           book_id=1)
            #
            # self.db.session.add(booksigning)
            # self.db.session.commit()

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

    def test_new_book(self):
        res = self.client().post('/books/new', json={self.new_book})

        self.assertEqual(res.status_code, 401)
        self.assertEqual(res.get_json()['success'], False)
        self.assertEqual(res.get_json()['message'],
                         "Authorization header is expected.")

    def test_new_book_user(self):
        res = self.client().post('/books/new',
                                 headers=self.user_token_headers,
                                 json={self.new_book})

        self.assertEqual(res.status_code, 401)
        self.assertEqual(res.get_json()['success'], False)
        self.assertEqual(res.get_json()['message'], "Inadequate permissions.")

    def test_new_book_admin(self):
        res = self.client().post('/books/new',
                                 headers=self.admin_token_headers,
                                 json={self.new_book})

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()['success'], True)

    # -----------------------
    # PATCH '/books/<int:book_id>'
    # -----------------------

    def test_edit_book(self):
        res = self.client().patch('/books/1', json={self.edit_book})

        self.assertEqual(res.status_code, 401)
        self.assertEqual(res.get_json()['success'], False)
        self.assertEqual(res.get_json()['message'],
                         "Authorization header is expected.")

    def test_edit_book_user(self):
        res = self.client().patch('/books/1',
                                  headers=self.user_token_headers,
                                  json={self.edit_book})

        self.assertEqual(res.status_code, 401)
        self.assertEqual(res.get_json()['success'], False)
        self.assertEqual(res.get_json()['message'], "Inadequate permissions.")

    def test_edit_book_admin(self):
        res = self.client().patch('/books/1',
                                  headers=self.admin_token_headers,
                                  json={self.edit_book})

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
        self.assertEqual(res.get_json()['message'], "Inadequate permissions.")

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
