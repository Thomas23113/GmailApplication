from tkinter.messagebox import showinfo
from tkinter import *
from tkinter import filedialog
from tkinter.ttk import *
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
    # Store email numbers

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
        # Display the information in the listbox
        email_listbox.insert(tk.END, f"From: {from_}, Subject: {subject}")
    # Logout from the server
    mail.logout()

def on_fetch_click(textAdressSender, textpass, email_listbox):
    sender_email = textAdressSender.get()
    password = textpass.get()
    fetch_emails(sender_email, password, email_listbox)

def OnDoubleClick(event, sender_email, textpass, window):
        # make all Stringvar objects Strings
        sender_email = sender_email.get()
        password = textpass.get()
        
        #connect to the server and login
        mail = imaplib.IMAP4_SSL('imap.gmail.com')

        mail.login(sender_email, password)
        mail.select('inbox')
        
        # Search for emails
        result, data = mail.search(None, 'ALL')
        # store email numbers
        email_numbers = data[0].split()
        # Extracts the exact values of the object you selected in the list box
        widget = event.widget
        selection= widget.curselection()[0]
        # value = widget.get(selection[0])
        email_number = email_numbers[selection] #find email UID
        # Fetch the email message
        status, data = mail.fetch(email_number, "(RFC822)")
        raw_email = data[0][1]
        

        if status == 'OK':
            raw_email_bytes = data[0][1]

            # decode bytes into a string
            msg = raw_email_bytes.decode('utf-8')
            #parse email
            email_message_click = email.message_from_string(msg)
            # fetch the header
            subject_click = email_message_click['Subject']
            # Get the body of the email
            body_click = get_body(email_message_click)
            open_new_window(window, subject_click,body_click)
        else:
            print("Failed to fetch email with status:", status)

def get_body(message: email.message.Message, encoding: str = "utf-8") -> str:
    body_in_bytes = ""
    if message.is_multipart():
        for part in message.walk():
            ctype = part.get_content_type()
            cdispo = str(part.get("Content-Disposition"))

            # Skip any text/plain (txt) attachments
            if ctype == "text/plain" and "attachment" not in cdispo:
                body_in_bytes = part.get_payload(decode=True)  # Decode
                break
    else:
        body_in_bytes = message.get_payload(decode=True)

    body = body_in_bytes.decode(encoding)
    return body

def open_new_window(window, subject, body):
    import tkinter as tk
    #Create a new window on top of the other window
    newWindow = Toplevel(window)
    
    # add traits of the new window
    newWindow.title(subject)
    newWindow.geometry("400x200")
    # Add body as the main text
    label = tk.Label(newWindow, text=body, wraplength=180)  # wraplength ensures text wraps within the window
    label.grid(row = 0, column = 0, sticky= 'n')
    label.pack()

