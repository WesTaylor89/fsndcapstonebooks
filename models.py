import os
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()
db = SQLAlchemy()

database_path = os.getenv('DATABASE_URL')
database_path = 'postgres://Wes:password@localhost:5432/fsndcapstone'

# ---------------------------------------------------------
# setup_db(app)
#    Sets up the DB
# ---------------------------------------------------------

def setup_db(app, db_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = db_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)

    # Uncomment db.drop_all() if running unittests
    # db.drop_all()
    db.create_all()


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), unique=True, nullable=False)
    author = db.Column(db.String(), nullable=False)
    genre = db.Column(db.String(), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    date_added = db.Column(db.DateTime(), nullable=False,
                           default=datetime.utcnow)

    book_signings = db.relationship('BookSigning', backref='book', lazy=True)

    def __init__(self, title, author, genre, description):
        self.title = title
        self.author = author
        self.genre = genre
        self.description = description

    def book_detail(self):
        return {
            'title': self.title,
            'author': self.author,
            'genre': self.author,
            'description': self.description
        }


class BookSigning(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime(), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)

    def __init__(self, start_time, book_id):
        self.start_time = start_time
        self.book_id = book_id
