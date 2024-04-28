class SignupAPI:
    
    def __init__(self, conn):
        self.conn = conn


    def signup(self, person_name, email, password):
        existing_person = self.check_person_existence(email)
        if existing_person:
            return {'error': 'Person already exists'}

        cursor = self.conn.cursor()
        try:
            query = """
                INSERT INTO person (person_name, email, pass, person_type, is_verified)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING person_id, person_name, email
            """
            cursor.execute(query, (person_name, email, password, 'student', False))
            new_person = cursor.fetchone()
            self.conn.commit()
            return {
                'success': 'Person signed up successfully',
                'person_id': new_person[0],
                'person_name': new_person[1],
                'email': new_person[2]
            }
        except Exception as e:
            return {'error': str(e)}
        finally:
            cursor.close()


    def check_person_existence(self, email):
        cursor = self.conn.cursor()
        try:
            query = "SELECT person_id FROM person WHERE email = %s"
            cursor.execute(query, (email,))
            result = cursor.fetchone()
            return result
        except Exception as e:
            return {'error': str(e)}
        finally:
            cursor.close()
