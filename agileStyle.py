from tkinter import *
from tkinter import messagebox as ms
import proj_editor as PA
import task_editor as TA
import sqlite3

from typing import List, Any



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

def open_task_fram():
    TA.creat_task_fram()
def open_proj_fram():
    PA.menu()

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
        self.users_db = users
        self.n_username = StringVar()
        self.n_password = StringVar()
        self.n_role = StringVar()
        self.classname = StringVar()
        self.widgets()

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
            #SHOW MANAGER FRAME
        elif role == Developer:
            # show DEV frame
            print("true")
            pass
        elif role == Custumer:
            c.execute(
                "SELECT class FROM users WHERE username=?", (self.username.get(),)
            )
            #show costomer frame
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

            if self.n_role.get() not in [Custumer, Maneger, Developer]:
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
        
        self.head["text"] = "התחברות"
        self.logf.pack()

    def create_acc_frame(self):
        self.n_username.set("")
        self.n_password.set("")
        self.logf.pack_forget()
        self.logf.pack_forget()
        self.head["text"] = "יצירת משתמש"
        self.crf.pack()
        # Draw Widgets
    def widgets(self):
        self.head = Label(self.master, text="התחברות", font=("", 35), pady=10)
        self.head.pack()
        self.logf = Frame(self.master, padx=10, pady=10)
        Label(self.logf, text="שם משתמש: ", font=("", 20), pady=5, padx=5).grid(
            sticky=W
        )
        Entry(self.logf, textvariable=self.username, bd=5, font=("", 15)).grid(
            row=0, column=1
        )
        Label(self.logf, text="סיסמא: ", font=("", 20), pady=5, padx=5).grid(
            sticky=W
        )
        Entry(
            self.logf, textvariable=self.password, bd=5, font=("", 15), show="*"
        ).grid(row=1, column=1)
        Button(
            self.logf,
            text=" התחברות ",
            bd=3,
            font=("", 15),
            padx=5,
            pady=5,
            command=self.login,
            ).grid()
        Button(
            self.logf,
            text=" יצירת משתמש ",
            bd=3,
            font=("", 15),
            padx=5,
            pady=5,
            command=self.create_acc_frame,
        ).grid(row=2, column=1)
        self.logf.pack()

        self.crf = Frame(self.master, padx=10, pady=10)
        Label(self.crf, text="שם משתמש: ", font=("", 20), pady=10, padx=10).grid(
            sticky=W
        )
        Entry(self.crf, textvariable=self.n_username, bd=5, font=("", 15)).grid(
            row=0, column=1
        )
        Label(self.crf, text="סיסמא: ", font=("", 20), pady=5, padx=5).grid(sticky=W)
        Entry(
            self.crf, textvariable=self.n_password, bd=5, font=("", 15), show="*"
        ).grid(row=1, column=1)
        Label(self.crf, text="תפקיד: ", font=("", 20), pady=5, padx=5).grid(sticky=W)
        Entry(self.crf, textvariable=self.n_role, bd=5, font=("", 15)).grid(
            row=2, column=1
        )
        
        Button(
            self.crf,
            text=" יצירת משתמש ",
            bd=3,
            font=("", 15),
            padx=5,
            pady=5,
            command=self.new_user,
        ).grid()
        Button(
            self.crf,
            text="חזור להתחברות ",
            bd=3,
            font=("", 15),
            padx=5,
            pady=5,
            command=self.login_frame,
        ).grid(row=4, column=1)
root = Tk()
main(root)
root.mainloop()

