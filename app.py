from flask import Flask, request, Response
from celery import Celery
import logging
from flask_mail import Mail, Message
from datetime import datetime
import os


# new function start
def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery

mail_port = os.getenv('MAIL_PORT')
if mail_port is None:
    raise ValueError('MAIL_PORT environment variable is not set.')

app.config['MAIL_PORT'] = int(mail_port)

# new code stop

app = Flask(__name__)

# Load environment variables
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
# app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT'))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS') == 'True'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

mail = Mail(app)
celery = make_celery(app)

# Configure Celery
app.config['CELERY_BROKER_URL'] = os.getenv('CELERY_BROKER_URL')
app.config['CELERY_RESULT_BACKEND'] = os.getenv('CELERY_RESULT_BACKEND')
# celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
# celery.conf.update(app.config)

# Set up logging
logging.basicConfig(filename='/var/log/messaging_system.log', level=logging.INFO)

@celery.task
def send_email(to):
    msg = Message('Hello', sender=app.config['MAIL_USERNAME'], recipients=[to])
    msg.body = 'This is a test email sent from a Flask app with Celery and RabbitMQ'
    with app.app_context():
        mail.send(msg)

@app.route('/')
def index():
    sendmail = request.args.get('sendmail')
    talktome = request.args.get('talktome')

    if sendmail:
        send_email.delay(sendmail)
        return f"Email to {sendmail} has been queued for sending."

    if talktome:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logging.info(f"Current time logged: {current_time}")
        return f"Current time logged: {current_time}"

    return "Welcome to the Messaging System!"

@app.route('/logs')
def get_logs():
    with open('/var/log/messaging_system.log', 'r') as f:
        log_content = f.read()
    return Response(log_content, mimetype='text/plain')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
