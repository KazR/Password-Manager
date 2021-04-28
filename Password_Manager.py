#   Qasem Rana 2021
#   Password Manager

#   Imports
import sqlite3
from hashlib import sha256
import pyperclip
from tkinter import *
from sys import exit
from threading import Thread
from time import sleep

#   Master Admin Pasword for Database and Menu Access 
adminPass = "123"; conn = False; copy = False

#    Copy to Clipboard Method
def clip_copy(password):
    pyperclip.copy(password)

#   Create Password Method
def create_passW(key, service, adminP):
    return sha256(adminP.encode('utf-8') + service.lower().encode('utf-8') + key.encode('utf-8')).hexdigest()[:15]

#   Get Hash Method
def hex_getter(adminP, service):
    return sha256(adminP.encode('utf-8') + service.lower().encode('utf-8')).hexdigest()

#   Get Password Method
def passW_getter(adminP, service):
    secret_key = hex_getter(adminP, service)
    cursor = link.execute("SELECT * from KEYS WHERE PASS_KEY=" + '"' + secret_key + '"')
    file_string = ""
    for row in cursor:
        file_string = row[0]
    return create_passW(file_string, service, adminP)

#   Set Password Method
def pass_add(service, adminP):
    secret_key = hex_getter(adminP, service)
    command = 'INSERT INTO KEYS (PASS_KEY) VALUES (%s);' %('"' + secret_key +'"')
    link.execute(command)
    link.commit()
    return create_passW(secret_key, service, adminP)

# Check Admin Pass is Correct Method
def checkPass(event):
    global conn
    if passEntry.get() == adminPass:
        conn = True
        root.destroy()
    else:
        conn = False
        passEntry.delete(0, END)

#   Create GUI
def placeMain():
    succesLabel.place(relx=0, rely=0, relwidth=1, relheight=0.1)
    getButton.place(relx=0.35, rely=0.39, relwidth=0.3, relheight=0.1)
    setButton.place(relx=0.35, rely=0.51, relwidth=0.3, relheight=0.1)
def forgetMain():
    getButton.place_forget()
    setButton.place_forget()
    succesLabel.place_forget()
def placeGet():
    forgetMain()
    getsetLabel.place(relx=0, rely=0.2, relwidth=1, relheight=0.1)
    getEntry.place(relx=0.3, rely=0.3, relwidth=0.4, relheight=0.1)
    backButton.place(relx=0.3, rely=0.9, relwidth=0.4, relheight=0.1)
    passLabel.place(relx=0, rely=0.5, relwidth=1, relheight=0.2)
    root.bind('<Return>', check_get)
def forgetGet():
    getsetLabel.place_forget()
    getEntry.place_forget()
    passLabel.place_forget()
    passLabel.config(text='')
    getEntry.delete(0, END)
    root.unbind('<Return>')
def placeSet():
    forgetMain()
    root.bind('<Return>', check_set)
    getsetLabel.place(relx=0, rely=0.2, relwidth=1, relheight=0.1)
    passLabel.place(relx=0, rely=0.5, relwidth=1, relheight=0.2)
    setEntry.place(relx=0.3, rely=0.3, relwidth=0.4, relheight=0.1)
    backButton.place(relx=0.3, rely=0.9, relwidth=0.4, relheight=0.1)
def forgetSet():
    getsetLabel.place_forget()
    passLabel.place_forget()
    setEntry.place_forget()
    backButton.place_forget()
    passLabel.config(text='')
    setEntry.delete(0, END)
    root.unbind('<Return>')
def goBack():
    placeMain()
    forgetSet()
    forgetGet()
def check_get(*args):
    service = getEntry.get()
    passLabel.config(text=service.capitalize()+" password:\n"+passW_getter(adminPass, service))
def check_set(*args):
    service = setEntry.get()
    passLabel.config(text=service.capitalize()+" password created:\n"+pass_add(service, adminPass))
def killapp(*args):
    root.destroy()
def makeCopy(event):
    global copy
    if passLabel['text']:
        clip_copy(passLabel['text'].split('\n')[1])
        copy = True
def showCopyAnim():
    global copy
    while True:
        if copy:
            for i in range(1, 3000):
                copyLabel.place(relx=0.3, rely=0.2/3000*i-0.1, relwidth=0.4, relheight=0.1)
            sleep(0.5)
            for i in range(1, 3000):
                copyLabel.place(relx=0.3, rely=0.1-0.2/3000*i, relwidth=0.4, relheight=0.1)
            copy=False
        sleep(0.25)

#   Initialize TKinter GUI
root = Tk()
root.geometry('300x200+300+200')
root.title('Password')
Label(text='Type in the admin password').place(relx=0, rely=0, relwidth=1, relheight=0.5)
passEntry = Entry(justify='center')
passEntry.place(relx=0.05, rely=0.4, relwidth=0.9, relheight=0.35)
root.bind('<Return>', checkPass)
root.mainloop()

#   Database Link on Correct Password
link = sqlite3.connect("passwords.db")

root = Tk()
root.title('Password Manager')
root.geometry('600x500+300+200')
if not conn: exit()

"""Main Section"""
succesLabel = Label(text='')
try:
    link.execute('''CREATE TABLE KEYS (PASS_KEY TEXT PRIMARY KEY NOT NULL);''')
    succesLabel['text'] = "Your safe has been created!\nWhat would you like to store in it today?"
except:
    succesLabel['text'] = "You have a safe, what would you like to do today?"

#   Menu Buttons
getButton = Button(text='Get Password', bg='#888888', fg='white', command=placeGet)
setButton = Button(text='Set Password', bg='#888888', fg='white', command=placeSet)

backButton = Button(text='Back', bg='#888888', fg='white', command=goBack)
getsetLabel = Label(text='What is the name of service?')
passLabel = Label(text='', font=('Arial', 15, 'normal'))

#   Entry Boxes
getEntry = Entry(justify='center')
setEntry = Entry(justify='center')

#   Copy to Clipboard Notification
copyLabel = Label(text='Password copied to clipboard', fg='white', bg='#165824')
copyThread = Thread(target=showCopyAnim); copyThread.start()

placeMain()

root.bind('<Escape>', killapp)
root.bind('<Control-c>', makeCopy)
root.mainloop()
