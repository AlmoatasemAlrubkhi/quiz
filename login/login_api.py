class LoginAPI:
    def __init__(self, conn):
        self.conn = conn

    def login(self, email, password):
        cursor = self.conn.cursor()
        try:
            # Check if the email and password match a record in the database
            query = "SELECT * FROM person WHERE email = %s AND pass = %s"
            cursor.execute(query, (email, password))
            result = cursor.fetchone()
            if result:
                return {'success': 'Login successful'}
            else:
                return {'error': 'Invalid email or password'}
        except Exception as e:
            return {'error': str(e)}
        finally:
            cursor.close()
