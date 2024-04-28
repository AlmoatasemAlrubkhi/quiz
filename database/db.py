import psycopg2

class Database:
    def __init__(self, dbname, user, password, host, port):
        self.conn = psycopg2.connect(
            dbname = 'quiz_db',
            user = 'al-moatasem',
            password = '123456789',
            #host = host,
            port = 5432
        )

    def execute_query(self, query, params=None):
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        self.conn.commit()
        cursor.close()

    def fetch_query(self, query, params=None):
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        result = cursor.fetchall()
        cursor.close()
        return result
