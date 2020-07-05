from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

'''
setup_db(app)
    Sets up the DB
'''

def setup_db(app):
    # Production DB
    app.config["SQLALCHEMY_DATABASE_URI"] = \
        'postgres://alfdtfgfwhhwoy:b780cc7da8953139ad45f56e0257301d47caceec8' \
        'f53b1cfb505967d2d84008a@ec2-52-202-146-43.compute-1.amazonaws.com:5432/d2ivnk6gdrr6q6'

    # Local DB
    # app.config["SQLALCHEMY_DATABASE_URI"] = \
    #     'postgres://Wes:password@localhost:5432/fsndcapstone'

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), unique=True, nullable=False)
    author = db.Column(db.String(), nullable=False)
    genre = db.Column(db.String(), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    date_added = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)

    book_signings = db.relationship('BookSigning', backref='book', lazy=True)

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

