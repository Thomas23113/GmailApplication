from tkinter.messagebox import showinfo
from tkinter import filedialog
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import smtplib
import imaplib
import email

# Global variable to store the selected file path
def browseFiles(labelexplorer):
    global selected_file_paths
    filenames = filedialog.askopenfilenames(initialdir="/", title="Select Files")
    if filenames:
        selected_file_paths = list(filenames)
        # Display the names of selected files in the label
        file_names = [os.path.basename(file) for file in selected_file_paths]
        labelexplorer.config(text="Files Opened: " + ", ".join(file_names))

# Create a function to handle button click
def on_button_click(textpass, textAdressSender, textAdressRecipient):
    # Right now it does nothing usefull but it can give you some reassurance
    msg = f'You have logged in with your new credentials!'
    textpass.get()
    textAdressSender.get()
    textAdressRecipient.get()
    showinfo(
        title='Log in',
        message=msg
    )

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

def SendEmail_Attachment(recipientEmailAddress, yourEmailAddress, yourPassword, emailHeader, emailText, filenames):
    email_smtp = "smtp.gmail.com"

    # Create an email message object
    message = MIMEMultipart()

    # Configure email headers
    message['Subject'] = emailHeader
    message['From'] = yourEmailAddress
    message['To'] = recipientEmailAddress

    # Set email body text
    message.attach(MIMEText(emailText, 'plain'))

    # Attach files
    for filename in filenames:
        with open(filename, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename= {os.path.basename(filename)}')
        message.attach(part)


    # Set SMTP server and port
    server = smtplib.SMTP(email_smtp, 587)
    # Identify this client to the SMTP server
    server.ehlo()
    # Secure the SMTP connection
    server.starttls()

    # Login to email account
    server.login(yourEmailAddress, yourPassword)
    # Send email
    server.send_message(message)
    # Close connection to server
    server.quit()

#Create a function to send the email
def send_email(textAdressRecipient, textAdressSender, textpass, textheader, emailtext):
    global selected_file_paths                      #get the variable holding the variables you selected
    import tkinter as tk                            # reimport tkinter so that you can read out the full email text
    # The following get functions make sure that all info is up to date
    recipient_email = textAdressRecipient.get()     
    sender_email = textAdressSender.get()
    password = textpass.get()
    header = textheader.get()
    email_text = emailtext.get("1.0", tk.END)
    
    # Check if a file was selected
    if 'selected_file_paths' in globals():
        SendEmail_Attachment(recipient_email, sender_email, password, header, email_text, selected_file_paths)
    else:
        SendEmail_noAttachment(recipient_email, sender_email, password, header, email_text)
    showinfo(title='Email Sent', message='Email has been sent successfully!')

def remove_storedFilesVariable (labelexplorer):
    global selected_file_paths
    del selected_file_paths
    labelexplorer.config(text="File explorer")

# Function to fetch emails using IMAP
def fetch_emails(sender_email, password, email_listbox):
    import tkinter as tk
    # Connect to the IMAP server
    mail = imaplib.IMAP4_SSL('imap.gmail.com')

    mail.login(sender_email, password)
    mail.select('inbox')
    
    # Search for emails
    result, data = mail.search(None, 'ALL')
    # Clear the existing listbox
    email_listbox.delete(0, tk.END)
    # Loop through the email IDs
    for num in data[0].split():
        # Fetch the email using the ID
        result, data = mail.fetch(num, '(RFC822)')
        # Parse the email content
        raw_email = data[0][1]
        email_message = email.message_from_bytes(raw_email)
        # Extract required information like sender, subject, etc.
        from_ = email.utils.parseaddr(email_message['From'])[1]
        subject = email_message['Subject']
        snippet = email_message.get_payload()
        # Display the information in the listbox
        email_listbox.insert(tk.END, f"From: {from_}, Subject: {subject}")
    # Logout from the server
    mail.logout()

def on_fetch_click(textAdressSender, textpass, email_listbox):
    sender_email = textAdressSender.get()
    password = textpass.get()
    fetch_emails(sender_email, password, email_listbox)