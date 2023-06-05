import cx_Oracle

class OracleDB:
    def __init__(self):
        self.dsn = cx_Oracle.makedsn(host='project-db-stu.smhrd.com', port=1524, sid='xe')
        self.username = 'campus_c_230531_2'
        self.password = 'smhrd2'
        self.connection = None

    def connect(self):
        self.connection = cx_Oracle.connect(self.username, self.password, self.dsn)

    def disconnect(self):
        if self.connection:
            self.connection.close()

    def execute_query(self, query):
        self.connect()
        cursor = self.connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        self.disconnect()
        return result

    def execute_insert(self, book):
        query = f"INSERT INTO book VALUES (:num, :title, :author, :company, :isbn, :count)"
        self.connect()
        cursor = self.connection.cursor()
        cursor.execute(query, num=book.num, title=book.title, author=book.author,company= book.company, isbn=book.company,count= book.count)
        self.connection.commit()
        self.disconnect()

    def execute_insert1(self, values):
            query = f"INSERT INTO book(num, title) VALUES (:num, :title)"
            self.connect()
            cursor = self.connection.cursor()
            cursor.execute(query, values)
            self.connection.commit()
            self.disconnect()
    # def execute_select(self, table, columns=None, condition=None):
    #     query = f"SELECT {','.join(columns) if columns else '*'} FROM {table}"
    #     if condition:
    #         query += f" WHERE {condition}"
    #     return self.execute_query(query)

    # def execute_delete(self, table, condition):
    #     query = f"DELETE FROM {table} WHERE {condition}"
    #     self.connect()
    #     cursor = self.connection.cursor()
    #     cursor.execute(query)
    #     self.connection.commit()
    #     self.disconnect()