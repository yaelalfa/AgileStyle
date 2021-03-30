from tkinter import *
from tkinter import messagebox as ms

import sqlite3

from typing import List, Any

from PIL import ImageTk, Image

from docx import Document
from docx.shared import Inches

import os
# make database and users (if not exists already) table at programme start up
users = sqlite3.connect("users.db")



#users.cursor().execute("drop table users")
#images.cursor().execute("drop table images")
#stories.cursor().execute("drop table stories")


users.cursor().execute(
    "CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY ,password TEXT, role TEXT)"
)

 

print(
    users.cursor()
    .execute("SELECT username, role FROM users")
    .fetchall()
)

Maneger = "maneger"
Developer = "developer"
Custumer = "customer"

imgs = {}


# main Class
class main:
    def __init__(self, master):
        # Window
        self.master = master
        # Some Usefull variables
        self.username = StringVar()
        self.password = StringVar()
        self.role = StringVar()
        self.age = StringVar()
        

    # Login Function
    def login(self):
        # Establish Connection
        # with sqlite3.connect('quit.db') as db:
        c = self.users_db.cursor()
        # Find user If there is any take proper action
        find_user = "SELECT * FROM users WHERE username = ? and password = ?"
        c.execute(find_user, [(self.username.get()), (self.password.get())])
        result = c.fetchone()
        if not result:
            ms.showerror("אוי", "שם המשתמש או הסיסמא לא תקינים")
            return
        self.logf.pack_forget()
        # self.head['text'] = f'Logged In As\n {self.username.get()}'
        # self.head['pady'] = 150
        username = result[0]
        role: str = result[3].lower()
        if role == Maneger:
            c.execute(
                "SELECT class FROM users WHERE username=?", (self.username.get(),)
            )
            self.classname.set(c.fetchone()[0])
            self.show_Manger_frame()
        elif role == Developer:
            self.setup_dev()
            self.show_parent_dev()
            # show parents frame
            pass

    
    # Frame Packing Methords
    def login_frame(self):
        self.username.set("")
        self.password.set("")
        self.crf.pack_forget()
        self.teacher_frame.pack_forget()
        self.head["text"] = "התחברות"
        self.logf.pack()


