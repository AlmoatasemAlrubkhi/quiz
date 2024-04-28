class PersonAPI:
    def __init__(self, db):
        self.db = db

    def get(self, person_id):
        query = "SELECT * FROM person WHERE person_id = %s"
        return self.db.fetch_query(query, (person_id,))

    def create_person(self, person_name, password, person_type, is_verified):
        query = """
            INSERT INTO person (person_name, pass, person_type, is_verified)
            VALUES (%s, %s, %s, %s)
            RETURNING person_id
        """
        params = (person_name, password, person_type, is_verified)
        result = self.db.fetch_query(query, params)
        return result[0][0]

    
    def get_user_details(self, user_id):
        try:
            query = "SELECT * FROM person WHERE person_id = %s"
            cursor = self.db.cursor()
            cursor.execute(query, (user_id,))
            user_details = cursor.fetchone()
            if user_details:
                return {
                    'person_id': user_details[0],
                    'person_name': user_details[1],
                    'person_type': user_details[4],
                    'is_verified': user_details[5]
                }
            else:
                return None
        except Exception as e:
            print("An error occurred:", e)
            return None
        finally:
            cursor.close()
    
    def update_person(self, person_id, person_name, password, person_type, is_verified):
        query = """
            UPDATE person
            SET person_name = %s, pass = %s, person_type = %s, is_verified = %s
            WHERE person_id = %s
        """
        params = (person_name, password, person_type, is_verified, person_id)
        self.db.execute_query(query, params)
    

    def change_user_type(self, person_id, new_user_type, requester_person_type):
        if requester_person_type != 'super':
            return {'error': 'Only super users can change user types'}

        cursor = self.db.cursor()
        try:
            query = """
                UPDATE person
                SET person_type = %s
                WHERE person_id = %s
            """
            cursor.execute(query, (new_user_type, person_id))
            self.db.commit()
            return {'success': 'User type changed successfully'}
        except Exception as e:
            return {'error': str(e)}
        finally:
            cursor.close()

    def get_user_type(self, user_id):
        try:
            cursor = self.db.cursor()
            query = "SELECT person_type FROM person WHERE person_id = %s"
            cursor.execute(query, (user_id,))
            user_type = cursor.fetchone()
            cursor.close()

            if user_type:
                return user_type[0]  
            else:
                return None
        except Exception as e:
            print("Error:", e)
            return None

    def delete_person(self, person_id):
        query = "DELETE FROM person WHERE person_id = %s"
        self.db.execute_query(query, (person_id,))