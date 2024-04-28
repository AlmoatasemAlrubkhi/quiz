import smtplib

from email.mime.text import MIMEText


def send_email(receiver_email, token):
    sender_email = "almoatasem190737@nu.edu.om"
    password = "13203756"

    message = MIMEText(f"Click the following link to view your quiz scores: http://127.0.0.1:5000/scores/{token}")
    message["Subject"] = "View Quiz Scores"
    message["From"] = sender_email
    message["To"] = receiver_email

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()
        return {'success': 'Email sent successfully'}
    except Exception as e:
        return {'error': f"An error occurred: {str(e)}"}
