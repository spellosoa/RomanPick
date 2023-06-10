import cx_Oracle

class OracleDB:
    def __init__(self):
        self.dsn = cx_Oracle.makedsn(host='project-db-cgi.smhrd.com', port=1524, sid='xe')
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

    # 유사도 6개 가져오기
    def select_cosine(self, novel_no):
        query = "select novel_no, rank1, rank2, rank3, rank4, rank5, rank6 from t_cosine where novel_no=:novel_no"
        self.connect()
        cursor = self.connection.cursor()
        cursor.execute(query, novel_no=novel_no)
        self.connection.commit()
        self.disconnect()
        
    def select_novel(self, novel_no):
        query = "select novel_no, title, writer, synopsis from t_novel where novel_no=:novel_no"
    def execute_insert(self,novel):
        query = f"INSERT INTO t_cosine VALUES (:novel_no, :rank1, :rank2, :rank3, :rank4, :rank5, :rank6)"
        self.connect()
        cursor = self.connection.cursor()
        for key,i in novel.items():
            cursor.execute(query, novel_no=i['novel_no'], rank1=i['rank1'], rank2=i['rank2'],rank3= i['rank3'], rank4=i['rank4'],rank5= i['rank5'], rank6=i['rank6'])
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