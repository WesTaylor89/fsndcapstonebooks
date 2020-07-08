from models import Book, BookSigning
from models import db

"""
Populates DB with dummy data
"""

def db_dummy_data():
    book1 = Book(title="Harry Potter",
                 author="J.K.Rowling",
                 genre="Fantasy",
                 description="Books about wizards")

    book2 = Book(title="Lord of the rings",
                 author="J.R.R.Tolkien",
                 genre="Fantasy",
                 description="Elves, Trolls, Goblins etc")

    book3 = Book(title="Jamie's kitchen",
                 author="Jamie Oliver",
                 genre="Cook Book",
                 description="Jamie's favourite recipes")

    book4 = Book(title="If it Bleeds",
                 author="Stephen King",
                 genre="Horror",
                 description="4 Stories in 1 book")

    book5 = Book(title="History of World War 2",
                 author="Chris McNab",
                 genre="History",
                 description="Events of 1939-1945")

    db.session.add(book1)
    db.session.add(book2)
    db.session.add(book3)
    db.session.add(book4)
    db.session.add(book5)
    db.session.commit()

    booksigning1 = BookSigning(start_time="2020-07-20 14:00:00",
                               book_id="1")

    booksigning2 = BookSigning(start_time="2020-07-22 14:00:00",
                               book_id="2")

    booksigning3 = BookSigning(start_time="2020-07-22 16:00:00",
                               book_id="2")

    db.session.add(booksigning1)
    db.session.add(booksigning2)
    db.session.add(booksigning3)
    db.session.commit()
