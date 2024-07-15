import os
import time
from flask import Flask, request, Response
from dotenv import load_dotenv
from celery import Celery
from celeryconfig import make_celery
from flask_mail import Mail, Message

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# # Load environment variables
mail_port = os.getenv('MAIL_PORT')
if mail_port is None:
    raise ValueError('MAIL_PORT environment variable is not set.')


# Flask-Mail configuration for Gmail using SSL
# app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
# app.config['MAIL_PORT'] = int(mail_port)
# app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS') == 'True'
# app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL') == 'False'
# app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
# app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')


# # Celery configuration
# app.config['CELERY_BROKER_URL'] = os.getenv('CELERY_BROKER_URL')
# app.config['CELERY_RESULT_BACKEND'] = os.getenv('CELERY_RESULT_BACKEND')

app.config['MAIL_SERVER'] ='smtp.gmail.com'
app.config['MAIL_PORT'] =587
app.config['MAIL_USE_TLS'] ='True'
app.config['MAIL_USE_SSL'] ='False'
app.config['MAIL_USERNAME'] ='devmichaelalao@gmail.com'
app.config['MAIL_PASSWORD'] ='babatunde_2503'
# MAIL_SERVER=smtp.gmail.com
# MAIL_PORT=587
# MAIL_USE_TLS=True
# MAIL_USE_SSL=False
# MAIL_USERNAME=devmichaelalao@gmail.com
# MAIL_PASSWORD=babatunde_2503
# CELERY_BROKER_URL=amqp://guest:guest@rabbitmq//
# CELERY_RESULT_BACKEND=rpc://guest:guest@rabbitmq//
# ngrok = https://e589-34-35-58-26.ngrok-free.app
# NGROK_AUTH_TOKEN=2ACnR4qRSwhcwJfbW1ixBONRcbX_4NzAcUXcNXM7aREcX87oY
# NGROK_REGION=us
# NGROK_PORT=5000

# Celery configuration
app.config['CELERY_BROKER_URL'] ='amqp://guest:guest@rabbitmq//'
app.config['CELERY_RESULT_BACKEND'] ='rpc://guest:guest@rabbitmq//'


# Initialize Flask-Mail and Celery
mail = Mail(app)

def make_celery(app):
    celery = Celery(
        app.import_name,
        broker=app.config['CELERY_BROKER_URL'],
        backend=app.config['CELERY_RESULT_BACKEND']
    )
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery

celery = make_celery(app)

@celery.task(name='app.send_email')  # Register the task with a specific name
def send_email(receivermail):
    msg = Message("Stage 3 Test Email", sender=os.getenv('MAIL_USERNAME'), recipients=[receivermail])
    msg.body = "This is a test email from DevOps stage 3 Task."

    try:
        # Simulate a delay of 10 seconds before sending email
        #time.sleep(10)

        with app.app_context():
            mail.send(msg)
        print(f"Sent email to {receivermail}")
    except Exception as e:
        print(f"Error sending email: {e}")

    return True  # Optionally, return a value indicating success

@app.route("/")
def handle_request():
    sendmail_param = request.args.get('sendmail')
    talktome_param = request.args.get('talktome')

    if sendmail_param:
        send_email.delay(sendmail_param)
        return f'Sending email to {sendmail_param}...'

    elif talktome_param is not None: 
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        log_message = f'Logged at {current_time}\n'
        log_file = '/var/log/messaging_system.log'
        with open(log_file, 'a') as f:
            f.write(log_message)
        return 'Logging message...'

    else:
        return 'Welcome to DevOps Stage 3 Task, Messaging System! This was built by Michael Alao, @michaelalao.'

@app.route('/logs')
def get_log():
    try:
        with open('/var/log/messaging_system.log', 'r') as f:
            log_content = f.read()
        return Response(log_content, mimetype='text/plain')
    except Exception as e:
        return str(e), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
