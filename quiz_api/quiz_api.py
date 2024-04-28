import json


class QuizAPI:
    def __init__(self, conn):
        self.conn = conn



    def create_quiz(self, quiz_name, teacher_id, category, difficulty_level, question_type, questions, is_verified):
        if not is_verified:
            return {'error': 'Only verified users (teachers) can create quizzes.'}

        cursor = self.conn.cursor()
        try:
            query = """
                INSERT INTO quiz (quiz_name, teacher_id, category, difficulty_level, question_type, questions)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING quiz_id
            """
            questions_json = json.dumps(questions)
            params = (quiz_name, teacher_id, category, difficulty_level, question_type, questions_json)
            cursor.execute(query, params)
            quiz_id = cursor.fetchone()[0]
            self.conn.commit()
            return {'success': 'Quiz created successfully', 'quiz_id': quiz_id}
        except Exception as e:
            return {'error': str(e)}
        finally:
            cursor.close()



    def get_quiz(self, quiz_id):
        query = "SELECT * FROM quiz WHERE quiz_id = %s" %quiz_id
        cursor = self.conn.cursor()
        cursor.execute(query, quiz_id)
        result = cursor.fetchone()
        cursor.close()
        return {'success': 'quiz has been successfully retrieved', 'quiz_id' : quiz_id, 'quiz_name' : result[1], 'category' : result[3], 'difficulty_level' : result[4], 'question_type' : result[5], 'questions' : result[6]}

    def get_correct_answers(self, quiz_id):
        try:
            query = "SELECT questions FROM quiz WHERE quiz_id = %s"
            cursor = self.conn.cursor()
            cursor.execute(query, (quiz_id),)
            result = cursor.fetchone()
            questions_data = result[0]['questions']

            correct_answers = {question_id: question_data['correct_answer'] for question_id, question_data in questions_data.items()}
            return correct_answers
        except Exception as e:
            return {'error': str(e)}


    def get_correct_answers(self, quiz_id):
        try:
            query = "SELECT questions FROM quiz WHERE quiz_id = %s"
            cursor = self.conn.cursor()
            cursor.execute(query, (quiz_id,))
            result = cursor.fetchone()

            if result is not None:
                questions_data = result[0]  

                if isinstance(questions_data, dict):
                    correct_answers = {question_id: question_data['correct_answer'] for question_id, question_data in questions_data.items()}
                    return correct_answers
                else:
                    return {'error': 'Invalid data format for questions'}
            else:
                return {'error': 'Quiz not found'}

        except Exception as e:
            return {'error': str(e)}


    def update_quiz(self, quiz_id, update_data):
        query = """
            UPDATE quiz
            SET questions = %s  
            WHERE quiz_id = %s
        """
        params = (json.dumps(update_data), quiz_id)  # Convert the dictionary to JSON string

        cursor = self.conn.cursor()
        try:
            cursor.execute(query, params)
            self.conn.commit()
            return {'success': 'Quiz updated successfully'}
        except Exception as e:
            return {'error': str(e)}
        finally:
            cursor.close()


    def delete_quiz(self, quiz_id):
        query = "DELETE FROM quiz WHERE quiz_id = %s"
        self.db.execute_query(query, (quiz_id,))

    
