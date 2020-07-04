from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

'''
setup_db(app)
    Sets up the DB
'''

def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = \
        'postgresql://Wes:password@localhost:5432/fsndcapstone'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    # db.create_all()


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), unique=True, nullable=False)
    author = db.Column(db.String(), nullable=False)
    genre = db.Column(db.String(), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    date_added = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)

    def book_detail(self):
        return {
            'title': self.title,
            'author': self.author,
            'genre': self.author,
            'description': self.description
        }


# class Comments(db.Model):
