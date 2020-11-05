import mysql.connector

db_conn = mysql.connector.connect(host="python3855lab5.eastus.cloudapp.azure.com", user="mikes_python", password="P@ssw0rd", database="events", port=3306)

db_cursor = db_conn.cursor()



db_cursor.execute(
    '''
          CREATE TABLE book_list
          (id INT NOT NULL AUTO_INCREMENT, 
           title VARCHAR(250) NOT NULL,
           author VARCHAR(250) NOT NULL,
           publisher VARCHAR(250) NOT NULL,
           genre VARCHAR(250) NOT NULL,
           isbn_10 VARCHAR(10) NOT NULL,
           isbn_13 VARCHAR(13) NOT NULL,
           reader_rating INTEGER NOT NULL,
           reader_id VARCHAR(250) NOT NULL,
           date_created VARCHAR(100) NOT NULL,
           CONSTRAINT book_list_pk PRIMARY KEY (id))
    '''
)

db_cursor.execute('''
          CREATE TABLE reader_list
          (database_id INT NOT NULL AUTO_INCREMENT, 
           name VARCHAR(250) NOT NULL,
           reader_id VARCHAR(250)NOT NULL,
           date_created VARCHAR(100) NOT NULL,
           CONSTRAINT reader_list_pk PRIMARY KEY (database_id))   
          '''
          )

db_conn.commit()
db_conn.close()
