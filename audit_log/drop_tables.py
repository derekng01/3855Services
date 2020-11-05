import sqlite3

conn = sqlite3.connect('bookkeeper.sqlite')

c = conn.cursor()
c.execute('''
          DROP TABLE book_list
          ''')

conn.commit()
conn.close()