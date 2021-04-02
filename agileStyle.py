from tkinter import *
from tkinter import messagebox as ms

import sqlite3

from typing import List, Any



from docx import Document
from docx.shared import Inches

import os
# make database and users (if not exists already) table at programme start up
users = sqlite3.connect("users.db")



#users.cursor().execute("drop table users")

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
        elif role == Custumer:
            c.execute(
                "SELECT class FROM users WHERE username=?", (self.username.get(),)
            )
            self.classname.set(c.fetchone()[0])
            self.show_Custumer_frame()
        else:
            print(f"לא מכיר את התפקיד {username} - {role}")
            return


def new_user(self):
        # Establish Connection
        users_cursor = self.users_db.cursor()
       

        # Find Existing username if any take proper action
        # find_user = "SELECT * FROM users WHERE username = ?"
        # users_cursor.execute(find_user, [(self.username.get())])
        # if users_cursor.fetchall():
        #     ms.showerror("Error!", "Username Taken Try a Diffrent One.")
        #     return

        if self.n_role.get() not in [Custumer]:
            ms.showerror(
                "תקלה!",
                f"התפקיד {self.n_role.get()} לא קיים",
            )
            return

        # Create New Account
        insert_users = "INSERT INTO users(username, password, role) VALUES(?,?,?)"
        
        try:
            users_cursor.execute(
            insert_users,
            [
                (self.n_username.get()),
                (self.n_password.get()),
                self.n_role.get().lower(),
            ],
        )
        except Exception:
            return ms.showerror("!תקלה", "שם המשתמש קיים")
        
       
        self.users_db.commit()
        ms.showinfo("בוצע", "המשתמש נוצר בהצלחה")
        self.login_frame()

        
    # Frame Packing Methords
    def login_frame(self):
        self.username.set("")
        self.password.set("")
        self.crf.pack_forget()
        self.teacher_frame.pack_forget()
        self.head["text"] = "התחברות"
        self.logf.pack()


