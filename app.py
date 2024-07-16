import os
import time
from flask import Flask, request, Response
from dotenv import load_dotenv
from celery import Celery
from email_sender import send_email  # Import the send_email function

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Load environment variables
gmail_user ='devmichaelalao@gmail.com'
gmail_password ='lqck cgww nedz khhs'
if gmail_user is None or gmail_password is None:
    raise ValueError('GMAIL_USER and GMAIL_PASSWORD environment variables must be set.')

# Celery configuration
app.config['CELERY_BROKER_URL'] = 'amqp://guest:guest@rabbitmq//'
app.config['CELERY_RESULT_BACKEND'] = 'rpc://guest:guest@rabbitmq//'

def make_celery(app):
    celery = Celery(
        app.import_name,
        broker=app.config['CELERY_BROKER_URL'],
        backend=app.config['CELERY_RESULT_BACKEND']
    )
    celery.conf.update(app.config)
    
    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

celery = make_celery(app)

@celery.task(name='app.send_email')
def send_email_task(receivermail):
    subject = "Stage 3 Test Email"
    body = "This is a test email from DevOps stage 3 Task."
    
    send_email(gmail_user, gmail_password, [receivermail], subject, body)

@app.route("/")
def index():
    sendmail_param = request.args.get('sendmail')
    talktome_param = request.args.get('talktome')

    if sendmail_param:
        send_email_task.delay(sendmail_param)
        return f'Sending email to {sendmail_param}...'

    elif talktome_param:
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        log_message = f'Logged at {current_time}\n'
        log_file = '/var/log/messaging_system.log'
        
        try:
            with open(log_file, 'a') as f:
                f.write(log_message)
            return 'Logging message...'
        except Exception as e:
            return str(e), 500

    else:
        return 'Welcome to DevOps Stage 3 Task, Messaging System! This was built by Michael Alao, @michaelalao.'

@app.route('/logs')
def get_log():
    log_file = '/var/log/messaging_system.log'
    try:
        with open(log_file, 'r') as f:
            log_content = f.read()
        return Response(log_content, mimetype='text/plain')
    except Exception as e:
        return str(e), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
