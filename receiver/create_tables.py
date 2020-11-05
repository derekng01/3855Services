import sqlite3

conn = sqlite3.connect('bookkeeper.sqlite')

c = conn.cursor()

c.execute(
    '''
          CREATE TABLE book_list
          (id INTEGER PRIMARY KEY AUTOINCREMENT , 
           title VARCHAR(250) NOT NULL,
           author VARCHAR(250) NOT NULL,
           publisher VARCHAR(250) NOT NULL,
           genre VARCHAR(250) NOT NULL,
           isbn_10 VARCHAR(10) NOT NULL,
           isbn_13 VARCHAR(13) NOT NULL,
           reader_rating INTEGER NOT NULL,
           reader_id VARCHAR(250) NOT NULL,
           date_created VARCHAR(100) NOT NULL

    )
    '''
)

c.execute('''
          CREATE TABLE reader_list
          (reader_id INTEGER PRIMARY KEY AUTOINCREMENT , 
           name VARCHAR(250) NOT NULL,
           date_created VARCHAR(100) NOT NULL
           )
          '''
          )


conn.commit()
conn.close()
