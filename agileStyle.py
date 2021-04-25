from tkinter import *
from tkinter import messagebox as ms
import tkinter as tk
import sqlite3



from typing import List, Any

# from docx import Document
# from docx.shared import Inches

import os

# make database and users (if not exists already) table at programme start up
users = sqlite3.connect("users.db")

# users.cursor().execute("drop table users")

users.cursor().execute(
    "CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY ,password TEXT, role TEXT)"
)

print(
    users.cursor()
        .execute("SELECT username, role FROM users")
        .fetchall()
)

Maneger = "manager"
Developer = "developer"
Custumer = "customer"

imgs = {}

##########################################################################################
# creat database if not exist and get conecction to it
conect = sqlite3.connect('myDb.db')

# get a cursor to execute sql statements
cc = conect.cursor()

# creat table
sql = '''CREATE TABLE IF NOT EXISTS projects
         (projId text PRIMARY KEY,
          name text,
          managerId text )'''
cc.execute(sql)
sql = '''CREATE TABLE IF NOT EXISTS tasks
         (taskId text PRIMARY KEY,
          time text,
          crew text )'''
cc.execute(sql)

conect.commit()
conect.close()

###########################################################################################
global flag1
flag1=0
global flag2
flag2=0
global flag3
flag3=0
global flag4
flag4=0
global flag5
flag5=0
global flag6
flag6=0
global flag7
flag7=0

#************project class**********************************#
class PROJECT:
    def __init__(self, projId, name, us):
        self.projId = projId
        self.name = name
        self.user = us #usrename

    def insert_to_table(self):
        connect = sqlite3.connect('myDb.db')
        cc = connect.cursor()
        sql = '''INSERT INTO projects VALUES(?,?,?)
        '''
        dats_tuple = (self.projId, self.name, self.user)
        try:
            cc.execute(sql, dats_tuple)
            ms.showinfo("פרויקט חדש נוצר בהצלחה")
        except Exception:
            ms.showerror("שגיאה!"," נסיון להכניס פרויקט חדש לטבלה נכשל")
        connect.commit()
        connect.close()

    @classmethod
    def printAll(cls):

        print("projects: ")
        connect = sqlite3.connect('myDb.db')
        cc = connect.cursor()

        sql = 'SELECT * FROM projects'
        cc.execute(sql)
        rows = cc.fetchall()

        for row in rows:
            print(row)
        connect.commit()
        connect.close()

    @classmethod
    def projectManager(cls, id):

        print("select project manager by project id: " + id)

        connect = sqlite3.connect('myDb.db')
        cc = connect.cursor()

        sql = """SELECT managerId 
            FROM projects 
            where projId=?         

                            """
        dt = (id,)
        cc.execute(sql, dt)
        user = cc.fetchone()

        if not user:
            ms.showerror("error", "project not exists")
            return 0

        ru = user[0]
        return ru

        connect.commit()
        connect.close()

    @classmethod
    def remove_by_id(cls, id):
        connect = sqlite3.connect('myDb.db')
        cc = connect.cursor()
        sql = """DELETE FROM projects 
                           WHERE projId=? 


                           """
        dt = (id,)
        try:
            cc.execute(sql, dt)
            ms.showinfo("בוצע","נמחק פרויקט: " + id)

        except Exception:
            ms.showerror("שגיאה","שגיאה בזמן מחיקת פרויקט")
        connect.commit()
        connect.close()
#*************end of project class**********************************#

#**************task class*********************************#
class TASK:
    def __init__(self,taskId,time,crewN):
        self.taskId=taskId
        self.time=time
        self.crewNum=crewN


    def insert_to_table(self):
        conect = sqlite3.connect('myDb.db')
        cc = conect.cursor()
        sql = '''INSERT INTO tasks VALUES(?,?,?)
         '''
        dats_tuple = (self.taskId,self.time,self.crewNum)

        try:
            cc.execute(sql, dats_tuple)
            ms.showinfo("משימה חדשה נוצרה בהצלחה")

        except Exception:
            ms.showerror("שגיאה! נסיון להכניס משימה חדשה לטבלה נכשל")

        conect.commit()
        conect.close()

    @classmethod
    def printAll(cls):
        connect= sqlite3.connect('myDb.db')
        cc = connect.cursor()

        sql = 'SELECT * FROM tasks'
        try:

            cc.execute(sql)
            rows = cc.fetchall()
            for row in rows:
                print(row)
        except Exception:
            ms.showerror("שגיאה! נסיון למשוך משימות נכשל")


        connect.commit()
        connect.close()

    @classmethod
    def get_task(cls,id):
        connect = sqlite3.connect('myDb.db')
        cc = connect.cursor()

        sql = """SELECT * 
                    FROM tasks 
                    where taskId=?         

                                    """
        dt = (id,)
        cc.execute(sql, dt)
        user = cc.fetchone()

        if not user:
            ms.showerror("error", "task not exists")
            return 0


        return user

        connect.commit()

#**************end of task class*********************************#







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
        self.resetPass = StringVar()
        self.findName = StringVar()
        self.widgets()
        self.prjNum=StringVar()
        self.prjName = StringVar()
        self.taskId=StringVar()
        self.time=StringVar()
        self.crew=StringVar()

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
        role = result[2].lower()
        if role == Maneger:
            c.execute(
                "SELECT username FROM users WHERE username=?", (self.username.get(),)
            )
            self.maneger_frame()
        elif role == Developer:
            print("true")
            self.developer_frame()
            pass
        elif role == Custumer:
            c.execute(
                "SELECT username FROM users WHERE username=?", (self.username.get(),)
            )
            self.custumer_frame()
        else:
            print("לא מכיר את התפקיד {username} - {role}")
            return

    def forgot_password(self):
        c = self.users_db.cursor()
        find_user = "SELECT * FROM users WHERE username = ? "
        c.execute(find_user, [(self.findName.get())])
        result = c.fetchone()
        if not result:
            ms.showerror("אוי", "שם המשתמש לא קיים")
            return
        update = """UPDATE users set password = ? where username = ?"""
        c.execute(update, [self.resetPass.get(), self.findName.get()])
        self.users_db.commit()
        self.login_frame()

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
                "התפקיד {self.n_role.get()} לא קיים",
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
        self.fpf.pack_forget()
        self.head["text"] = "התחברות"
        self.logf.pack()

    def create_acc_frame(self):
        self.n_username.set("")
        self.n_password.set("")
        self.logf.pack_forget()
        self.logf.pack_forget()
        self.head["text"] = "יצירת משתמש"
        self.crf.pack()

    def forgot_password_frame(self):
        self.findName.set("")
        self.resetPass.set("")
        self.logf.pack_forget()
        self.crf.pack_forget()
        self.head["text"] = "שחזור סיסמא"
        self.fpf.pack()

    def developer_frame(self):
        self.logf.pack_forget()
        self.head["text"] = "מפתח"
        self.df.pack()

    def maneger_frame(self):
        self.logf.pack_forget()
        self.head["text"] = "מנהל"
        Button(
            self.df,
            text="פרויקטים",
            bd=3,
            font=("", 15),
            padx=1,
            pady=1,
            command=self.project_frame,
        ).grid()
        Button(
            self.df,
            text="משימות",
            bd=3,
            font=("", 15),
            padx=1,
            pady=1,
            command=self.task_frame,
        ).grid()
        self.df.pack()

    def custumer_frame(self):
        self.logf.pack_forget()
        self.head["text"] = "לקוח"
        self.df.pack()

    ## DRAW WIDGETS ##
    def widgets(self):

        # Login widgets

        self.head = Label(self.master, text="התחברות", font=("", 35), pady=10)
        self.head.pack()
        self.logf = Frame(self.master, padx=10, pady=10)
        self.fpf = Frame(self.master, padx=10, pady=10)

        self.mf = Frame(self.master, padx=20, pady=30)
        self.cf = Frame(self.master, padx=20, pady=30)
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
            text=" שכחת סיסמא? ",
            bd=3,
            font=("", 15),
            padx=1,
            pady=1,
            command=self.forgot_password_frame,
        ).grid()
        Button(
            self.logf,
            text=" התחברות ",
            bd=3,
            font=("", 15),
            padx=5,
            pady=5,
            command=self.login,
        ).grid(row=2, column=1)
        Button(
            self.logf,
            text=" יצירת משתמש ",
            bd=3,
            font=("", 15),
            padx=5,
            pady=5,
            command=self.create_acc_frame,
        ).grid(row=2, column=2)
        self.logf.pack()

        # NewUser widgets

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

        # Forgot password widgets
        Label(self.fpf, text="שם משתמש: ", font=("", 20), pady=10, padx=10).grid(
            sticky=W
        )
        Entry(self.fpf, textvariable=self.findName, bd=5, font=("", 15)).grid(
            row=0, column=1
        )
        Label(self.fpf, text="סיסמא חדשה: ", font=("", 20), pady=5, padx=5).grid(sticky=W)
        Entry(
            self.fpf, textvariable=self.resetPass, bd=5, font=("", 15), show="*"
        ).grid(row=1, column=1)
        Button(
            self.fpf,
            text=" אפס סיסמא",
            bd=3,
            font=("", 15),
            padx=5,
            pady=5,
            command=self.forgot_password,
        ).grid()
        Button(
            self.fpf,
            text="חזור להתחברות ",
            bd=3,
            font=("", 15),
            padx=5,
            pady=5,
            command=self.login_frame,
        ).grid(row=2, column=1)

        # Developer Widgets
        self.df = Frame(self.master, padx=20, pady=30)

        # Manager Widgets
        self.mf = Frame(self.master, padx=20, pady=30)

        # Customer Widgets
        self.cf = Frame(self.master, padx=20, pady=30)



        self.pf = Frame(self.master, padx=20, pady=30)     #project frame
        self.apf = Frame(self.master, padx=20, pady=30)  #add project
        self.rpf = Frame(self.master, padx=20, pady=30) #remove project
        self.tf = Frame(self.master, padx=20, pady=30)  # task frame
        self.atf = Frame(self.master, padx=20, pady=30)  # add task frame
        self.shtf = Frame(self.master, padx=20, pady=30)  # show task frame
        self.tef = Frame(self.master, padx=20, pady=30)  #  task editor frame

    ##################project editor functions##############################

    def project_frame(self):
        self.df.forget()
        global flag1
        if flag1==0:
            flag1 = 1
            self.head["text"] = "ניהול פרויקט"
            Button(
                self.pf,
                text="הוסף פרויקט",
                bd=3,
                font=("", 15),
                padx=1,
                pady=1,
                command=self.add_proj_frame,
            ).grid()
            Button(
                self.pf,
                text="מחק פרויקט",
                bd=3,
                font=("", 15),
                padx=1,
                pady=1,
                command=self.remov_proj_frame, ).grid()

        self.pf.pack()


    def remov_proj_frame(self):
        self.pf.forget()


        def chekUser():

            pu=PROJECT.projectManager(self.prjNum.get())

            return  self.username.get()==pu

        def remove_proj():
            self.rpf.forget()
            if chekUser() is True:

                PROJECT.remove_by_id(self.prjNum.get())

            else:
                ms.showerror("error", "only project mamager can erase project")

            self.df.pack()


        global flag3
        if flag3==0:
            flag3=1
            self.head["text"] = "מחיקת פרויקט"
            Label(self.rpf, text="מספר מזהה של פרויקט: ", font=("", 20), pady=10, padx=10).grid(
                sticky=W
            )
            Entry(self.rpf, textvariable=self.prjNum, bd=5, font=("", 15)).grid(
                row=0, column=1
            )
            Button(
                self.rpf,
                text="מחק",
                bd=3,
                font=("", 15),
                padx=1,
                pady=1,
                command=remove_proj,
            ).grid()
        self.rpf.pack()



    def add_proj_frame(self):



        def add_proj():
            self.apf.forget()
            newp=PROJECT(self.prjNum.get(),self.prjName.get(),self.username.get())
            newp.insert_to_table()
            self.df.pack()


        self.pf.forget()

        global flag2
        if flag2==0:
            flag2=1
            self.head["text"] = "הוספת פרויקט"
            Label(self.apf, text="מספר מזהה של פרויקט: ", font=("", 20), pady=10, padx=10).grid(
                sticky=W
            )
            Entry(self.apf, textvariable=self.prjNum, bd=5, font=("", 15)).grid(
                row=0, column=1
            )
            Label(self.apf, text="שם של פרויקט: ", font=("", 20), pady=10, padx=10).grid(sticky=W)
            Entry(self.apf, textvariable=self.prjName, bd=5, font=("", 15)).grid(row=1, column=1)

            Button(
                self.apf,
                text="הוסף",
                bd=3,
                font=("", 15),
                padx=1,
                pady=1,
                command=add_proj,
            ).grid()




        self.apf.pack()



   ###################end project editor functions##############################

   ###########task editor##############

    def add_task_fram(self):
        self.tf.forget()

        def add_task():
            self.atf.forget()
            t=TASK(self.taskId.get(),self.time.get(),self.crew.get())
            t.insert_to_table()
            self.head["text"]="מנהל"
            self.df.pack()




        global flag5
        if flag5==0:
            flag5 = 1



            Label(self.atf, text="מזהה של משימה: ", font=("", 20), pady=10, padx=10).grid(
                sticky=W
            )
            Entry(self.atf, textvariable=self.taskId, bd=5, font=("", 15)).grid(
                row=0, column=1
            )
            Label(self.atf, text="מספר שעות מוערך להשלמת משימה: ", font=("", 20), pady=10, padx=10).grid(sticky=W)
            Entry(self.atf, textvariable=self.time, bd=5, font=("", 15)).grid(row=1, column=1)
            Label(self.atf, text="מספר צוות דרוש: ", font=("", 20), pady=10, padx=10).grid(sticky=W)
            Entry(self.atf, textvariable=self.crew, bd=5, font=("", 15)).grid(row=2, column=1)

            Button(
                self.atf,
                text="הוסף",
                bd=3,
                font=("", 15),
                padx=1,
                pady=1,
                command=add_task,
            ).grid()
        self.head["text"] = "הוספת משימה"
        self.atf.pack()


    def task_editor_frame(self):
        t = TASK.get_task(self.taskId.get())
        if t==0:
            return

        self.time.set(t[1])
        self.crew.set(t[2])
        self.shtf.forget()

        Label(self.tef, text=":מזה משימה ", font=("", 20), pady=10, padx=10).grid(
            row=0, column=1
        )
        Label(self.tef, text=self.taskId.get(), font=("", 20), pady=10, padx=10).grid(
            row=0, column=0
        )
        Label(self.tef, text=":מספר שעות מוערך להשלמת משימה ", font=("", 20), pady=10, padx=10).grid(
            row=1, column=1
        )
        Label(self.tef, text=self.time.get(), font=("", 20), pady=10, padx=10).grid(
            row=1, column=0
        )
        Label(self.tef, text=":כמות אנשי צוות דרוש ", font=("", 20), pady=10, padx=10).grid(
            row=2, column=1
        )
        Label(self.tef, text=self.crew.get(), font=("", 20), pady=10, padx=10).grid(
            row=2, column=0
        )




        self.tef.pack()



    def show_task_frame(self):
        self.tf.forget()
        print("hello")
        TASK.printAll()


        global flag6
        if flag6 == 0:
            flag6 = 1
            Label(self.shtf, text="מזהה של משימה: ", font=("", 20), pady=10, padx=10).grid(
                row=0, column=0
            )
            Entry(self.shtf, textvariable=self.taskId, bd=5, font=("", 15)).grid(
                row=0, column=1
            )

            Button(
                self.shtf,
                text="הצג",
                bd=3,
                font=("", 15),
                padx=1,
                pady=1,
                command=self.task_editor_frame,
            ).grid()
        self.shtf.pack()





    def task_frame(self):

        self.df.forget()
        global flag4
        if flag4==0:
            flag4=1

            Button(
                self.tf,
                text="הוסף משימה",
                bd=3,
                font=("", 15),
                padx=1,
                pady=1,
                command=self.add_task_fram,
            ).grid()
            Button(
                self.tf,
                text="הצג משימה",
                bd=3,
                font=("", 15),
                padx=1,
                pady=1,
                command=self.show_task_frame,
            ).grid()
        self.head["text"] = "ניהול משימות"
        self.tf.pack()




   #########end of task editor##############



root = Tk()
main(root)
root.mainloop()
