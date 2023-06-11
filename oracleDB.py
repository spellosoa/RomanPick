import cx_Oracle

class OracleDB:
    def __init__(self):
        self.dsn = cx_Oracle.makedsn(host='project-db-cgi.smhrd.com', port=1524, sid='xe')
        self.username = 'campus_c_230531_2'
        self.password = 'smhrd2'
        self.connection = None
    def __del__(self):
        self.disconnect()
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

    # 소설 제목으로 정보 가져오기
    def novel_nm_select(self, novel_nm):
        query = "select novel_no, novel_nm, novel_writer, novel_synopsis, novel_cover from t_novel where novel_nm=:novel_nm"
        self.connect()
        cursor = self.connection.cursor()
        cursor.execute(query, novel_nm=novel_nm)
        result = cursor.fetchone()
        self.disconnect()
        return result
    
    # 유사도 6개 가져오기
    def select_cosine(self, novel_no):
        query = "select novel_no, rank1, rank2, rank3, rank4, rank5, rank6 from t_cosine where novel_no=:novel_no"
        self.connect()
        cursor = self.connection.cursor()
        cursor.execute(query, novel_no=novel_no)
        result = cursor.fetchone()
        self.disconnect()
        data=[]
        if result is not None:
            data = {
                'rank1':result[1],
                'rank2':result[2],
                'rank3':result[3],
                'rank4':result[4],
                'rank5':result[5],
                'rank6':result[6]
            }
        return data
        
    def select_novel(self, novel_no):
        query = "select novel_no, novel_nm, novel_writer, novel_synopsis, novel_cover from t_novel where novel_no=:novel_no"
        self.connect()
        cursor = self.connection.cursor()
        cursor.execute(query, novel_no=novel_no)
        result = cursor.fetchone()
        self.disconnect()
        if result is not None:
            data = {
                'novel_no':result[0],
                'novel_nm':result[1],
                'novel_writer':result[2],
                'novel_synopsis':result[3],
                'novel_cover':result[4]
            }
        return data
        
    def execute_insert(self,novel):
        query = f"INSERT INTO t_cosine VALUES (:novel_no, :rank1, :rank2, :rank3, :rank4, :rank5, :rank6)"
        self.connect()
        cursor = self.connection.cursor()
        for key,i in novel.items():
            cursor.execute(query, novel_no=i['novel_no'], rank1=i['rank1'], rank2=i['rank2'],rank3= i['rank3'], rank4=i['rank4'],rank5= i['rank5'], rank6=i['rank6'])
        self.connection.commit()
        self.disconnect()
        
    def random_list(self):
        # 랜덤한 novel_nm 10개 select
        query = """SELECT novel_nm
                FROM (
                SELECT novel_nm
                FROM t_novel
                ORDER BY DBMS_RANDOM.RANDOM
                )
                WHERE ROWNUM <= 10"""
        self.connect()
        cursor = self.connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        self.disconnect()
        text_list = [row[0] for row in result]
        return text_list

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