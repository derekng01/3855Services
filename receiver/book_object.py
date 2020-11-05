from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import datetime


class Book(Base):
    __tablename__ = "book_list"

    id = Column(Integer, primary_key=True)
    title = Column(String(250), nullable=False)
    author = Column(String(250), nullable=False)
    publisher = Column(String(250), nullable=False)
    genre = Column(String(250), nullable=False)
    isbn_10 = Column(String(10), nullable=False)
    isbn_13 = Column(String(13), nullable=False)
    reader_rating = Column(Integer, nullable=False)
    reader_id = Column(String(250), nullable=False)
    date_created = Column(DateTime, nullable=False)


    def __init__(self, title, author, publisher, genre, isbn_10, isbn_13, reader_rating, reader_id):
        self.title = title
        self.author = author
        self.publisher = publisher
        self.genre = genre
        self.isbn_10 = isbn_10
        self.isbn_13 = isbn_13
        self.reader_rating = reader_rating
        self.reader_id = reader_id
        self.date_created = datetime.datetime.now()


    def to_dict(self):
        dict = {}
        dict['id'] = self.id
        dict['title'] = self.title
        dict['author'] = self.author
        dict['publisher'] = self.publisher
        dict['genre'] = self.genre
        dict['isbn_10'] = self.isbn_10
        dict['isbn_13'] = self.isbn_13
        dict['reader_rating'] = self.reader_rating
        dict['reader_id'] = self.reader_id
        dict['date_created'] = self.date_created

        return dict
