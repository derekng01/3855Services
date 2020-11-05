from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import datetime


class Reader(Base):

    __tablename__ = "reader_list"

    database_id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    reader_id = Column(String(250), nullable=False)
    date_created = Column(DateTime, nullable=False)


    def __init__(self, name, reader_id):
        self.name = name
        self.reader_id = reader_id
        self.date_created = datetime.datetime.now()


    def to_dict(self):
        dict = {}
        dict['database_id'] = self.database_id
        dict['name'] = self.name
        dict['reader_id'] = self.reader_id
        dict['date_created'] = self.date_created

        return dict
