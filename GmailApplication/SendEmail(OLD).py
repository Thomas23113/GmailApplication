import smtplib
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

from GUI import *



def SendEmail_noAttachment(recipientEmailAddress, yourEmailAddress, yourPassword, emailHeader, emailText):
    email_smtp = "smtp.gmail.com"

    # create an email message object
    message = EmailMessage()

    # configure email headers
    message['Subject'] = emailHeader
    message['From'] = yourEmailAddress
    message['To'] = recipientEmailAddress

    # set email body text
    message.set_content(emailText)

    # set smtp server and port
    server = smtplib.SMTP(email_smtp, '587')
    # identify this client to the SMTP server
    server.ehlo()
    # secure the SMTP connection
    server.starttls()

    # login to email account
    server.login(yourEmailAddress, yourPassword)
    # send email
    server.send_message(message)
    # close connection to server
    server.quit()

def SendEmail_Attachment(recipientEmailAddress, yourEmailAddress, yourPassword, emailHeader, emailText,filename):
    email_smtp = "smtp.gmail.com"

    # create an email message object
    message = EmailMessage()

    # configure email headers
    message['Subject'] = emailHeader
    message['From'] = yourEmailAddress
    message['To'] = recipientEmailAddress

    # set email body text
    message.set_content(emailText)

    #attach files
    filename = filename
    attachment = open(filename, 'rb')

    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename= {filename}')

    message.attach(part)
    attachment.close()

    # set smtp server and port
    server = smtplib.SMTP(email_smtp, '587')
    # identify this client to the SMTP server
    server.ehlo()
    # secure the SMTP connection
    server.starttls()

    # login to email account
    server.login(yourEmailAddress, yourPassword)
    # send email
    server.send_message(message)
    # close connection to server
    server.quit()