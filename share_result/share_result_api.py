from datetime import datetime, timedelta


class ShareResultAPI:

    def __init__(self, conn):
        self.conn = conn



    def save_shared_result(self, quiz_id, sender_id, receiver_id, token, expiration_period_days, score):
        try:
            expiration_date = datetime.now() + timedelta(days=expiration_period_days)
            query = """
                INSERT INTO shared_results (quiz_id, sender_id, receiver_id, token, expiration_date, status, score)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            params = (quiz_id, sender_id, receiver_id, token, expiration_date, 'enabled', score)
            cursor = self.conn.cursor() 
            cursor.execute(query, params)
            self.conn.commit()  
            return True
        except Exception as e:
            print("An error occurred:", e)
            return False
        finally: 
            cursor.close()
