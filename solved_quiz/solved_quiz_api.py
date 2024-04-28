import json

class SolvedQuizAPI: 

    def __init__(self, conn):
        self.conn = conn



    def calculate_score(self, student_answers, correct_answers):
        total_questions = len(student_answers)  
        correct_count = 0

        for question_id, student_answer in student_answers.items():
            if question_id in correct_answers and student_answer == correct_answers[question_id]:
                correct_count += 1

        score = (correct_count / total_questions) * 100 if total_questions > 0 else 0  

        return score



    def save_solved_quiz(self, student_id, quiz_id, student_answers, score, token):
        try:
            student_answers_json = json.dumps(student_answers)

            query = """
                INSERT INTO solved_quiz (student_id, quiz_id, student_answers, score, token)
                VALUES (%s, %s, %s, %s, %s)
            """
            params = (student_id, quiz_id, student_answers_json, score, token)

            cursor = self.conn.cursor() 
            cursor.execute(query, params)
            self.conn.commit()  
            return {'success': 'Solved quiz saved successfully'}
        except Exception as e:
            return {'error': str(e)}
        finally: 
            cursor.close()


    def get_quiz_scores_by_token(self, token):
        try:
            query = """
                SELECT quiz_id, student_id, score, token
                FROM solved_quiz
                WHERE token = %s
            """
            cursor = self.conn.cursor()
            cursor.execute(query, (token,))
            scores = cursor.fetchone()
            return scores
        except Exception as e:
            return {'error': str(e)}
        finally:
            cursor.close()

