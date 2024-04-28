from flask import Flask, request, jsonify
from email_score.email import send_email
from person_api import person_api
from quiz_api import quiz_api
from database import db
from signup import signup_api
from login import login_api
from quiz_api import quiz_api
from solved_quiz import solved_quiz_api
from share_result import share_result_api
import psycopg2
import secrets

app = Flask(__name__)


conn = psycopg2.connect(database = 'quiz_db', user = 'al-moatasem', password = '123456789', port = 5432)


cursor = conn.cursor()

cursor.execute('select person_name from person where person_id = 1')

name = cursor.fetchone()

@app.route("/")
def index():
    return 'new flask ' + name[0]

@app.route("/login", methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    login_api_instance = login_api.LoginAPI(conn)
    result = login_api_instance.login(email, password)

    return jsonify(result)

@app.route("/signup", methods=['POST'])
def signup():
    data = request.get_json()

    person_name = data.get('person_name')
    email = data.get('email')
    password = data.get('password')

    signup_api_instance = signup_api.SignupAPI(conn)
    result = signup_api_instance.signup(person_name, email, password)

    return jsonify(result)


@app.route("/quiz/create_quiz", methods=['POST'])
def create_quiz():
    data = request.get_json()

    quiz_name = data.get('quiz_name')
    teacher_id = data.get('teacher_id')
    category = data.get('category')
    difficulty_level = data.get('difficulty_level')
    question_type = data.get('question_type')
    questions = data.get('questions')  
    is_verified = data.get('is_verified')

    quiz_api_instance = quiz_api.QuizAPI(conn)
    result = quiz_api_instance.create_quiz(quiz_name, teacher_id, category, difficulty_level, question_type, questions, is_verified)

    return jsonify(result)

@app.route("/quiz/get_quiz", methods=['GET'])
def get_quiz():
    quiz_id = request.args.get('quiz_id')

    quiz_api_instance = quiz_api.QuizAPI(conn)
    result = quiz_api_instance.get_quiz(quiz_id)

    return jsonify(result)



@app.route("/quiz/update_quiz", methods=['POST'])
def update_quiz():
    data = request.get_json()

    quiz_id = data.get('quiz_id')
    update_data = data.get('update_data')

    quiz_api_instance = quiz_api.QuizAPI(conn)
    result = quiz_api_instance.update_quiz(quiz_id, update_data)

    return jsonify(result)



def generate_token():
    return secrets.token_urlsafe(16)  

@app.route("/quiz/submit_answers", methods=['POST'])
def submit_answers():
    data = request.get_json()

    quiz_id = data.get('quiz_id')
    student_id = data.get('student_id')
    student_answers = data.get('student_answers')

    quiz_api_instance = quiz_api.QuizAPI(conn)
    correct_answers = quiz_api_instance.get_correct_answers(quiz_id)

    solved_quiz_api_instance = solved_quiz_api.SolvedQuizAPI(conn)
    score = solved_quiz_api_instance.calculate_score(student_answers, correct_answers)

    token = generate_token()
    
    result = solved_quiz_api_instance.save_solved_quiz(student_id, quiz_id, student_answers, score, token)

    return jsonify(result)


@app.route("/scores/<token>")
def view_quiz_score(token):
    
    solved_quiz_api_instance = solved_quiz_api.SolvedQuizAPI(conn)

    try:
        quiz_scores = solved_quiz_api_instance.get_quiz_scores_by_token(token)

        student_id = quiz_scores[1]
        quiz_id = quiz_scores[0]
        score = quiz_scores[2]

        return f"Student ID: {student_id}, Quiz ID: {quiz_id}, Score: {score}"

    except Exception as e:
        return 'error: token is invalid'
   

@app.route("/share_quiz_scores", methods=["POST"])
def share_quiz_scores():
    data = request.get_json()
    receiver_email = data.get("receiver_email")
    token = data.get("token")

    solved_quiz_api_instance = solved_quiz_api.SolvedQuizAPI(conn)
    result = solved_quiz_api_instance.get_quiz_scores_by_token(token)

    if "error" in result:
        return jsonify({"error": "Failed to retrieve quiz scores"})

    scores = result
    message = "Quiz Score:\n"
    message += f"Quiz ID: {scores[0]}, Score: {scores[2]}\n"

    email_result = send_email(receiver_email, token)
    if "error" in email_result:
        return jsonify({"error": "Failed to send email"})

    return jsonify({"success": "Email sent successfully"})


@app.route("/share_result", methods=['POST'])
def share_result():
    data = request.get_json()

    quiz_id = data.get('quiz_id')
    sender_id = data.get('sender_id')
    receiver_id = data.get('receiver_id')
    score = data.get('score')
    expiration_period_days = data.get('expiration_period_days')

    token = generate_token()

    share_results_instance = share_result_api.ShareResultAPI(conn)
    success = share_results_instance.save_shared_result(quiz_id, sender_id, receiver_id, token, expiration_period_days, score)

    if success:
        return jsonify({'success': 'Quiz result shared successfully', 'token': token})
    else:
        return jsonify({'error': 'Failed to share quiz result'})



@app.route("/user/user_details/<int:user_id>", methods=['GET'])
def get_user_details(user_id):
    person_api_instance = person_api.PersonAPI(conn)
    user_details = person_api_instance.get_user_details(user_id)
    if user_details:
        return jsonify(user_details)
    else:
        return jsonify({'error': 'User not found'})


@app.route("/change_user_type", methods=['PATCH'])
def change_user_type():
    data = request.get_json()
    person_id = data.get('person_id')
    new_user_type = data.get('new_user_type')
    requester_person_type = data.get('requester_person_type')

    user_type_api_instance = person_api.PersonAPI(conn)
    result = user_type_api_instance.change_user_type(person_id, new_user_type, requester_person_type)

    return jsonify(result)


@app.route("/get_user_type", methods=['GET'])
def get_user_type():
    user_id = request.args.get('user_id')

    person_api_instance = person_api.PersonAPI(conn)
    user_type = person_api_instance.get_user_type(user_id)

    if user_type:
        return jsonify({'user_type': user_type})
    else:
        return jsonify({'error': 'User not found'})



if __name__ == "__main__":
    app.run(debug=True)