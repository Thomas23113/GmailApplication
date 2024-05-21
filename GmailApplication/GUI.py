import tkinter as tk
from GUIfunctions import *

# Create a new instance of Tkinter window
window = tk.Tk()
window.geometry("300x150")


# Set the window title
window.title("Email application")

# create variables for storing information
textAdressSender = tk.StringVar(value = "calcotest123@gmail.com")   # Gives the entry field an initial value
textAdressRecipient = tk.StringVar()
textpass = tk.StringVar(value = "")                                 # Gives the entry field an initial value
textheader = tk.StringVar()
textemail = tk.StringVar()

# Create space for filling in your emailaddress
labelemail = tk.Label(window, text="Your emailaddress",font=("arial", 14))
labelemail.grid(row = 0, column = 0, sticky= 'n')                                                  # To place the label into the window
emailAddress = tk.Entry(window, textvariable = textAdressSender, width= 25,font=("arial", 14))     # Couple the entry box to instance window and the Stringvar coupled to entry box
emailAddress.grid(row = 1, column = 0, sticky= 'n',pady = 10)                                      # to place the Entry pane into the window

#create space for filling in your app password
labelpass = tk.Label(window, text="Your App password", font=("arial", 14))
labelpass.grid(row = 2, column = 0, sticky= 'n', rowspan=2)
appPassword = tk.Entry(window, textvariable = textpass, show = '*', width= 25,font=("arial", 14))
appPassword.grid(row = 3, column = 0, sticky= 'n')

# Create space for filling in your recipients emailaddress
labelemail = tk.Label(window, text="Recipient emailaddress",font=("arial", 14))
labelemail.grid(row = 3, column = 0, sticky= 'n', pady = 70)                                                  
emailAddress = tk.Entry(window, textvariable = textAdressRecipient, width= 25,font=("arial", 14))     
emailAddress.grid(row = 3, column = 0, sticky= 'n',pady = 100)                                               

# Create a button widget for logging in
button = tk.Button(window, text="Login", command= lambda: on_button_click(textpass, textAdressSender, textAdressRecipient))
button.grid(row = 3, column = 0, pady = 40, sticky= 'n')

#Create room for your email text header
labelheader = tk.Label(window, text = "Email Header", font = ("arial", 14))
labelheader.grid(row = 0, column = 1, padx = 30)
header = tk.Entry(window, textvariable = textheader , width = 40 , font = ("arial", 14))
header.grid(row = 1, column = 1, padx = 30)

# create room for filling in the main text of the email
labeltext = tk.Label(window, text = "Email text", font = ("arial", 14))
labeltext.grid(row = 2, column = 1, padx = 30)
emailtext = tk.Text(window, width = 40 , font = ("arial", 14), height = 15, yscrollcommand = True)
emailtext.grid(row = 3, column = 1, padx = 30)

# Create a button widget for sending an email
button = tk.Button(window, text="send email", command= lambda: send_email( textAdressRecipient
                                                                  , textAdressSender
                                                                  , textpass
                                                                  , textheader
                                                                  , emailtext))
button.grid(row = 4, column = 0, pady = 20, sticky= 'n')

# Room for a file explorer

labelexplorer = tk.Label(window, text = "File explorer", font = ("arial", 14))
labelexplorer.grid(row = 0, column = 2, padx = 30)
button_explore = tk.Button(window,text = "Enter Files", command = lambda: browseFiles(labelexplorer))
button_explore.grid(row = 1, column = 2, padx = 30)
button_remove = tk.Button(window,text = "Remove files", command = lambda: remove_storedFilesVariable (labelexplorer) )
button_remove.grid(row = 2, column = 2, padx = 30, pady = 10 )

# Create the email inbox and associated widgets
# Email listbox
email_listbox = tk.Listbox(window, width=80, height=20)
email_listbox.grid(row=3, column=2, columnspan=2, padx=30, pady=20)
# code for selecting individual emails
email_listbox.bind("<Double-Button-1>", lambda event: OnDoubleClick(event, textAdressSender, textpass, window))

# Fetch button
fetch_button = tk.Button(window, text="Fetch Emails", command= lambda: on_fetch_click(textAdressSender, textpass, email_listbox))
fetch_button.grid(row=4, column=2, columnspan=2, padx=30, pady=10)

# Start the Tkinter event loop
window.mainloop()