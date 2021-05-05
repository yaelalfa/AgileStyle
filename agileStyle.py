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
sql = '''CREATE TABLE IF NOT EXISTS project_tasks
         (projId text NOT NULL,
          taskId text NOT NULL,
          time text,
          crew text ,
          PRIMARY KEY (projId,taskId))
          '''
cc.execute(sql)

sql = '''CREATE TABLE IF NOT EXISTS project_crew
         (projId text NOT NULL,
          user text NOT NULL,
          PRIMARY KEY (projId,user))
          '''
cc.execute(sql)

sql = '''CREATE TABLE IF NOT EXISTS user_message
         (
          sender text NOT NULL,
          to_user text NOT NULL,
          message text )

          '''
cc.execute(sql)


conect.commit()
conect.close()

###########################################################################################


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
    def get_projects(cls, manger_id):
        connect = sqlite3.connect('myDb.db')
        cc = connect.cursor()
        sql = """SELECT * FROM projects 
                               WHERE  managerId=? 


                               """
        dt = (manger_id,)
        try:
            cc.execute(sql, dt)
            rows = cc.fetchall()
            return rows



        except Exception:
            ms.showerror("שגיאה", "שגיאה בזמן משיכת פרויקטים")
        connect.commit()
        connect.close()

    @classmethod
    def get_project(cls, manger_id,proj_id):
        connect = sqlite3.connect('myDb.db')
        cc = connect.cursor()
        sql = """SELECT * FROM projects 
                               WHERE  managerId=? 
                               AND projId=?


                               """


        dt = (manger_id,proj_id)
        try:
            cc.execute(sql, dt)
            row = cc.fetchone()

            return row



        except Exception:
            ms.showerror("שגיאה", "שגיאה בזמן משיכת פרויקט")
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
        sql = '''INSERT INTO project_tasks VALUES(?,?,?,?)
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

        sql = 'SELECT * FROM project_tasks'
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
                    FROM project_tasks
                    where taskId=?   
                    AND projId=?      

                                    """
        dt = (tid,pid)
        try:
            cc.execute(sql, dt)
            r = cc.fetchone()
            return r


        except Exception:
            ms.showerror("error", "שגיאה בזמן משיכת משימה")





        connect.commit()

    @classmethod
    def get_tasks(cls, pid):
        connect = sqlite3.connect('myDb.db')
        cc = connect.cursor()

        sql = """SELECT * 
                        FROM project_tasks
                        where  projId=?      

                                        """
        dt = (pid,)

        try:

            cc.execute(sql,dt)
            rows = cc.fetchall()
            return rows
        except Exception:
            ms.showerror("error", "שגיאה בזמן משיכת משימה")



        connect.commit()


    @classmethod
    def update_hour(cls, pid,tid,time):
        connect = sqlite3.connect('myDb.db')
        cc = connect.cursor()

        sql = """UPDATE project_tasks
                        SET time=?
                        where  projId=?  
                        AND taskId=?    

                                        """
        dt = (time,pid,tid)

        try:

            cc.execute(sql,dt)
            ms.showinfo("", "מספר השעות עודכן בהצלחה ")
        except Exception:
            ms.showerror("error", "שגיאה בעידכון שעה ")



        connect.commit()


    @classmethod
    def update_crew(cls, pid,tid,crew):
        connect = sqlite3.connect('myDb.db')
        cc = connect.cursor()

        sql = """UPDATE project_tasks
                        SET time=?
                        where  projId=?  
                        AND taskId=?    

                                        """
        dt = (crew,pid,tid)

        try:

            cc.execute(sql,dt)
            ms.showinfo("", "מספר צוות עודכן בהצלחה ")
        except Exception:
            ms.showerror("error", "שגיאה בעידכון מספר צוות ")



        connect.commit()



    @classmethod
    def delet_task(cls, pid,tid):
        connect = sqlite3.connect('myDb.db')
        cc = connect.cursor()

        sql = """DELETE FROM project_tasks
                        where  projId=?  
                        AND taskId=?    

                                        """
        dt = (pid,tid)

        try:

            cc.execute(sql,dt)
            ms.showinfo("", "משימה נמחקה בהצלחה")
        except Exception:
            ms.showerror("error", "שגיאה ניסיון מחיקת משימה ")



        connect.commit()


#**************end of task class*********************************#


#************project crew class**********************************#
class PROJECT_CREW:
    @classmethod
    def insert_to_table(cls,pid,us):
        conect = sqlite3.connect('myDb.db')
        cc = conect.cursor()
        sql = '''INSERT INTO project_crew VALUES(?,?)
         '''
        dats_tuple = (pid,us)

        try:
            cc.execute(sql, dats_tuple)
            ms.showinfo(":עובד חדש נוסף לפרויקט"+pid)

        except Exception:
            ms.showerror("שגיאה! נסיון להכניס עובד חדש לטבלה נכשל")

        conect.commit()
        conect.close()

    @classmethod
    def get_crew(cls, pid):
        conect = sqlite3.connect('myDb.db')
        cc = conect.cursor()
        sql = '''SELECT * FROM project_crew 
                 WHERE projId=?
             '''
        dats_tuple = (pid,)

        try:
            cc.execute(sql, dats_tuple)
            rows=cc.fetchall()
            return rows

        except Exception:
            ms.showerror("שגיאה","נסיון למשוך צוות עובדים נכשל")

        conect.commit()
        conect.close()

    @classmethod
    def get_project(cls, username):
        connect = sqlite3.connect('myDb.db')
        cc = connect.cursor()
        sql = 'SELECT projId FROM project_crew WHERE  user=?'
        cc.execute(sql, (username,))
        row = cc.fetchone()
        print(row)
        return row

# ************end of project crew class**********************************#

# ************message  class**********************************#
class MESSAGE:
    @classmethod
    def new_message(cls,sender,to,message):
        conect = sqlite3.connect('myDb.db')
        cc = conect.cursor()
        sql = '''INSERT INTO user_message VALUES(?,?,?)
                '''
        dats_tuple = (sender,to,message)

        try:
            cc.execute(sql, dats_tuple)
            ms.showinfo("", ":הודעה נשלחה בהצלחה ל" + to)

        except Exception:
            ms.showerror("שגיאה", "נסיון לשלוח הודעה נכשל נכשל")

        conect.commit()
        conect.close()

    @classmethod
    def printAll(cls):
        connect = sqlite3.connect('myDb.db')
        cc = connect.cursor()

        sql = 'SELECT * FROM user_message'
        try:

            cc.execute(sql)
            rows = cc.fetchall()
            for row in rows:
                print(row)
        except Exception:
            ms.showerror(  "שגיאה", "שגיאה! נסיון למשוך הודעות נכשל")

        connect.commit()
        connect.close()

    @classmethod
    def get_my_mesagges(cls,us):
        connect = sqlite3.connect('myDb.db')
        cc = connect.cursor()

        sql = 'SELECT * FROM user_message where to_user=? '
        tp=(us,)
        try:

            cc.execute(sql,tp)
            rows = cc.fetchall()
            return rows
        except Exception:
            ms.showerror("שגיאה", "שגיאה! נסיון למשוך הודעות נכשל")

        connect.commit()
        connect.close()



# ************end of message  class**********************************#

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
        self.user_crew=StringVar()

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
        self.att.pack_forget()
        self.atf.pack_forget()
        self.head["text"] = "מפתח"
        self.df.pack()
        Button(
            self.df,
            text="הוספת משימות",
            bd=3,
            font=("", 15),
            padx=1,
            pady=1,
            command=self.add_task_frame_developer,
        ).grid(row=1, column=2)
        Button(self.df,
               text="עריכת משימות ",
               bd=3,
               font=("", 15),
               padx=1,
               pady=1,
               command=self.task_editor_frame_developer,
               ).grid(row=1, column=0)
        Button(self.df,
               text=" דף משימות ",
               bd=3,
               font=("", 15),
               padx=5,
               pady=5,
               command=self.all_teammates_task,
               ).grid(row=4, column=2)
        Button(self.df,
               text=" סכימה ",
               bd=3,
               font=("", 15),
               padx=5,
               pady=5,
               command=self.schema_dev,
               ).grid(row=4, column=1)
        Button(self.df,
               text=" להתנתק ",
               bd=3,
               font=("", 15),
               padx=5,
               pady=5,
               command=self.login_frame,
               ).grid(row=4, column=0)
        self.messages(self.df, 2)
        self.df.pack()

    def maneger_frame(self):
        self.logf.pack_forget()
        self.head["text"] = "מנהל"
        Label(self.mf, text="שלום ", font=("", 20), pady=10, padx=10).grid(row=0, column=1)
        Label(self.mf, text=self.username.get(), font=("", 20), pady=10, padx=10).grid(row=0, column=0)
        Button(
            self.mf,
            text="פרויקטים",
            bd=3,
            font=("", 15),
            padx=1,
            pady=1,
            command=self.project_frame,
        ).grid(row=1, column=1)
        
        self.messages(self.mf,2)

        self.mf.pack()

    def custumer_frame(self):
        self.logf.pack_forget()
        self.scc.pack_forget()
        self.head["text"] = "לקוח"
        Button(self.cusf,
               text=" סכימה ",
               bd=3,
               font=("", 15),
               padx=5,
               pady=5,
               command=self.schema_cus,
               ).grid(row=4, column=1)
        Button(self.cusf,
               text=" להתנתק ",
               bd=3,
               font=("", 15),
               padx=5,
               pady=5,
               command=self.login_frame,
               ).grid(row=4, column=0)
        self.cusf.pack()

    ## tasks for developer page
    def all_teammates_task(self):
        self.df.pack_forget()
        self.head["text"] = "דף משימות"
        projectAssign = PROJECT_CREW.get_project(self.username.get())
        print(projectAssign)
        tasks = TASK.get_tasks(projectAssign[0])
        crew = PROJECT_CREW.get_crew(projectAssign[0])
        print(tasks)
        Label(self.att, text="מס' מזהה-משימות", font=("", 18), pady=10, padx=10).grid(row=0, column=0)
        r = 0
        for i in tasks:
            r = r + 1
            Label(self.att, text=i[1], font=("", 15), pady=10, padx=10).grid(row=r, column=0)
        r = r + 1
        Label(self.att, text="חברי צוות", font=("", 18), pady=10, padx=10).grid(row=r, column=0)

        for c in crew:
            if c[1] != '' and c[1] != None:
                r += 1
                Label(self.att, text=c[1], font=("", 14), pady=10, padx=10).grid(row=r, column=0)
        r = r + 1
        Button(
            self.att,
            text="חזור",
            bd=3,
            font=("", 15),
            padx=1,
            pady=1,
            command=self.developer_frame,
        ).grid(row=r, column=2)
        self.att.pack()

    def schema_dev(self):
        self.df.pack_forget()
        self.cf.pack_forget()
        self.head["text"] = "סכימת התקדמות"
        Button(
            self.scd,
            text="חזור",
            bd=3,
            font=("", 15),
            padx=1,
            pady=1,
            command=self.developer_frame,
        ).grid(row=2, column=0)
        self.scd.pack()

    def schema_cus(self):
        self.cusf.pack_forget()
        self.cf.pack_forget()
        self.head["text"] = "סכימת התקדמות"
        Button(
            self.scc,
            text="חזור",
            bd=3,
            font=("", 15),
            padx=1,
            pady=1,
            command=self.custumer_frame,
        ).grid(row=2, column=0)
        self.scc.pack()

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
        self.cusf = Frame(self.master, padx=20, pady=30)



        self.pf = Frame(self.master, padx=20, pady=30)     #project frame
        self.apf = Frame(self.master, padx=20, pady=30)  #add project
        self.rpf = Frame(self.master, padx=20, pady=30) #remove project
        self.tf = Frame(self.master, padx=20, pady=30)  # task frame
        self.atf = Frame(self.master, padx=20, pady=30)  # add task frame
        self.shtf = Frame(self.master, padx=20, pady=30)  # show task frame
        self.tef = Frame(self.master, padx=20, pady=30)  #  task editor frame

        self.spf = Frame(self.master, padx=20, pady=30)  # show project frame
        self.pef = Frame(self.master, padx=20, pady=30)  #project editor frame
        self.rtf = Frame(self.master, padx=20, pady=30)  # remove task frame

        self.cf = Frame(self.master, padx=20, pady=30)  # crew frame
        self.att = Frame(self.master, padx=20, pady=100)  # tasks for project frame
        self.scd = Frame(self.master, padx=20, pady=100)  # developer schema frame
        self.scc = Frame(self.master, padx=20, pady=100)  # customer schema frame

    ##################project editor functions##############################

    def project_frame(self):
        self.mf.forget()
        projects=PROJECT.get_projects(self.username.get())


        def back():
            self.pf.forget()
            self.maneger_frame()


        Button(
            self.pf,
            text="חזור",
            bd=3,
            font=("", 15),
            padx=1,
            pady=1,
            command=back, ).grid(row=0, column=1)


        self.head["text"] = "ניהול פרויקט"
        Button(
            self.pf,
            text="הוסף פרויקט",
            bd=3,
            font=("", 15),
            padx=1,
            pady=1,
            command=self.add_proj_frame,
        ).grid(row=1,column=1)
        Button(
            self.pf,
            text="מחק פרויקט",
            bd=3,
            font=("", 15),
            padx=1,
            pady=1,
            command=self.remov_proj_frame, ).grid(row=2,column=1)

        Button(
            self.pf,
            text="הצג פרויקט",
            bd=3,
            font=("", 15),
            padx=1,
            pady=1,
            command=self.show_proj_frame, ).grid(row=3,column=1)

        Label(self.pf, text="*******************", font=("", 20), pady=10, padx=10).grid(row=4,column=0)
        Label(self.pf, text="*******************", font=("", 20), pady=10, padx=10).grid(row=4, column=1)
        Label(self.pf, text="הפרויקטים שלך", font=("", 20), pady=10, padx=10).grid(row=5, column=1)
        Label(self.pf, text="שם הפרויקט", font=("", 20,'underline'), pady=10, padx=10).grid(row=6, column=0)
        Label(self.pf, text="מזהה הפרויקט", font=("", 20,'underline'), pady=10, padx=10).grid(row=6, column=1)
        i=7
        for p in projects:
            Label(self.pf, text="   "+p[1]+"   ", font=("", 20), pady=10, padx=10).grid(row=i, column=0)
            Label(self.pf, text="   "+p[0]+"    ", font=("", 20), pady=10, padx=10).grid(row=i, column=1)
            i=i+1

        Label(self.pf, text="    ", font=("", 20), pady=10, padx=10).grid(row=i, column=0)
        Label(self.pf, text="    ", font=("", 20), pady=10, padx=10).grid(row=i, column=1)
        i = i + 1
        Label(self.pf, text="   ", font=("", 20), pady=10, padx=10).grid(row=i, column=0)
        Label(self.pf, text="   ", font=("", 20), pady=10, padx=10).grid(row=i, column=1)








        self.pf.pack()

    def show_proj_frame(self):
        def back():
            self.spf.forget()
            self.project_frame()
        self.pf.forget()
        self.head["text"] = "הצגת פרויקט"
        Label(self.spf, text="מספר מזהה של פרויקט: ", font=("", 20), pady=10, padx=10).grid(
            row=0, column=1
        )
        Entry(self.spf, textvariable=self.prjNum, bd=5, font=("", 15)).grid(
            row=0, column=0
        )
        Button(
            self.spf,
            text="הצג",
            bd=3,
            font=("", 15),
            padx=1,
            pady=1,
            command=self.proj_editor_frame, ).grid(row=2, column=1)

        Button(
            self.spf,
            text="חזור",
            bd=3,
            font=("", 15),
            padx=1,
            pady=1,
            command=back, ).grid(row=3, column=1)

        self.spf.pack()

    def proj_editor_frame(self):
        proj=PROJECT.get_project(self.username.get(),self.prjNum.get())
        if not proj:
            ms.showerror("שגיאה", "הפרויקט המבוקש לא נמצא")
            return

        self.spf.forget()
        def back():
            self.pef.forget()
            self.project_frame()


        Label(self.pef, text=":שם הפרויקט ", font=("", 20), pady=10, padx=10).grid(row=1, column=1)
        Label(self.pef, text=proj[1], font=("", 20), pady=10, padx=10).grid(row=1, column=0)
        Label(self.pef, text=":מזהה הפרויקט ", font=("", 20), pady=10, padx=10).grid(row=2, column=1)
        Label(self.pef, text=proj[0], font=("", 20), pady=10, padx=10).grid(row=2, column=0)
        Button(self.pef, text="משימות", bd=3, font=("", 15), padx=1, pady=1, command=self.task_frame, ).grid(row=3, column=1)
        self.prjName.set(proj[1])
        Button(self.pef, text="צוות", bd=3, font=("", 15), padx=1, pady=1, command=self.crew_frame, ).grid(row=4,column=1)

        Button(self.pef, text="חזור", bd=3, font=("", 15), padx=1, pady=1, command=back, ).grid(row=5, column=1)

        self.pef.pack()





    def crew_frame(self):
        self.pef.forget()



        def back():
            self.cf.forget()
            self.proj_editor_frame()

        def my_crew():
            j=6
            crew = PROJECT_CREW.get_crew(self.prjNum.get())
            Label(self.cf, text="*******************", font=("", 20), pady=10, padx=10).grid(row=4, column=1)
            Label(self.cf, text="הצוות שלי", font=("", 20, 'underline'), pady=10, padx=10).grid(row=5, column=1)
            for c in crew:
                Label(self.cf, text="   " + c[1] + "   ", font=("", 20), pady=10, padx=10).grid(row=j, column=1)

                j = j + 1

            Label(self.cf, text="            ", font=("", 20), pady=10, padx=10).grid(row=j, column=1)
            j = j + 1
            Label(self.cf, text="            ", font=("", 20), pady=10, padx=10).grid(row=j, column=1)

        def add_crew_member():
            c = self.users_db.cursor()
            sql = "SELECT * FROM users WHERE role = 'developer' AND username=? "
            tp=(self.user_crew.get(),)
            try:
                c.execute(sql,tp)


            except:
                ms.showerror("שגיאה", "משתמש לא נמצא")
                return

            PROJECT_CREW.insert_to_table(self.prjNum.get(), self.user_crew.get())

            msg = "שוייכת לפרויקט מספר "
            msg += self.prjNum.get()



            MESSAGE.new_message(self.username.get(), self.user_crew.get(), msg)
            MESSAGE.printAll()
            my_crew()




        c = self.users_db.cursor()
        # Find user If there is any take proper action
        sql = "SELECT * FROM users WHERE role = 'developer' "
        try:
            c.execute(sql)
            users = c.fetchall()

        except:
            ms.showerror("שגיאה","ניסיון של שליפת משתמשים נכשל")




        Button(
            self.cf,
            text="חזור",
            bd=3,
            font=("", 15),
            padx=1,
            pady=1,
            command=back,
        ).grid(row=2, column=2)

        Button(self.cf, text="הוסף לצוות שלי", bd=3, font=("", 15), padx=1, pady=1, command=add_crew_member, ).grid(row=3, column=0)

        Label(self.cf, text=":שם משתמש ", font=("", 20), pady=10, padx=10).grid(
            row=3, column=2
        )
        Entry(self.cf, textvariable=self.user_crew, bd=5, font=("", 15)).grid(
            row=3, column=1
        )








        Label(self.cf, text="*******************", font=("", 20), pady=10, padx=10).grid(row=4, column=0)
        Label(self.cf, text="עובדים קיימים", font=("", 20,'underline'), pady=10, padx=10).grid(row=5, column=0)
        i = 6
        for u in users:
            Label(self.cf, text="   " + u[0] + "   ", font=("", 20), pady=10, padx=10).grid(row=i, column=0)

            i = i + 1

        Label(self.cf, text="            ", font=("", 20), pady=10, padx=10).grid(row=i, column=0)

        i = i + 1

        Label(self.cf, text="           ", font=("", 20), pady=10, padx=10).grid(row=i, column=0)
        i=i+1

        my_crew()


        self.cf.pack()














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

            self.project_frame()


        def back():
            self.rpf.forget()
            self.project_frame()

        self.head["text"] = "מחיקת פרויקט"
        Label(self.rpf, text="מספר מזהה של פרויקט: ", font=("", 20), pady=10, padx=10).grid(
            row=0, column=0
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
        ).grid(row=1, column=1)

        Button(
            self.rpf,
            text="חזור",
            bd=3,
            font=("", 15),
            padx=1,
            pady=1,
            command=back,
        ).grid(row=2, column=1)


        self.rpf.pack()



    def add_proj_frame(self):

        def back():
            self.apf.forget()
            self.project_frame()

        def add_proj():
            self.apf.forget()
            newp=PROJECT(self.prjNum.get(),self.prjName.get(),self.username.get())
            newp.insert_to_table()
            self.project_frame()


        self.pf.forget()

        self.head["text"] = "הוספת פרויקט"
        Label(self.apf, text="מספר מזהה של פרויקט: ", font=("", 20), pady=10, padx=10).grid(
            row=0, column=0
        )
        Entry(self.apf, textvariable=self.prjNum, bd=5, font=("", 15)).grid(
            row=0, column=1
        )
        Label(self.apf, text="שם של פרויקט: ", font=("", 20), pady=10, padx=10).grid(row=1, column=0)
        Entry(self.apf, textvariable=self.prjName, bd=5, font=("", 15)).grid(row=1, column=1)

        Button(
            self.apf,
            text="הוסף",
            bd=3,
            font=("", 15),
            padx=1,
            pady=1,
            command=add_proj,
        ).grid(row=2, column=1)

        Button(
            self.apf,
            text="חזור",
            bd=3,
            font=("", 15),
            padx=1,
            pady=1,
            command=back,
        ).grid(row=3, column=1)





        self.apf.pack()



   ###################end project editor functions##############################

   ###########task editor##############

    def add_task_frame(self):
        self.tf.forget()
        def back():
            self.atf.forget()
            self.task_frame()

        def add_task():
            t=TASK(self.taskId.get(),self.time.get(),self.crew.get(),self.prjNum.get())
            t.insert_to_table()



        Button(self.atf, text="חזור", bd=3, font=("", 15), padx=1, pady=1, command=back, ).grid(row=0, column=1)
        Label(self.atf, text=":מזהה של משימה ", font=("", 20), pady=10, padx=10).grid(row=1, column=1 )
        Entry(self.atf, textvariable=self.taskId, bd=5, font=("", 15)).grid(row=1, column=0)
        Label(self.atf, text=":מספר שעות מוערך להשלמת משימה ", font=("", 20), pady=10, padx=10).grid(row=2, column=1)
        Entry(self.atf, textvariable=self.time, bd=5, font=("", 15)).grid(row=2, column=0)
        Label(self.atf, text=":מספר צוות דרוש ", font=("", 20), pady=10, padx=10).grid(row=3, column=1)
        Entry(self.atf, textvariable=self.crew, bd=5, font=("", 15)).grid(row=3, column=0)

        Button(
            self.atf,
            text="הוסף",
            bd=3,
            font=("", 15),
            padx=1,
            pady=1,
            command=add_task,
        ).grid(row=4, column=0)



        self.head["text"] = "הוספת משימה"
        self.atf.pack()

    def add_task_frame_developer(self):
        self.tf.forget()
        self.df.forget()
        def back():
            self.atf.forget()
            self.task_frame()

        def add_task_developer():
            t=TASK(self.taskId.get(),self.time.get(),self.crew.get(),self.prjNum.get())
            t.insert_to_table()



        Button(self.atf, text="חזור", bd=3, font=("", 15), padx=1, pady=1, command= self.developer_frame, ).grid(row=0, column=1)
        Label(self.atf, text=":מזהה של משימה ", font=("", 20), pady=10, padx=10).grid(row=1, column=1 )
        Entry(self.atf, textvariable=self.taskId, bd=5, font=("", 15)).grid(row=1, column=0)
        Label(self.atf, text=":מספר שעות מוערך להשלמת משימה ", font=("", 20), pady=10, padx=10).grid(row=2, column=1)
        Entry(self.atf, textvariable=self.time, bd=5, font=("", 15)).grid(row=2, column=0)
        Label(self.atf, text=":מספר צוות דרוש ", font=("", 20), pady=10, padx=10).grid(row=3, column=1)
        Entry(self.atf, textvariable=self.crew, bd=5, font=("", 15)).grid(row=3, column=0)

        Button(
            self.atf,
            text="הוסף",
            bd=3,
            font=("", 15),
            padx=1,
            pady=1,
            command=add_task_developer,
        ).grid(row=4, column=0)



        self.head["text"] = "הוספת משימה"
        self.atf.pack()

    def remove_task_frame(self):
        self.tf.forget()

        def back():
            self.rtf.forget()
            self.task_frame()

        def remove():
            TASK.delet_task(self.prjNum.get(),self.taskId.get())



        Button(self.rtf, text="חזור", bd=3, font=("", 15), padx=1, pady=1, command=back, ).grid(row=3, column=0)

        Label(self.rtf, text=":מזהה של משימה ", font=("", 20), pady=10, padx=10).grid(
            row=1, column=1
        )
        Entry(self.rtf, textvariable=self.taskId, bd=5, font=("", 15)).grid(
            row=1, column=0
        )

        Button(
            self.rtf,
            text="מחק",
            bd=3,
            font=("", 15),
            padx=1,
            pady=1,
            command=remove,
        ).grid(row=2, column=0)

        self.rtf.pack()

    def remove_task_frame_developer(self):
        self.tf.forget()

        def back():
            self.rtf.forget()
            self.task_editor_frame_developer()

        def remove():
            TASK.delet_task(self.prjNum.get(),self.taskId.get())



        Button(self.rtf, text="חזור", bd=3, font=("", 15), padx=1, pady=1, command=back, ).grid(row=3, column=0)

        Label(self.rtf, text=":מזהה של משימה ", font=("", 20), pady=10, padx=10).grid(
            row=1, column=1
        )
        Entry(self.rtf, textvariable=self.taskId, bd=5, font=("", 15)).grid(
            row=1, column=0
        )

        Button(
            self.rtf,
            text="מחק",
            bd=3,
            font=("", 15),
            padx=1,
            pady=1,
            command=remove,
        ).grid(row=2, column=0)

        self.rtf.pack()

    def task_editor_frame_developer(self):
        t = TASK.get_task(self.taskId.get(),self.prjNum.get())
        if not t:
            ms.showerror("error", "המשימה המבוקשת לא נמצאת")
            return

        def back():
            self.tef.forget()
            self.developer_frame

        def message_crew():
            crew=PROJECT_CREW.get_crew(self.prjNum.get())
            msg="בפרויקט מספר "
            msg+=self.prjNum.get()
            msg+="יש שינוי במשימה "
            msg+=self.taskId.get()

            for c in crew:
                MESSAGE.new_message(self.username.get(),c[1],msg)
            MESSAGE.printAll()



        def change_h():
            TASK.update_hour(self.prjNum.get(),self.taskId.get(),self.time.get())
            Label(self.tef, text=self.time.get(), font=("", 20), pady=10, padx=10).grid(
                row=1, column=0
            )
            message_crew()

        def change_c():
            TASK.update_crew(self.prjNum.get(),self.taskId.get(),self.crew.get())
            Label(self.tef, text=self.crew.get(), font=("", 20), pady=10, padx=10).grid(
                row=2, column=0
            )
            message_crew()

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

        Entry(self.tef, textvariable=self.time, bd=5, font=("", 15)).grid(row=3, column=0)
        Button(self.tef, text="שנה מספר שעות ", bd=3, font=("", 15), padx=1, pady=1, command=change_h, ).grid(row=3, column=1)

        Entry(self.tef, textvariable=self.crew, bd=5, font=("", 15)).grid(row=4, column=0)
        Button(self.tef, text="שנה כמות צוות", bd=3, font=("", 15), padx=1, pady=1, command=change_c, ).grid(row=4,column=1)


        Button(self.tef, text="חזור", bd=3, font=("", 15), padx=1, pady=1, command=back, ).grid(row=5, column=0)




        self.tef.pack()

    def task_editor_frame(self):
        t = TASK.get_task(self.taskId.get(),self.prjNum.get())
        if not t:
            ms.showerror("error", "המשימה המבוקשת לא נמצאת")
            return

        def back():
            self.tef.forget()
            self.task_frame()

        def message_crew():
            crew=PROJECT_CREW.get_crew(self.prjNum.get())
            msg="בפרויקט מספר "
            msg+=self.prjNum.get()
            msg+="יש שינוי במשימה "
            msg+=self.taskId.get()

            for c in crew:
                MESSAGE.new_message(self.username.get(),c[1],msg)
            MESSAGE.printAll()



        def change_h():
            TASK.update_hour(self.prjNum.get(),self.taskId.get(),self.time.get())
            Label(self.tef, text=self.time.get(), font=("", 20), pady=10, padx=10).grid(
                row=1, column=0
            )
            message_crew()

        def change_c():
            TASK.update_crew(self.prjNum.get(),self.taskId.get(),self.crew.get())
            Label(self.tef, text=self.crew.get(), font=("", 20), pady=10, padx=10).grid(
                row=2, column=0
            )
            message_crew()

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

        Entry(self.tef, textvariable=self.time, bd=5, font=("", 15)).grid(row=3, column=0)
        Button(self.tef, text="שנה מספר שעות ", bd=3, font=("", 15), padx=1, pady=1, command=change_h, ).grid(row=3, column=1)

        Entry(self.tef, textvariable=self.crew, bd=5, font=("", 15)).grid(row=4, column=0)
        Button(self.tef, text="שנה כמות צוות", bd=3, font=("", 15), padx=1, pady=1, command=change_c, ).grid(row=4,column=1)


        Button(self.tef, text="חזור", bd=3, font=("", 15), padx=1, pady=1, command=back, ).grid(row=5, column=0)




        self.tef.pack()



    def show_task_frame(self):
        def back():
            self.shtf.forget()
            self.task_frame()
        self.tf.forget()

        Button(self.shtf, text="חזור", bd=3, font=("", 15), padx=1, pady=1, command=back, ).grid(row=3, column=0)

        Label(self.shtf, text=":מזהה של משימה ", font=("", 20), pady=10, padx=10).grid(
            row=1, column=1
        )
        Entry(self.shtf, textvariable=self.taskId, bd=5, font=("", 15)).grid(
            row=1, column=0
        )

        Button(
            self.shtf,
            text="הצג",
            bd=3,
            font=("", 15),
            padx=1,
            pady=1,
            command=self.task_editor_frame,
        ).grid(row=2, column=0)

        self.shtf.pack()








    def task_frame(self):
        self.pef.forget()

        tasks=TASK.get_tasks(self.prjNum.get())

        def back():
            self.tf.forget()
            self.project_frame()

        self.head["text"] = "ניהול משימות"
        Label(self.tf, text=":משימות של פרויקט ", font=("", 20), pady=10, padx=10).grid(row=0, column=1)
        Label(self.tf, text=self.prjName.get(), font=("", 20), pady=10, padx=10).grid(row=0, column=0)

        Button(self.tf, text="חזור", bd=3, font=("", 15), padx=1, pady=1, command=back, ).grid(row=1, column=1)
        Button(self.tf, text="הוסף משימה", bd=3, font=("", 15), padx=1, pady=1, command=self.add_task_frame, ).grid(row=2, column=1)
        Button(self.tf, text="הצג משימה", bd=3, font=("", 15), padx=1, pady=1, command=self.show_task_frame, ).grid(row=3, column=1)
        Button(self.tf, text="מחק משימה", bd=3, font=("", 15), padx=1, pady=1, command=self.remove_task_frame, ).grid(
            row=4, column=1)



        Label(self.tf, text="******************", font=("", 20), pady=10, padx=10).grid(row=7, column=0)
        Label(self.tf, text="******************", font=("", 20), pady=10, padx=10).grid(row=7, column=1)
        Label(self.tf, text="******************", font=("", 20), pady=10, padx=10).grid(row=7, column=2)
        Label(self.tf, text="משימות קיימות בפרויקט", font=("", 20), pady=10, padx=10).grid(row=8, column=1)

        Label(self.tf, text="מזהה משימה", font=("", 20,'underline'), pady=10, padx=10).grid(row=9, column=2)
        Label(self.tf, text="מספר שעות מוערך", font=("", 20,'underline'), pady=10, padx=10).grid(row=9, column=1)
        Label(self.tf, text="מספר צוות דרוש", font=("", 20,'underline'), pady=10, padx=10).grid(row=9, column=0)
        i = 10
        for t in tasks:
            Label(self.tf, text="   "+t[1]+"   ", font=("", 20), pady=10, padx=10).grid(row=i, column=2)
            Label(self.tf, text="   "+t[2]+"   ", font=("", 20), pady=10, padx=10).grid(row=i, column=1)
            Label(self.tf, text="   "+t[3]+"   ", font=("", 20), pady=10, padx=10).grid(row=i, column=0)
            i = i + 1

        Label(self.tf, text="     ", font=("", 20), pady=10, padx=10).grid(row=i, column=2)
        Label(self.tf, text="     ", font=("", 20), pady=10, padx=10).grid(row=i, column=1)
        Label(self.tf, text="     ", font=("", 20), pady=10, padx=10).grid(row=i, column=0)
        i = i + 1
        Label(self.tf, text="     ", font=("", 20), pady=10, padx=10).grid(row=i, column=2)
        Label(self.tf, text="     ", font=("", 20), pady=10, padx=10).grid(row=i, column=1)
        Label(self.tf, text="     ", font=("", 20), pady=10, padx=10).grid(row=i, column=0)




        self.tf.pack()




   #########end of task editor##############

    def messages(self, Widgets, r):   #### show the messages the the user have
        #width----the frame u use ( --self.df--- for example)
        # r---the row u want to print the messages
        msg = MESSAGE.get_my_mesagges(self.username.get())
        if not msg:
            Label(Widgets, text="אין הודעות", font=("", 20), pady=10, padx=10).grid(row=r, column=1)

        else:
            Label(Widgets, text="שולח ההודעה", font=("", 20, 'underline'), pady=10, padx=10).grid(row=r, column=1)
            Label(Widgets, text="ההודעה", font=("", 20, 'underline'), pady=10, padx=10).grid(row=r, column=0)
            r = r + 1
            for m in msg:
                Label(Widgets, text=m[0], font=("", 20), pady=10, padx=10).grid(row=r, column=1)
                Label(Widgets, text=m[2], font=("", 20), pady=10, padx=10).grid(row=r, column=0)
                r = r + 1



root = Tk()
main(root)
root.mainloop()
