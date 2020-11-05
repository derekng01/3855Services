import mysql.connector

db_conn = mysql.connector.connect(host="localhost", user="mikes_python", password="P@ssw0rd", database="bookkeeper")

db_cursor = db_conn.cursor()

db_cursor = db_conn.cursor()
db_cursor.execute('''
                DROP TABLE reader_list, book_list
''')

db_conn.commit()
db_conn.close()
