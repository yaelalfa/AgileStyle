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
sql = '''CREATE TABLE IF NOT EXISTS proj_tasks
         (
          proj_id text NOT NULL,
          taskId text NOT NULL,        
          time text,
          crewNum text,
          PRIMARY KEY(proj_id,taskId)
           ) ;          
          '''
cc.execute(sql)

conect.commit()
conect.close()

###########################################################################################
global flag1,flag2,flag3,flag4,flag5,flag6,flag7
flag1,flag2,flag3,flag4,flag5,flag6,flag7=0,0,0,0,0,0,0,


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

    @classmethod
    def get_projects(cls, id): #return all the projects by the managerId
        connect = sqlite3.connect('myDb.db')
        cc = connect.cursor()
        sql = """SELECT * FROM projects 
                           WHERE managerId=? 


                           """
        dt = (id,)
        try:
            cc.execute(sql, dt)
          #  ms.showinfo("בוצע"," :הצגת פרויקטים עבור מזהה מנהל " + id)
            p = cc.fetchall()
            return p

        except Exception:
            ms.showerror("שגיאה"," :לא ניתן להציג פרויקטים שהמזהה של המנהל הוא"+id)
        connect.commit()
        connect.close()


    @classmethod
    def get_project(cls, pid,mid): #return project with projId=pid and managerId=mid
        connect = sqlite3.connect('myDb.db')
        cc = connect.cursor()
        sql = """SELECT * FROM projects 
                           WHERE projId=?
                           AND managerId=? 


                           """
        dt = (pid,mid)
        try:
            cc.execute(sql, dt)
          #  ms.showinfo("בוצע"," :הצגת פרויקטים עבור מזהה מנהל " + id)
            p = cc.fetchone()
            return p

        except Exception:
            ms.showerror("שגיאה"," לא ניתן להציג פרויקט")
        connect.commit()
        connect.close()


#*************end of project class**********************************#

#**************task class*********************************#
class TASK:
    def __init__(self,taskId,time,crewN,projId):
        self.taskId=taskId
        self.time=time
        self.crewNum=crewN
        self.projId=projId



    def insert_to_table(self):
        conect = sqlite3.connect('myDb.db')
        cc = conect.cursor()
        sql = '''INSERT INTO proj_tasks VALUES(?,?,?,?)
         '''
        dats_tuple = (self.projId,self.taskId,self.time,self.crewNum)

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

        sql = 'SELECT * FROM proj_tasks'
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
    def get_task(cls,tid,pid):
        connect = sqlite3.connect('myDb.db')
        cc = connect.cursor()

        sql = """SELECT * 
                    FROM proj_tasks
                    where proj_Id=? 
                    AND taskId=?         

                                    """
        dt = (pid,tid)
        cc.execute(sql, dt)
        user = cc.fetchone()

        if not user:
            ms.showerror("error", "task not exists")
            return 0


        return user

        connect.commit()


    @classmethod
    def get_tasks(cls, pid): #return all the tasks by the projId=pj
        connect = sqlite3.connect('myDb.db')
        cc = connect.cursor()
        sql = """SELECT * FROM proj_tasks 
                           WHERE proj_id=? 


                           """
        dt = (pid,)
        try:
            cc.execute(sql, dt)
          #  ms.showinfo("בוצע"," :הצגת פרויקטים עבור מזהה מנהל " + id)
            t = cc.fetchall()
            return t

        except Exception:
            ms.showerror("שגיאה"," :לא ניתן להציג פרויקטים שהמזהה של המנהל הוא"+id)
        connect.commit()
        connect.close()


    @classmethod
    def update_time(cls,tid,t,pid):
        conect = sqlite3.connect('myDb.db')
        cc = conect.cursor()
        sql = '''UPDATE proj_tasks 
        SET time = ?
        WHERE proj_id=?
        AND taskId = ?
         '''
        dats_tuple = (pid,tid,t)


        try:
            cc.execute(sql, dats_tuple)
            ms.showinfo("","משימה עודכנה בהצלחה")
            return 1

        except Exception:
            ms.showerror("שגיאה"," נסיון לעדכן משימה נכשל")
            return 0

        conect.commit()
        conect.close()

    @classmethod
    def update_crew(cls,tid,cr,pid):
        conect = sqlite3.connect('myDb.db')
        cc = conect.cursor()
        sql = '''UPDATE proj_tasks 
        SET crewNum= ?
        WHERE taskId = ?
         '''
        dats_tuple = (pid,tid,cr)


        try:
            cc.execute(sql, dats_tuple)
            ms.showinfo("","מספר אנשי צוות עודכן בהצלחה")
            return 1

        except Exception:
            ms.showerror("שגיאה"," נסיון לעדכן משימה נכשל")
            return 0

        conect.commit()
        conect.close()



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
        ).grid(row=1, column=1)


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
        self.spf = Frame(self.master, padx=20, pady=30)  # show project frame

    ##################project editor functions##############################

    def project_frame(self):

        self.df.forget()

        def back():
            self.pf.forget()
            self.maneger_frame()


        self.head["text"] = self.username.get()+" :ניהול פרויקטים של "
        Button(
            self.pf,
            text="הוסף פרויקט",
            bd=3,
            font=("", 15),
            padx=1,
            pady=1,
            command=self.add_proj_frame,
        ).grid(row=1, column=1)
        Button(
            self.pf,
            text="מחק פרויקט",
            bd=3,
            font=("", 15),
            padx=1,
            pady=1,
            command=self.remov_proj_frame, ).grid(row=2, column=1)

        Button(
            self.pf,
            text=" :הצג פרויקט לפי מספר מזהה",
            bd=3,
            font=("", 15),
            padx=1,
            pady=1,
            command=self.show_proj_frame, ).grid(row=3, column=1)

        Entry(self.pf, textvariable=self.prjNum, bd=5, font=("", 15)).grid(
            row=3, column=0
        )

        Button(
            self.pf,
            text="חזור",
            bd=3,
            font=("", 15),
            padx=1,
            pady=1,
            command=back, ).grid(row=0, column=1)

        projects = PROJECT.get_projects(self.username.get())

        Label(self.pf, text="_____________________________________", font=("", 20), pady=10, padx=10).grid(row=5, column=0)
        Label(self.pf, text=":הפרויקטים שלך", font=("", 20), pady=10, padx=10).grid(row=6, column=1)
        Label(self.pf, text=":מזהה פרויקט", font=("", 20, 'underline'), pady=10, padx=10).grid(row=7, column=0)
        Label(self.pf, text=":שם פרויקט", font=("", 20, 'underline'), pady=10, padx=10).grid(row=7, column=1)

        i = 8
        for p in projects:
            Label(self.pf, text=p[0], font=("", 20), pady=10, padx=10).grid(row=i, column=0)
            Label(self.pf, text=p[1], font=("", 20), pady=10, padx=10).grid(row=i, column=1)
            i = i + 1







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

            self.prjName()


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
            self.project_frame()


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

    def show_proj_frame(self):
        def back():
            self.spf.forget()
            self.project_frame()


        p=PROJECT.get_project(self.prjNum.get(),self.username.get())
        if not p:
            return

        self.pf.forget()
        self.head["text"] = "הצגת פרויקט"

        Button(
            self.spf,
            text="חזור",
            bd=3,
            font=("", 15),
            padx=1,
            pady=1,
            command=back,
        ).grid(row=0, column=1)

        Button(
            self.spf,
            text="משימות",
            bd=3,
            font=("", 15),
            padx=1,
            pady=1,
            command=self.task_frame,
        ).grid(row=1, column=1)



        Label(self.spf, text=" :מספר מזהה של פרויקט ", font=("", 20), pady=10, padx=10).grid( row=2, column=1 )
        Label(self.spf, text=p[0], font=("", 20), pady=10, padx=10).grid(row=2, column=0)
        Label(self.spf, text=" :שם ", font=("", 20), pady=10, padx=10).grid(row=3, column=1)
        Label(self.spf, text=p[1], font=("", 20), pady=10, padx=10).grid(row=3, column=0)







        self.spf.pack()






    def show_task_frame(self):
        self.tf.forget()

        def back():
            self.shtf.forget()
            self.task_frame()

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
        ).grid(row=1, column=1)
        Button(
            self.shtf,
            text="חזור",
            bd=3,
            font=("", 15),
            padx=1,
            pady=1,
            command=back,
        ).grid(row=2, column=1)

        self.shtf.pack()



   ###################end project editor functions##############################

   ###########task editor##############

    def add_task_fram(self):
        self.tf.forget()

        def add_task():
            self.atf.forget()
            t=TASK(self.taskId.get(),self.time.get(),self.crew.get(),self.prjNum.get())
            t.insert_to_table()
            self.head["text"]="מנהל"
            self.task_frame()




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

        def back():
            self.tef.forget()
            self.task_frame()

        t = TASK.get_task(self.taskId.get(),self.prjNum.get())
        if t==0:
            return

        self.time.set(t[2])
        self.crew.set(t[3])
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


        def update_time():
            b=TASK.update_time(self.taskId.get(),self.time.get(),self.prjNum.get())
            if b==1:
                Label(self.tef, text=self.time.get(), font=("", 20), pady=10, padx=10).grid(
                row=1, column=0)


        def update_crew():
            b=TASK.update_crew(self.taskId.get(),self.crew.get(),self.prjNum.get())

            if b == 1:
                Label(self.tef, text=self.crew.get(), font=("", 20), pady=10, padx=10).grid(
                    row=2, column=0
                )

        Button(
            self.tef,
            text="עדכן שעות",
            bd=3,
            font=("", 15),
            padx=1,
            pady=1,
            command=update_time,
        ).grid(row=4, column=2)

        Button(
            self.tef,
            text="עדכן כמות צוות",
            bd=3,
            font=("", 15),
            padx=1,
            pady=1,
            command=update_crew,
        ).grid(row=5, column=2)

        Entry(self.tef, textvariable=self.time, bd=5, font=("", 15)).grid(
            row=4, column=1
        )

        Entry(self.tef, textvariable=self.crew, bd=5, font=("", 15)).grid(
            row=5, column=1
        )

        Button(
            self.tef,
            text="חזור",
            bd=3,
            font=("", 15),
            padx=1,
            pady=1,
            command=back,
        ).grid(row=6, column=2)


        self.tef.pack()



    def task_frame(self):

        self.spf.forget()
        def back():
            self.tf.forget()
            self.show_proj_frame()

        Button(
            self.tf,
            text="חזור",
            bd=3,
            font=("", 15),
            padx=1,
            pady=1,
            command=back,
        ).grid(row=0, column=1)

        Button(
            self.tf,
            text="הוסף משימה",
            bd=3,
            font=("", 15),
            padx=1,
            pady=1,
            command=self.add_task_fram,
        ).grid(row=1, column=1)
        Button(
            self.tf,
            text="הצג משימה",
            bd=3,
            font=("", 15),
            padx=1,
            pady=1,
            command=self.show_task_frame,
        ).grid(row=2, column=1)

        tasks = TASK.get_tasks(self.prjNum.get())

        Label(self.tf, text="________________________________", font=("", 20), pady=10, padx=10).grid(row=4,
                                                                                                           column=0)
        Label(self.tf, text="________________________________", font=("", 20), pady=10, padx=10).grid(row=4,
                                                                                                           column=1)
        Label(self.tf, text=":המשימות הקיימות בפרויקט", font=("", 20), pady=10, padx=10).grid(row=5, column=1)
        Label(self.tf, text=":מזהה", font=("", 20, 'underline'), pady=10, padx=10).grid(row=6, column=0)
        Label(self.tf, text=":מספר שעות מוערך", font=("", 20, 'underline'), pady=10, padx=10).grid(row=6, column=1)
        Label(self.tf, text=":מספר צוות דרוש", font=("", 20, 'underline'), pady=10, padx=10).grid(row=6, column=2)

        i = 7
        for t in tasks:

            Label(self.tf, text=t[1], font=("", 20), pady=10, padx=10).grid(row=i, column=0)
            Label(self.tf, text=t[2], font=("", 20), pady=10, padx=10).grid(row=i, column=1)
            Label(self.tf, text=t[3], font=("", 20), pady=10, padx=10).grid(row=i, column=2)
            i = i + 1




        self.head["text"] = "ניהול משימות"
        self.tf.pack()




   #########end of task editor##############



root = Tk()
main(root)
root.mainloop()
