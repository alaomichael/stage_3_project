from app import celery, mail, app
from flask_mail import Message
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()

@celery.task
def send_email(to):
    msg = Message('Hello', sender=app.config['MAIL_USERNAME'], recipients=[to])
    msg.body = 'This is a test email sent from a Flask app with Celery and RabbitMQ'
    with app.app_context():
        mail.send(msg)
