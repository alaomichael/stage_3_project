# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart

# gmail_user = 'devmichaelalao@gmail.com'
# gmail_password = 'lqck cgww nedz khhs'

# sent_from = gmail_user
# to = ['devmichaelalao@gmail.com']
# subject = 'Test Email'
# body = 'This is a test email from the script.'

# email_text = MIMEMultipart()
# email_text['From'] = sent_from
# email_text['To'] = ", ".join(to)
# email_text['Subject'] = subject

# email_text.attach(MIMEText(body, 'plain'))

# try:
#     server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
#     server.ehlo()
#     server.login(gmail_user, gmail_password)
#     server.sendmail(sent_from, to, email_text.as_string())
#     server.close()

#     print('Email sent successfully!')
# except Exception as e:
#     print(f'Error sending email: {e}')



import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(gmail_user, gmail_password, to, subject, body):
    sent_from = gmail_user

    email_text = MIMEMultipart()
    email_text['From'] = sent_from
    email_text['To'] = ", ".join(to)
    email_text['Subject'] = subject
    email_text.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, email_text.as_string())
        server.close()

        print('Email sent successfully!')
    except Exception as e:
        print(f'Error sending email: {e}')
