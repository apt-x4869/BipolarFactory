from db import db

class BookModel(db.Model):
    __tablename__ = 'books'

    book_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    author = db.Column(db.String(100))
    amazon_url = db.Column(db.String(500))
    book_genre = db.Column(db.String(100))

    def __init__(self, title, author, amazon_url, book_genre):
        self.title = title
        self.author = author
        self.amazon_url = amazon_url
        self.book_genre = book_genre

    def json(self):
        return {
            'book_id' : self.book_id,
            'title': self.title,
            'author': self.author,
            'amazon_url' : self.amazon_url,
            'book_genre' : self.book_genre
        }
    
    @classmethod
    def find_by_title(cls, title):
        return cls.query.filter_by(title=title).first()

    @classmethod
    def find_by_author(cls, author):
        return cls.query.filter_by(author=author).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()