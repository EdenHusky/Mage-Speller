# -*- coding: utf-8 -*-
"""
Created on Thu Dec 29 10:37:05 2022

@author: twitc
"""

import datetime
from tkinter import *
from tkinter import ttk
import ms_usr

UserList = []
with open('ms_profiles.txt') as f:
    for line in f:
        temp = ms_usr.User()
        line = line.strip().replace(" ", "").split(",")
        temp.setUser(line[0])
        temp.setPass(line[1])
        temp.setHint(line[2])
        UserList.append(temp)

sessionUserName, sessionPassword = '', ''


def loginCheck():
    sessionUserName = usr_e.get()
    sessionPassWord = pass_e.get()

    for i in UserList:
        if i.getUser() == sessionUserName and i.getPass() == sessionPassWord:
            window.destroy()
    return


window = Tk()
window.geometry("330x175")

dt = Label(window, text=datetime.date.today(), bg='#00008B',
           fg='white', font=('Helvetica', 10, 'bold'))
dt.place(x=window.winfo_width() - 70, y=10)

lbl = Label(window, text='Welcome to Mage Speller',
            bg='#00008B', fg='white', font=('Helvetica', 16))
lbl.place(x=60, y=20)

usr_l = Label(window, text='User Name: ', fg='black',
              font=('Helvetica', 10, 'bold'))
usr_l.place(x=60, y=65)
usr_e = Entry(window, text='Enter User Name', bg='white', fg='black', bd=5)
usr_e.place(x=140, y=60)

pass_l = Label(window, text='Password:   ', fg='black',
               font=('Helvetica', 10, 'bold'))
pass_l.place(x=60, y=95)
pass_e = Entry(window, show="*", bg='white', fg='black', bd=5)
pass_e.place(x=140, y=90)

login = Button(window, text="Log In", fg='blue', command=loginCheck)
login.place(x=60, y=120)

create_account = Button(window, text="Create Account", fg='blue')
create_account.place(x=120, y=120)

window['bg'] = '#00008B'
window.title('Mage Speller Log-in System')


window.mainloop()
