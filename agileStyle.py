import tkinter
from tkinter import *
from tkinter import messagebox as ms
import tkinter as tk
import mysql.connector
import matplotlib
from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

# import numpy as np

# from typing import List, Any

# from docx import Document
# from docx.shared import Inches

import os

# make database and users (if not exists already) table at programme start up
# import numpy
import datetime as dt

# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# from matplotlib.figure import Figure
# pandas import DataFrame

users = mysql.connector.connect(
    host="b0cqj1javyo2et169rya-mysql.services.clever-cloud.com",
    user="usqjg0g0nbwvdfdf",
    passwd="88KJ85sZX1CKqSFyzJ09",
    database="b0cqj1javyo2et169rya"
)

# users.cursor().execute("drop table users")

users.cursor().execute(
    "CREATE TABLE IF NOT EXISTS users (username VARCHAR(255) PRIMARY KEY ,password VARCHAR(255), role VARCHAR(255))"
)

# print(users.cursor().execute("SELECT username,role FROM users").fetchall())

Maneger = "manager"
Developer = "developer"
Custumer = "customer"

imgs = {}

##########################################################################################
# creat database if not exist and get conecction to it
conect = users

# get a cursor to execute sql statements
cc = conect.cursor(buffered=True)
#sql= '''DROP TABLE projects'''
#cc.execute(sql)
# creat table
sql = '''CREATE TABLE IF NOT EXISTS projects
    (projId VARCHAR(255) PRIMARY KEY,
        name VARCHAR(255),
        managerId VARCHAR(255),
        end DATE)'''
cc.execute(sql)

# sql = '''DROP TABLE userstory#
# /          '''
# cc.execute(sql)

sql = '''CREATE TABLE IF NOT EXISTS userstory 
        (projectid VARCHAR(700) PRIMARY KEY ,
        project_description VARCHAR(255))
        '''
cc.execute(sql)

sql = '''CREATE TABLE IF NOT EXISTS project_tasks
         (projId VARCHAR(255) NOT NULL,
          taskId VARCHAR(255) NOT NULL,
          time VARCHAR(255),
          crew VARCHAR(255) ,
          status VARCHAR(255),
          priorty VARCHAR(255),
          description VARCHAR(255),
          PRIMARY KEY (projId,taskId))
          '''
cc.execute(sql)

sql = '''CREATE TABLE IF NOT EXISTS project_crew
         (projId VARCHAR(255) NOT NULL,
          user VARCHAR(255) NOT NULL,
          PRIMARY KEY (projId,user))
          '''
cc.execute(sql)

sql = '''CREATE TABLE IF NOT EXISTS sprints 
         (
          sprintNum VARCHAR(255) NOT NULL,
          projectId VARCHAR(255) NOT NULL,
          timeLeft VARCHAR(255) NOT NULL,
          status VARCHAR(255) NOT NULL,
          PRIMARY KEY (sprintNum,projectId)
        )
          '''
cc.execute(sql)

conect.commit()

sql = '''CREATE TABLE IF NOT EXISTS taskSprint 
         (
          taskId VARCHAR(255) NOT NULL,
          projectId VARCHAR(255) NOT NULL,
          sprintNum VARCHAR(255) NOT NULL,
          description VARCHAR(255) ,
          PRIMARY KEY (taskId,projectId,sprintNum)
        )
          '''

cc.execute(sql)

conect.commit()
sql = '''CREATE TABLE IF NOT EXISTS user_message
         (
          sender VARCHAR(255) NOT NULL,
          to_user VARCHAR(255) NOT NULL,
          message VARCHAR(255) )

          '''
cc.execute(sql)

###הערות על משימות#
sql = '''CREATE TABLE IF NOT EXISTS Remarks 
         (
          projId VARCHAR(255) NOT NULL,
          taskId VARCHAR(255) NOT NULL,
          title VARCHAR(255) NOT NULL,
          user VARCHAR(255) NOT NULL,
          remark VARCHAR(255)  NOT NULL
        )
          '''

###טבלה לשיוך לקוחות לפרויקטיחם#
sql = '''CREATE TABLE IF NOT EXISTS proj_cust 
         (
          projId VARCHAR(255) NOT NULL,
          user VARCHAR(255) NOT NULL
        )
          '''
cc.execute(sql)

conect.commit()


###########################################################################################


# ************project class**********************************#
class PROJECT:
    def __init__(self, projId, name, us,date):
        self.projId = projId
        self.name = name
        self.user = us  # usrename
        self.date=date

    def insert_to_table(self):
        connect = users
        cc = connect.cursor(buffered=True)
        sql = '''INSERT INTO projects VALUES(%s,%s,%s,%s)
        '''
        dats_tuple = (self.projId, self.name, self.user,self.date)
        try:
            cc.execute(sql, dats_tuple)
            ms.showinfo("פרויקט חדש נוצר בהצלחה")
        except Exception:
            ms.showerror("שגיאה!", " נסיון להכניס פרויקט חדש לטבלה נכשל")
        connect.commit()

    @classmethod
    def printAll(cls):

        print("projects: ")
        connect = users
        cc = connect.cursor(buffered=True)

        sql = 'SELECT * FROM projects'
        cc.execute(sql)
        rows = cc.fetchall()

        for row in rows:
            print(row)
        connect.commit()

    @classmethod
    def projectManager(cls, id):

        print("select project manager by project id: " + id)

        connect = users
        cc = connect.cursor(buffered=True)

        sql = """SELECT managerId 
            FROM projects 
            where projId=%s         

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

    @classmethod
    def remove_by_id(cls, id):
        connect = users
        cc = connect.cursor(buffered=True)
        sql = """DELETE FROM projects 
                           WHERE projId=%s 


                           """
        dt = (id,)
        try:
            cc.execute(sql, dt)
            ms.showinfo("בוצע", "נמחק פרויקט: " + id)

        except Exception:
            ms.showerror("שגיאה", "שגיאה בזמן מחיקת פרויקט")
        connect.commit()

    @classmethod
    def get_projects(cls, manger_id):  # get projects by manager id (username)
        connect = users
        cc = connect.cursor(buffered=True)
        sql = """SELECT * FROM projects 
                               WHERE  managerId=%s 


                               """
        dt = (manger_id,)
        try:
            cc.execute(sql, dt)
            rows = cc.fetchall()
            return rows



        except Exception:
            ms.showerror("שגיאה", "שגיאה בזמן משיכת פרויקטים")
        connect.commit()

    @classmethod
    def get_project(cls, manger_id, proj_id):  # get project by manager id and project id
        connect = users
        cc = connect.cursor(buffered=True)
        sql = """SELECT * FROM projects 
                               WHERE  managerId=%s 
                               AND projId=%s


                               """

        dt = (manger_id, proj_id)
        try:
            cc.execute(sql, dt)
            row = cc.fetchone()

            return row



        except Exception:
            ms.showerror("שגיאה", "שגיאה בזמן משיכת פרויקט")
        connect.commit()

    @classmethod
    def get_project_c(cls, name, proj_id):
        connect = users
        cc = connect.cursor(buffered=True)
        sql = """SELECT * FROM projects 
                               WHERE  name=%s
                               AND projId=%s


                               """

        dt = (name, proj_id)
        try:
            cc.execute(sql, dt)
            row = cc.fetchone()

            return row

        except Exception:
            ms.showerror("שגיאה", "שגיאה בזמן משיכת פרויקט")
        connect.commit()

    @classmethod
    def get_project_by_projId(cls, proj_id):
        connect = users
        cc = connect.cursor(buffered=True)
        sql = """SELECT * FROM projects 
                                   WHERE  projId=%s


                                   """

        dt = (proj_id,)
        try:
            cc.execute(sql, dt)
            row = cc.fetchone()

            return row

        except Exception:
            ms.showerror("שגיאה", "שגיאה בזמן משיכת פרויקט")
        connect.commit()

    # **************class Sprint*********************************#


class SPRINT:
    def __init__(self, sprintNum, projectId, timeLeft, status):
        self.sprintNum = sprintNum
        self.projectId = projectId
        self.timeLeft = timeLeft
        self.status = status

    def get_sprints(cls, pid):
        connect = users
        cc = connect.cursor(buffered=True)

        sql = """SELECT * 
                         FROM sprints
                         where  projectId=%s      

                                         """
        dt = (pid,)

        try:

            cc.execute(sql, dt)
            rows = cc.fetchall()
            return rows
        except Exception:
            ms.showerror("error", "שגיאה בזמן משיכת ספרינט")

        connect.commit()

    def get_sprints_by_num(sid, pid):
        connect = users
        cc = connect.cursor(buffered=True)

        sql = """SELECT * 
                         FROM sprints
                         WHERE  sprintNum=%s
                         AND projectId=%s      

                                         """
        dt = (sid, pid,)

        try:

            cc.execute(sql, dt)
            rows = cc.fetchall()
            return rows
        except Exception:
            ms.showerror("error", "שגיאה בזמן משיכת ספרינט")

        connect.commit()

    def insert_to_table(self):
        conect = users
        cc = conect.cursor(buffered=True)
        sql = '''INSERT INTO sprints VALUES(%s,%s,%s,%s)
          '''
        dats_tuple = (self.sprintNum, self.projectId, self.timeLeft, self.status)

        try:
            cc.execute(sql, dats_tuple)
            ms.showinfo("הושלם", "ספרינט חדש נוצר בהצלחה")

        except Exception:
            ms.showerror("שגיאה", "שגיאה! נסיון להכניס משימה חדשה לטבלה נכשל")

        conect.commit()

    @classmethod
    def delete_sprint(cls, pid, sid):
        connect = users
        cc = connect.cursor(buffered=True)

        sql = """DELETE FROM sprints
                             where  projectId=%s  
                             AND sprintNum=%s

                                             """
        dt = (pid, sid)

        try:

            cc.execute(sql, dt)
            ms.showinfo("", "ספרינט נמחק בהצלחה")
        except Exception:
            ms.showerror("error", "שגיאה ניסיון מחיקת ספרינט ")

        connect.commit()

    @classmethod
    def update_num(cls, pid, sid, time, status):
        connect = users
        c = connect.cursor(buffered=True)
        sql = """UPDATE sprints
                                 SET sprintNum=%s
                                 WHERE projectId=%s  
                                 AND timeLeft=%s
                                 AND status=%s    

                                                 """
        dt = (sid, pid, time, status)
        try:

            cc.execute(sql, dt)
            ms.showinfo("", "מספר הספרינט עודכן בהצלחה ")
        except Exception:
            ms.showerror("error", "שגיאה בעידכון מספר ספרינט ")

        connect.commit()

    @classmethod
    def update_time(cls, pid, sid, time, status):
        connect = users
        c = connect.cursor(buffered=True)
        sql = """UPDATE sprints
                                 SET timeLeft=%s
                                 WHERE projectId=%s  
                                 AND sprintNum=%s 

                                                 """
        dt = (time, pid, sid)
        try:

            cc.execute(sql, dt)
            ms.showinfo("", "מספר ימים עודכן בהצלחה ")
        except Exception:
            ms.showerror("error", "שגיאה בעידכון מספר ימים ")

        connect.commit()

    @classmethod
    def update_status(cls, pid, sid, time, status):
        connect = users
        c = connect.cursor(buffered=True)
        sql = """UPDATE sprints 
                            SET status=%s 
                            where projectId=%s 
                            AND sprintNum=%s
                            """
        dt = (status, pid, sid)
        try:

            cc.execute(sql, dt)
            ms.showinfo("", "סטאטוס עודכן בהצלחה ")
            connect.commit()
        except Exception:
            ms.showerror("error", "שגיאה בעידכון סטאטוס ")

        connect.commit()


class TASK_SPRINT:
    def __init__(self, taskId, projectId, sprintNum):
        self.sprintNum = sprintNum
        self.projectId = projectId
        self.taskId = taskId

    def addTask(tid, pid, sid, des):
        conect = users
        cc = conect.cursor(buffered=True)
        sql = '''INSERT INTO taskSprint VALUES(%s,%s,%s,%s)
                  '''
        dats_tuple = (tid, pid, sid, des,)

        try:
            cc.execute(sql, dats_tuple)
            ms.showinfo("משימה נוספה בהצלחה")

        except Exception:
            ms.showerror("שגיאה! נסיון להכניס משימה חדשה לטבלה נכשל")

        conect.commit()

    def deleteTask(tid, pid, sid):
        connect = users
        cc = connect.cursor(buffered=True)

        sql = """DELETE FROM taskSprint
                                     where  projectId=%s  
                                     AND sprintNum=%s
                                     AND taskId=%s

                                                     """
        dt = (pid, sid, tid)

        try:

            cc.execute(sql, dt)
            ms.showinfo("", "משימה הוסרה בהצלחה")
        except Exception:
            ms.showerror("error", "שגיאה ניסיון הסרת משימה ")

        connect.commit()

    def get_sprint_tasks(pid, sid):
        connect = users
        cc = connect.cursor(buffered=True)

        sql = """SELECT * FROM taskSprint WHERE projectId=%s AND sprintNum=%s
                                         """
        dt = (pid, sid,)

        try:

            cc.execute(sql, dt)
            rows = cc.fetchall()
            print(rows)

            return rows
        except Exception:
            ms.showerror("error", "שגיאה בזמן משיכת משימות לספרינט")

        connect.commit()


# *************end of project class**********************************#
class DISCRIPTION:
    def __init__(self, projNum, discription):
        self.projnum = projNum
        self.discription = discription

    def insert_to_table(self):
        conect = users
        cc = conect.cursor(buffered=True)
        sql = '''INSERT INTO userstory VALUES(%s,%s)'''
        dats_tuple = (self.projnum, self.discription)
        try:
            cc.execute(sql, dats_tuple)
            ms.showinfo("תיאור חדש נוצרה בהצלחה")

        except Exception:
            ms.showerror("שגיאה! נסיון להכניס תיאור חדש לטבלה נכשל")

        conect.commit()


# **************task class*********************************#
class TASK:
    def __init__(self, taskId, time, crewN, projId, status, priorty, description):
        self.taskId = taskId
        self.time = time
        self.crewNum = crewN
        self.projId = projId
        self.status = status
        self.priorty = priorty
        self.description = description

    def insert_to_table(self):
        conect = users
        cc = conect.cursor(buffered=True)
        sql = '''INSERT INTO project_tasks VALUES(%s,%s,%s,%s,%s,%s,%s)
         '''
        dats_tuple = (self.projId, self.taskId, self.time, self.crewNum, self.status, self.priorty, self.description)

        try:
            cc.execute(sql, dats_tuple)
            ms.showinfo("משימה חדשה נוצרה בהצלחה")

        except Exception:
            ms.showerror("שגיאה! נסיון להכניס משימה חדשה לטבלה נכשל")

        conect.commit()

    @classmethod
    def printAll(cls):
        connect = users
        cc = connect.cursor(buffered=True)

        sql = 'SELECT * FROM project_tasks'
        try:

            cc.execute(sql)
            rows = cc.fetchall()
            for row in rows:
                print(row)
        except Exception:
            ms.showerror("שגיאה! נסיון למשוך משימות נכשל")

        connect.commit()

    @classmethod
    def get_task(cls, tid, pid):
        connect = users
        cc = connect.cursor(buffered=True)

        sql = """SELECT * 
                    FROM project_tasks
                    where taskId=%s  
                    AND projId=%s      

                                    """
        dt = (tid, pid)
        try:
            cc.execute(sql, dt)
            r = cc.fetchone()
            return r


        except Exception:
            ms.showerror("error", "שגיאה בזמן משיכת משימה")

        connect.commit()

    @classmethod
    def get_tasks(cls, pid):
        connect = users
        cc = connect.cursor(buffered=True)

        sql = """SELECT * 
                        FROM project_tasks
                        where  projId=%s      

                                        """
        dt = (pid,)

        try:

            cc.execute(sql, dt)
            rows = cc.fetchall()
            return rows
        except Exception:
            ms.showerror("error", "שגיאה בזמן משיכת משימה")

        connect.commit()

    @classmethod
    def update_hour(cls, pid, tid, time):
        connect = users
        cc = connect.cursor(buffered=True)

        sql = """UPDATE project_tasks
                        SET time=%s
                        where  projId=%s  
                        AND taskId=%s    

                                        """
        dt = (time, pid, tid)

        try:

            cc.execute(sql, dt)
            ms.showinfo("", "מספר השעות עודכן בהצלחה ")
        except Exception:
            ms.showerror("error", "שגיאה בעידכון שעה ")

        connect.commit()

    @classmethod
    def update_crew(cls, pid, tid, crew):
        connect = users
        cc = connect.cursor(buffered=True)

        sql = """UPDATE project_tasks
                        SET time=%s
                        where  projId=%s  
                        AND taskId=%s    

                                        """
        dt = (crew, pid, tid)

        try:

            cc.execute(sql, dt)
            ms.showinfo("", "מספר צוות עודכן בהצלחה ")
        except Exception:
            ms.showerror("error", "שגיאה בעידכון מספר צוות ")

        connect.commit()

    @classmethod
    def update_status(cls, pid, tid, status):
        connect = users
        cc = connect.cursor(buffered=True)

        sql = """UPDATE project_tasks
                        SET status=%s
                        where  projId=%s  
                        AND taskId=%s

                                        """
        dt = (status, pid, tid)

        try:

            cc.execute(sql, dt)
            ms.showinfo("", "סטאטוס משימה עודכן בהצלחה ")
        except Exception:
            ms.showerror("error", "שגיאה בעידכון סטאטוס ")

        connect.commit()

    @classmethod
    def delet_task(cls, pid, tid):
        connect = users
        cc = connect.cursor(buffered=True)

        sql = """DELETE FROM project_tasks
                        where  projId=%s  
                        AND taskId=%s

                                        """
        dt = (pid, tid)

        try:

            cc.execute(sql, dt)
            ms.showinfo("", "משימה נמחקה בהצלחה")
        except Exception:
            ms.showerror("error", "שגיאה ניסיון מחיקת משימה ")

        connect.commit()

    @classmethod
    def update_description(cls, pid, tid, des):
        connect = users
        cc = connect.cursor(buffered=True)

        sql = """UPDATE project_tasks
                        SET description=%s
                        where  projId=%s  
                        AND taskId=%s    

                                        """
        dt = (des, pid, tid)

        try:

            cc.execute(sql, dt)
            ms.showinfo("", "תיאור משימה עודכן בהצלחה ")
        except Exception:
            ms.showerror("error", "שגיאה בתיאור משימה  ")

        connect.commit()


# **************end of task class*********************************#


# ************project crew class**********************************#
class PROJECT_CREW:
    @classmethod
    def insert_to_table(cls, pid, us):
        conect = users
        cc = conect.cursor(buffered=True)
        sql = '''INSERT INTO project_crew VALUES(%s,%s)
         '''
        dats_tuple = (pid, us)

        try:
            cc.execute(sql, dats_tuple)
            ms.showinfo(":עובד חדש נוסף לפרויקט" + pid)

        except Exception:
            ms.showerror("שגיאה! נסיון להכניס עובד חדש לטבלה נכשל")

        conect.commit()

    @classmethod
    def get_crew(cls, pid):
        conect = users
        cc = conect.cursor(buffered=True)
        sql = '''SELECT * FROM project_crew 
                 WHERE projId=%s
             '''
        dats_tuple = (pid,)

        try:
            cc.execute(sql, dats_tuple)
            rows = cc.fetchall()
            return rows

        except Exception:
            ms.showerror("שגיאה", "נסיון למשוך צוות עובדים נכשל")

        conect.commit()

    @classmethod
    def get_project(cls, username):
        connect = users
        cc = connect.cursor(buffered=True)
        sql = 'SELECT projId FROM project_crew WHERE  user=%s'
        cc.execute(sql, (username,))
        row = cc.fetchone()
        print(row)
        return row

    @classmethod
    def get_developer_projects(cls, user):
        conect = users
        cc = conect.cursor(buffered=True)
        sql = '''SELECT * FROM project_crew 
                 WHERE user=%s
             '''
        dats_tuple = (user,)

        try:
            cc.execute(sql, dats_tuple)
            rows = cc.fetchall()
            return rows

        except Exception:
            ms.showerror("שגיאה", "נסיון למשוך פרויקטים נכשל")

        conect.commit()


# ************end of project crew class**********************************#

# ************message  class**********************************#
class MESSAGE:
    @classmethod
    def new_message(cls, sender, to, message):
        conect = users
        cc = conect.cursor(buffered=True)
        sql = '''INSERT INTO user_message VALUES(%s,%s,%s)
                '''
        dats_tuple = (sender, to, message)

        try:
            cc.execute(sql, dats_tuple)
            ms.showinfo("", ":הודעה נשלחה בהצלחה ל" + to)

        except Exception:
            ms.showerror("שגיאה", "נסיון לשלוח הודעה נכשל נכשל")

        conect.commit()

    @classmethod
    def printAll(cls):
        connect = users
        cc = connect.cursor(buffered=True)

        sql = 'SELECT * FROM user_message'
        try:

            cc.execute(sql)
            rows = cc.fetchall()
            for row in rows:
                print(row)
        except Exception:
            ms.showerror("שגיאה", "שגיאה! נסיון למשוך הודעות נכשל")

        connect.commit()

    @classmethod
    def get_my_mesagges(cls, us):
        connect = users
        print(connect)
        print("***")
        cc = connect.cursor(buffered=True)

        sql = 'SELECT * FROM user_message where to_user=%s '
        tp = (us,)
        try:

            cc.execute(sql, tp)
            rows = cc.fetchall()
            return rows
        except Exception:
            ms.showerror("שגיאה", "שגיאה! נסיון למשוך הודעות נכשל")

        connect.commit()


# ************end of message  class**********************************#

# ************Remark class**********************************#
class REMARK:
    @classmethod
    def new_remark(cls, projId, taskId, title, user, remark):
        conect = users
        cc = conect.cursor(buffered=True)
        sql = '''INSERT INTO Remarks VALUES(%s,%s,%s,%s,%s)
                                   '''
        dats_tuple = (projId, taskId, title, user, remark)

        try:
            cc.execute(sql, dats_tuple)
            ms.showinfo("", "נוספה הערה חדשה")

        except Exception:
            ms.showerror("שגיאה", "נסיון להוסיף הערה נכשל")

        conect.commit()

    @classmethod
    def get_task_remarks(cls, projId, taskId):
        connect = users
        print(connect)

        cc = connect.cursor(buffered=True)

        sql = 'SELECT * FROM Remarks where projId=%s AND taskId=%s '
        tp = (projId, taskId)
        try:

            cc.execute(sql, tp)
            rows = cc.fetchall()
            return rows
        except Exception:
            ms.showerror("שגיאה", "שגיאה! נסיון למשוך הערות נכשל")

        connect.commit()

    @classmethod
    def remove_remark(cls, projId, taskId, title):
        connect = users
        print(connect)
        print("***")
        cc = connect.cursor(buffered=True)

        sql = 'SELECT * FROM Remarks where projId=%s AND taskId=%s AND title=%s '
        tp = (projId, taskId, title)
        try:

            cc.execute(sql, tp)
            rows = cc.fetchall()
            return rows
        except Exception:
            ms.showerror("שגיאה", "שגיאה! נסיון למשוך הערות נכשל")

        connect.commit()


class PROJECT_customer:
    @classmethod
    def add_cust(cls, projId, user):
        conect = users
        cc = conect.cursor(buffered=True)
        sql = '''INSERT INTO proj_cust VALUES(%s,%s)
                                   '''
        dats_tuple = (projId, user)

        try:
            cc.execute(sql, dats_tuple)
            ms.showinfo("", "לקוח שוייך לפרויקט")

        except Exception:
            ms.showerror("שגיאה", "נסיון לשייך לקוח נכשל")

        conect.commit()

    @classmethod
    def get_proj(cls, user):
        conect = users
        cc = conect.cursor(buffered=True)
        tp = (user,)

        sql = 'SELECT * FROM proj_cust where user=%s  '

        try:

            cc.execute(sql, tp)
            rows = cc.fetchall()
            return rows
        except Exception:
            ms.showerror("שגיאה", "שגיאה! נסיון למשוך פרויקטים נכשל")

        conect.commit()


# ************end of remark class**********************************#


# main Class
class main:
    def __init__(self, master):
        # Window
        self.master = master
        # Some Usefull variables

        self.date= StringVar
        self.discriptuon = StringVar()
        self.username = StringVar()
        self.password = StringVar()
        self.role = StringVar()
        self.age = StringVar()
        self.priorty = StringVar()
        self.users_db = users
        self.n_username = StringVar()
        self.n_password = StringVar()
        self.n_role = StringVar()
        self.classname = StringVar()
        self.resetPass = StringVar()
        self.findName = StringVar()
        self.widgets()
        self.prjNum = StringVar()
        self.prjName = StringVar()
        self.taskId = StringVar()
        self.time = StringVar()
        self.crew = StringVar()
        self.user_crew = StringVar()
        self.status = StringVar()
        self.description = StringVar()
        self.title = StringVar()
        self.remark = StringVar()
        self.cust_username = StringVar()
        self.sprintNum = StringVar()
        self.sprintTime = StringVar()
        self.sprintStatus = StringVar()
        self.messageTo = StringVar()

    # Login Function
    def login(self):
        # Establish Connection
        # with sqlite3.connect('quit.db') as db:
        c = self.users_db.cursor(buffered=True)
        # Find user If there is any take proper action
        find_user = "SELECT * FROM users WHERE username = %s and password = %s"
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
                "SELECT username FROM users WHERE username=%s", (self.username.get(),)
            )
            self.maneger_frame()
        elif role == Developer:
            print("true")
            self.developer_frame()
            pass
        elif role == Custumer:
            c.execute(
                "SELECT username FROM users WHERE username=%s", (self.username.get(),)
            )
            self.custumer_frame()
        else:
            print("לא מכיר את התפקיד {username} - {role}")
            return

    def forgot_password(self):
        c = self.users_db.cursor(buffered=True)
        find_user = "SELECT * FROM users WHERE username = %s "
        c.execute(find_user, [(self.findName.get())])
        result = c.fetchone()
        if not result:
            ms.showerror("אוי", "שם המשתמש לא קיים")
            return
        update = """UPDATE users set password = %s where username = %s"""
        c.execute(update, [self.resetPass.get(), self.findName.get()])
        self.users_db.commit()
        self.login_frame()

    def new_user(self):
        # Establish Connection
        users_cursor = self.users_db.cursor(buffered=True)

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
        insert_users = "INSERT INTO users(username, password, role) VALUES(%s,%s,%s)"

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
        self.df.pack_forget()
        self.cusf.pack_forget()
        self.mf.pack_forget()
        self.fpf.pack_forget()
        self.head["text"] = "התחברות"
        self.logf.pack()

    def create_acc_frame(self):
        self.n_username.set("")
        self.n_password.set("")
        self.logf.pack_forget()
        self.logf.pack_forget()
        self.head["text"] = "יצירת משתמש"
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
        self.iframe5.pack_forget()
        self.scd.pack_forget()
        self.atf.pack_forget()

        self.head["text"] = "מפתח"

        Button(
            self.df,
            text="פרויקטים",
            bd=3,
            font=("", 15),
            padx=1,
            pady=1,
            command=self.d_project_frame,
        ).grid(row=0, column=0)

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

        Button(self.mf,
               text=" להתנתק ",
               bd=3,
               font=("", 15),
               padx=5,
               pady=5,
               command=self.login_frame,
               ).grid(row=2, column=1)

        self.messages(self.mf, 3)
        self.mf.pack()

    def custumer_frame(self):
        self.logf.pack_forget()
        self.scc.pack_forget()

        self.head["text"] = "לקוח"
        projs = PROJECT_customer.get_proj(self.username.get())

        for p in projs:
            print(p[0])

        Button(self.cusf,
               text=" הכנסת תיאור פרוייקט",
               bd=3,
               font=("", 15),
               padx=5,
               pady=5,
               command=self.enter_discription_fram,
               ).grid(row=4, column=1)
        Button(self.cusf,
               text=" פתח פרויקט",
               bd=3,
               font=("", 15),
               padx=5,
               pady=5,
               command=self.cus_show_proj_frame,
               ).grid(row=1, column=1)

        Button(self.cusf,
               text=" סכימה ",
               bd=3,
               font=("", 15),
               padx=5,
               pady=5,
               command=self.schema_cus,
               ).grid(row=2, column=1)
        Button(self.cusf,
               text=" פנייה למנהל הפרויקט ",
               bd=3,
               font=("", 15),
               padx=5,
               pady=5,
               command=self.message_to_manager,
               ).grid(row=3, column=1)
        Button(self.cusf,
               text=" להתנתק ",
               bd=3,
               font=("", 15),
               padx=5,
               pady=5,
               command=self.login_frame,
               ).grid(row=5, column=1)

        i = 7
        Label(self.cusf, text="*******************", font=("", 20), pady=10, padx=10).grid(row=i, column=0)
        Label(self.cusf, text="*******************", font=("", 20), pady=10, padx=10).grid(row=i, column=1)
        i = i + 1
        Label(self.cusf, text="הפרויקטים שאתה משויך אליהם", font=("", 20), pady=10, padx=10).grid(row=i, column=1)
        i = i + 1
        Label(self.cusf, text="שם הפרויקט", font=("", 20, 'underline'), pady=10, padx=10).grid(row=i, column=0)
        Label(self.cusf, text="מזהה הפרויקט", font=("", 20, 'underline'), pady=10, padx=10).grid(row=i, column=1)
        i = i + 1
        for p in projs:
            t = PROJECT.get_project_by_projId(p[0])
            Label(self.cusf, text="   " + t[1] + "   ", font=("", 20), pady=10, padx=10).grid(row=i, column=0)
            Label(self.cusf, text="   " + t[0] + "    ", font=("", 20), pady=10, padx=10).grid(row=i, column=1)
            i = i + 1

        self.cusf.pack()

    ## tasks for developer page
    def all_teammates_task(self):
        self.df.pack_forget()
        self.head["text"] = "דף משימות"
        projectAssign = PROJECT_CREW.get_project(self.username.get())
        print(projectAssign)
        Label(self.att, text="מס' מזהה-משימות", font=("", 18), pady=10, padx=10).grid(row=0, column=0)
        r = 0
        if projectAssign != None:
            tasks = TASK.get_tasks(projectAssign[0])
            crew = PROJECT_CREW.get_crew(projectAssign[0])
            print(tasks)
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
        else:
            Label(self.att, text="אינך משויך לפרויקט", font=("", 18), pady=10, padx=10).grid(row=r, column=0)
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
        self.dpef.forget()
        self.head["text"] = "סכימת התקדמות"
        ########
        projectAssign = PROJECT_CREW.get_project(self.username.get())
        ylabels = []
        xlabels = []
        if projectAssign != None:
            tasks = TASK.get_tasks(projectAssign[0])
            print(tasks)
            crew = PROJECT_CREW.get_crew(projectAssign[0])
            fig = Figure(figsize=(5, 5),
                         dpi=100)

            # list of squares
            y = [i ** 2 for i in range(101)]

            # adding the subplot
            plot1 = fig.add_subplot(111)

            # plotting the graph
            plot1.plot(y)

            # creating the Tkinter canvas
            # containing the Matplotlib figure
            canvas = FigureCanvasTkAgg(fig,
                                       master=self.iframe5)
            canvas.draw()

            # placing the canvas on the Tkinter window
            canvas.get_tk_widget().pack()

            # creating the Matplotlib toolbar
            toolbar = NavigationToolbar2Tk(canvas,
                                           self.iframe5)
            toolbar.update()

            # placing the toolbar on the Tkinter window
            canvas.get_tk_widget().pack()

            self.iframe5.pack(expand=1, fill=X, pady=10, padx=5)
        Button(
            self.scd,
            text="חזור",
            bd=3,
            font=("", 15),
            padx=1,
            pady=1,
            command=self.developer_frame,
        ).grid(row=10, column=0)
        self.scd.pack()

    def schema_cus(self):
        self.cusf.pack_forget()
        self.cf.pack_forget()
        self.head["text"] = "סכימת התקדמות"
        self.schema(self.scc)

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

    def schema(self, f):
        projectAssign = PROJECT_customer.get_proj(self.username.get())
        print(projectAssign)
        y1 = y2 = x = []
        if projectAssign is not None:
            tasks = TASK.get_tasks(projectAssign[0][0])
            numTasks = len(tasks)
            q = numTasks

            for t in tasks:
                if t[0] == projectAssign[0][0]:
                    if t[4] != 'DEF' and t[4] != 'DEFF':
                        print(t[4])
                        numTasks = numTasks - 1

            x = [projectAssign[0][0]]
            y1 = [numTasks]
            y2 = [q]

        print(x)
        print(y1)
        print(y2)
        c = (numTasks / q) * 100
        print(c)
        fig = plt.figure(figsize=(4, 5))
        plt.bar(['Project'], y1, color='r')
        plt.text(x=0, y=q + 1, s='100%')
        plt.bar(['Project'], y2, bottom=y1)
        plt.text(x=0 - 0.1, y=y2[0] - 1, s="completed:" + str(c) + '%')
        plt.yticks([])
        canvas = FigureCanvasTkAgg(fig, master=self.scc)
        canvas.draw()
        canvas.get_tk_widget().grid(row=1, column=0, ipadx=40, ipady=20)

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

        # Developer Widgets
        self.df = Frame(self.master, padx=20, pady=30)

        # Manager Widgets
        self.mf = Frame(self.master, padx=20, pady=30)

        # Customer Widgets
        self.sst = Frame(self.master, padx=20, pady=30)
        self.cusf = Frame(self.master, padx=20, pady=30)
        self.cct = Frame(self.master, padx=20, pady=30)
        self.pf = Frame(self.master, padx=20, pady=30)  # project frame
        self.apf = Frame(self.master, padx=20, pady=30)  # add project
        self.rpf = Frame(self.master, padx=20, pady=30)  # remove project
        self.tf = Frame(self.master, padx=20, pady=30)  # task frame
        self.tfc = Frame(self.master, padx=20, pady=30)  # task frame custumer
        self.atf = Frame(self.master, padx=20, pady=30)  # add task frame
        self.shtf = Frame(self.master, padx=20, pady=30)  # show task frame
        self.dtef = Frame(self.master, padx=20, pady=30)  # task editor frame

        self.spf = Frame(self.master, padx=20, pady=30)  # show project frame
        self.pef = Frame(self.master, padx=20, pady=30)  # project editor frame
        self.rtf = Frame(self.master, padx=20, pady=30)  # remove task frame
        self.pefc = Frame(self.master, padx=20, pady=30)  # project editor frame for customer
        self.spfc = Frame(self.master, padx=20, pady=30)  # show project frame for customer
        self.cf = Frame(self.master, padx=20, pady=30)  # crew frame
        self.att = Frame(self.master, padx=20, pady=100)  # tasks for project frame
        self.scd = Frame(self.master, padx=20, pady=100)  # developer schema frame
        self.scc = Frame(self.master, padx=20, pady=100)  # customer schema frame
        self.iframe5 = Frame(self.master, bd=2, relief=RAISED)

        self.dpf = Frame(self.master, padx=20, pady=30)  # developer project frame
        self.dspf = Frame(self.master, padx=20, pady=30)  # developer show project frame
        self.dpef = Frame(self.master, padx=20, pady=30)  # developer project editor frame
        self.dtf = Frame(self.master, padx=20, pady=30)  # developer task frame
        self.datf = Frame(self.master, padx=20, pady=30)  # developer add task frame
        self.drtf = Frame(self.master, padx=20, pady=30)  # remove task frame
        self.dtef = Frame(self.master, padx=20, pady=30)  # developer task editor frame
        self.dshtf = Frame(self.master, padx=20, pady=30)  # developer show task frame
        self.det = Frame(self.master, padx=20, pady=30)  # developer edit task frame

        self.drf = Frame(self.master, padx=20, pady=30)  # developer remark  frame

        self.pcf = Frame(self.master, padx=20, pady=30)  # project customer frame
        self.dfc = Frame(self.master, padx=50, pady=50)  # customer show discription frame
        self.cspf = Frame(self.master, padx=20, pady=30)  # customer show project frame
        self.cpef = Frame(self.master, padx=20, pady=30)  # customer project editor frame
        self.cshtf = Frame(self.master, padx=20, pady=30)  # customer show task frame
        self.ctf = Frame(self.master, padx=20, pady=30)  # customer task frame  ( cus_task_fram)
        self.crf = Frame(self.master, padx=20, pady=30)  # customer remark  frame

        self.tasd = Frame(self.master, padx=20, pady=30)
        self.ssfmd = Frame(self.master, padx=20, pady=30)
        self.sf = Frame(self.master, padx=20, pady=30)  # sprints frame
        self.asf = Frame(self.master, padx=20, pady=30)  # add sprint frame
        self.esf = Frame(self.master, padx=20, pady=30)  # edit sprint frame
        self.rsf = Frame(self.master, padx=20, pady=30)  # remove sprint frame
        self.ssf = Frame(self.master, padx=20, pady=30)  # show sprint frame
        self.ssfm = Frame(self.master, padx=20, pady=30)  # show sprint frame main
        self.atts = Frame(self.master, padx=20, pady=30)  # add task to sprint frame
        self.tas = Frame(self.master, padx=20, pady=30)  # add task to sprint frame
        self.dtfs = Frame(self.master, padx=20, pady=30)  # delete task from sprint frame

    #########customer funcs########################

    def cus_show_proj_frame(self):

        self.cusf.forget()

        def back():
            self.cspf.forget()
            self.custumer_frame()

        def chek_proj():
            projs = PROJECT_customer.get_proj(self.username.get())
            x = 0
            for p in projs:
                if p[0] == self.prjNum.get():
                    x = 1
                    self.cus_proj_editor_frame()

            if x == 0:
                ms.showerror("שגיאה", "הפרויקט המבוקש לא נמצא")

        self.head["text"] = "הצגת פרויקט"
        Label(self.cspf, text="מספר מזהה של פרויקט: ", font=("", 20), pady=10, padx=10).grid(
            row=0, column=1
        )
        Entry(self.cspf, textvariable=self.prjNum, bd=5, font=("", 15)).grid(
            row=0, column=0
        )
        Button(
            self.cspf,
            text="הצג",
            bd=3,
            font=("", 15),
            padx=1,
            pady=1,
            command=chek_proj, ).grid(row=2, column=1)

        Button(
            self.cspf,
            text="חזור",
            bd=3,
            font=("", 15),
            padx=1,
            pady=1,
            command=back, ).grid(row=3, column=1)

        self.cspf.pack()

    def cus_proj_editor_frame(self):

        proj = PROJECT.get_project_by_projId(self.prjNum.get())
        if not proj:
            ms.showerror("שגיאה", "הפרויקט המבוקש לא נמצא")
            return

        self.cspf.forget()

        def back():
            self.cpef.forget()
            self.custumer_frame()

        Label(self.cpef, text=":שם הפרויקט ", font=("", 20), pady=10, padx=10).grid(row=1, column=1)
        Label(self.cpef, text=proj[1], font=("", 20), pady=10, padx=10).grid(row=1, column=0)
        Label(self.cpef, text=":מזהה הפרויקט ", font=("", 20), pady=10, padx=10).grid(row=2, column=1)
        Label(self.cpef, text=proj[0], font=("", 20), pady=10, padx=10).grid(row=2, column=0)
        Label(self.cpef, text=":מנהל הפרויקט ", font=("", 20), pady=10, padx=10).grid(row=3, column=1)
        Label(self.cpef, text=proj[2], font=("", 20), pady=10, padx=10).grid(row=3, column=0)

        self.prjName.set(proj[1])
        self.prjNum.set(proj[0])

        Button(self.cpef,
               text=" שהושלמו משימות ",
               bd=3,
               font=("", 15),
               padx=5,
               pady=5,
               command=self.complited_tasks,
               ).grid(row=4, column=1)

        Button(self.cpef,
               text=" סכימה ",
               bd=3,
               font=("", 15),
               padx=5,
               pady=5,
               command=self.schema_cus,
               ).grid(row=5, column=1)

        Button(self.cpef,
               text="פתח משימה ",
               bd=3,
               font=("", 15),
               padx=5,
               pady=5,
               command=self.cus_show_task_frame,
               ).grid(row=5, column=1)

        Button(self.cpef, text="חזור", bd=3, font=("", 15), padx=1, pady=1, command=back, ).grid(row=6, column=1)

        tasks = TASK.get_tasks(self.prjNum.get())
        i = 10

        Label(self.cpef, text="******************", font=("", 20), pady=10, padx=10).grid(row=i, column=0)
        Label(self.cpef, text="******************", font=("", 20), pady=10, padx=10).grid(row=i, column=1)
        Label(self.cpef, text="******************", font=("", 20), pady=10, padx=10).grid(row=i, column=2)
        i = i + 1
        Label(self.cpef, text="משימות הקיימות בפרויקט", font=("", 20), pady=10, padx=10).grid(row=i, column=1)
        i = i + 1
        Label(self.cpef, text="מזהה משימה", font=("", 20, 'underline'), pady=10, padx=10).grid(row=i, column=2)
        Label(self.cpef, text="תאור", font=("", 20, 'underline'), pady=10, padx=10).grid(row=i, column=1)
        Label(self.cpef, text="סטאטוס", font=("", 20, 'underline'), pady=10, padx=10).grid(row=i, column=3)
        i = i + 1
        for t in tasks:
            Label(self.cpef, text="   " + t[1] + "   ", font=("", 20), pady=10, padx=10).grid(row=i, column=2)

            Label(self.cpef, text="   " + t[6] + "   ", font=("", 20), pady=10, padx=10).grid(row=i, column=1)
            Label(self.cpef, text="   " + t[4] + "   ", font=("", 20), pady=10, padx=10).grid(row=i, column=3)
            i = i + 1

        Label(self.cpef, text="     ", font=("", 20), pady=10, padx=10).grid(row=i, column=2)
        Label(self.cpef, text="     ", font=("", 20), pady=10, padx=10).grid(row=i, column=1)

        self.cpef.pack()

    def complited_tasks(self):
        proj = PROJECT.get_project_by_projId(self.prjNum.get())
        if not proj:
            ms.showerror("שגיאה", "הפרויקט המבוקש לא נמצא")
            return

        self.cpef.forget()

        def back():
            self.cct.forget()
            self.custumer_frame()

        self.prjName.set(proj[1])
        self.prjNum.set(proj[0])

        Button(self.cct, text="חזור", bd=3, font=("", 15), padx=1, pady=1, command=back, ).grid(row=6, column=1)

        tasks = TASK.get_tasks(self.prjNum.get())
        i = 10

        Label(self.cct, text="******************", font=("", 20), pady=10, padx=10).grid(row=i, column=0)
        Label(self.cct, text="******************", font=("", 20), pady=10, padx=10).grid(row=i, column=1)
        Label(self.cct, text="******************", font=("", 20), pady=10, padx=10).grid(row=i, column=2)
        i = i + 1
        Label(self.cct, text="משימות הקיימות בפרויקט", font=("", 20), pady=10, padx=10).grid(row=i, column=1)
        i = i + 1
        Label(self.cct, text="מזהה משימה", font=("", 20, 'underline'), pady=10, padx=10).grid(row=i, column=2)
        Label(self.cct, text="תאור", font=("", 20, 'underline'), pady=10, padx=10).grid(row=i, column=1)
        Label(self.cct, text="סטאטוס", font=("", 20, 'underline'), pady=10, padx=10).grid(row=i, column=3)
        i = i + 1
        for t in tasks:
            if t[4] == "DONE":
                Label(self.cct, text="   " + t[1] + "   ", font=("", 20), pady=10, padx=10).grid(row=i, column=2)
                Label(self.cct, text="   " + t[6] + "   ", font=("", 20), pady=10, padx=10).grid(row=i, column=1)
                Label(self.cct, text="   " + t[4] + "   ", font=("", 20), pady=10, padx=10).grid(row=i, column=3)

                i = i + 1

        Label(self.cct, text="     ", font=("", 20), pady=10, padx=10).grid(row=i, column=2)
        Label(self.cct, text="     ", font=("", 20), pady=10, padx=10).grid(row=i, column=1)
        self.cct.pack()

    def enter_discription_fram(self):
        self.head["text"] = "תיאור הפרוייקט"
        self.cshtf.forget()
        self.cusf.forget()

        def back():
            self.dfc.forget()
            self.custumer_frame()

        def add_disc():
            t = DISCRIPTION(self.prjNum.get(), self.discriptuon.get())
            t.insert_to_table()

        self.dfc.forget()

        Button(self.dfc, text="חזור", bd=3, font=("", 15), padx=1, pady=1, command=back, ).grid(row=3, column=0)
        Button(self.dfc, text="הכנס", bd=3, font=("", 15), padx=1, pady=1, command=add_disc, ).grid(row=3, column=1)

        Label(self.dfc, text=":מזהה של פרוייקט ", font=("", 20), pady=10, padx=10).grid(
            row=1, column=1
        )
        Entry(self.dfc, textvariable=self.prjNum, bd=5, font=("", 15)).grid(
            row=1, column=0
        )
        Label(self.dfc, text=":תיאור הפרוייקט ", font=("", 20), pady=40, padx=30).grid(
            row=2, column=1
        )
        Entry(self.dfc, textvariable=self.discriptuon, bd=10, font=("", 20), width="80").grid(
            row=2, column=0
        )
        self.dfc.pack()

    def cus_show_task_frame(self):
        self.head["text"] = "משימות הפרויקט"

        def back():
            self.dshtf.forget()
            self.cus_proj_editor_frame()

        self.cpef.forget()

        Button(self.cshtf, text="חזור", bd=3, font=("", 15), padx=1, pady=1, command=back, ).grid(row=3, column=0)

        Label(self.cshtf, text=":מזהה של משימה ", font=("", 20), pady=10, padx=10).grid(
            row=1, column=1
        )
        Entry(self.cshtf, textvariable=self.taskId, bd=5, font=("", 15)).grid(
            row=1, column=0
        )

        Button(
            self.cshtf,
            text="הצג",
            bd=3,
            font=("", 15),
            padx=1,
            pady=1,
            command=self.cus_task_frame,
        ).grid(row=2, column=0)

        self.cshtf.pack()

    def cus_task_frame(self):
        t = TASK.get_task(self.taskId.get(), self.prjNum.get())
        if not t:
            ms.showerror("error", "המשימה המבוקשת לא נמצאת")
            return

        def back():
            self.ctf.forget()
            self.dev_task_frame()

        self.time.set(t[2])
        self.crew.set(t[3])
        self.status.set(t[4])
        self.priorty.set(t[5])
        self.description.set(t[6])
        self.cshtf.forget()

        Label(self.ctf, text=":מזהה משימה ", font=("", 20), pady=10, padx=10).grid(
            row=0, column=1
        )
        Label(self.ctf, text=self.taskId.get(), font=("", 20), pady=10, padx=10).grid(
            row=0, column=0
        )
        Label(self.ctf, text=":מספר שעות מוערך להשלמת משימה ", font=("", 20), pady=10, padx=10).grid(
            row=1, column=1
        )
        Label(self.ctf, text=self.time.get(), font=("", 20), pady=10, padx=10).grid(
            row=1, column=0
        )
        Label(self.ctf, text=":כמות אנשי צוות דרוש ", font=("", 20), pady=10, padx=10).grid(
            row=2, column=1
        )
        Label(self.ctf, text=self.crew.get(), font=("", 20), pady=10, padx=10).grid(
            row=2, column=0
        )
        Label(self.ctf, text=" :סטאטוס", font=("", 20), pady=10, padx=10).grid(
            row=3, column=1
        )
        Label(self.ctf, text=self.status.get(), font=("", 20), pady=10, padx=10).grid(
            row=3, column=0
        )
        Label(self.ctf, text=" :סטאטוס", font=("", 20), pady=10, padx=10).grid(
            row=3, column=1
        )
        Label(self.ctf, text=self.status.get(), font=("", 20), pady=10, padx=10).grid(
            row=3, column=0
        )
        Label(self.ctf, text=" :עדיפות", font=("", 20), pady=10, padx=10).grid(
            row=4, column=1
        )
        Label(self.ctf, text=self.priorty.get(), font=("", 20), pady=10, padx=10).grid(
            row=4, column=0
        )

        Label(self.ctf, text=" :תיאור", font=("", 20), pady=10, padx=10).grid(
            row=5, column=1
        )
        Label(self.ctf, text=self.description.get(), font=("", 20), pady=10, padx=10).grid(
            row=5, column=0
        )

        Button(self.ctf, text="הערות", bd=3, font=("", 15), padx=1, pady=1, command=self.cus_remark_frame, ).grid(
            row=6,
            column=1)

        Button(self.ctf, text="חזור", bd=3, font=("", 15), padx=1, pady=1, command=back, ).grid(
            row=7,
            column=1)

        self.ctf.pack()

    def cus_remark_frame(self):
        self.ctf.forget()

        def back():
            self.crf.forget()
            self.cus_show_task_frame()

        def drow_list(i):
            remarks = REMARK.get_task_remarks(self.prjNum.get(), self.taskId.get())
            Label(self.crf, text="************* ", font=("", 20), pady=10, padx=10).grid(row=i, column=1)
            Label(self.crf, text="************* ", font=("", 20), pady=10, padx=10).grid(row=i, column=0)
            Label(self.crf, text="************* ", font=("", 20), pady=10, padx=10).grid(row=i, column=2)
            i = i + 1
            Label(self.crf, text="הערות קיימות", font=("", 20), pady=10, padx=10).grid(row=i, column=2)
            i = i + 1
            Label(self.crf, text="כותרת", font=("", 20, 'underline'), pady=10, padx=10).grid(row=i, column=2)
            Label(self.crf, text="מאת", font=("", 20, 'underline'), pady=10, padx=10).grid(row=i, column=1)
            Label(self.crf, text="הערה", font=("", 20, 'underline'), pady=10, padx=10).grid(row=i, column=0)
            i = i + 1
            for r in remarks:
                Label(self.crf, text="   " + r[2] + "   ", font=("", 20), pady=10, padx=10).grid(row=i, column=2)
                Label(self.crf, text="   " + r[3] + "   ", font=("", 20), pady=10, padx=10).grid(row=i, column=1)
                Label(self.crf, text="   " + r[4] + "   ", font=("", 20), pady=10, padx=10).grid(row=i, column=0)
                i = i + 1

            Label(self.crf, text="     ", font=("", 20), pady=10, padx=10).grid(row=i, column=2)
            Label(self.crf, text="     ", font=("", 20), pady=10, padx=10).grid(row=i, column=1)
            Label(self.crf, text="     ", font=("", 20), pady=10, padx=10).grid(row=i, column=0)
            self.crf.pack()

        def add():
            REMARK.new_remark(self.prjNum.get(), self.taskId.get(), self.title.get(), self.username.get(),
                              self.remark.get())
            drow_list(7)

        def remove():
            REMARK.remove_remark(self.prjNum.get(), self.taskId.get(), self.title.get())
            drow_list(7)

        self.head["text"] = self.taskId.get() + " הערות על משימה "
        Label(self.crf, text="כותרת", font=("", 20), pady=10, padx=10).grid(row=1, column=1)
        Entry(self.crf, textvariable=self.title, bd=5, font=("", 15)).grid(row=1, column=0)
        Label(self.crf, text="הערה", font=("", 20), pady=10, padx=10).grid(row=2, column=1)
        Entry(self.crf, textvariable=self.remark, bd=5, font=("", 15)).grid(row=2, column=0)
        Button(self.crf, text="הוסף הערה", bd=3, font=("", 15), padx=1, pady=1, command=add, ).grid(row=3, column=1)

        Button(self.crf, text="מחק הערה (רשום כותרת הערה)", bd=3, font=("", 15), padx=1, pady=1, command=remove, ).grid(
            row=4, column=1)
        Entry(self.crf, textvariable=self.title, bd=5, font=("", 15)).grid(
            row=4, column=0
        )

        Button(self.crf, text="חזור", bd=3, font=("", 15), padx=1, pady=1, command=back, ).grid(row=5, column=1)

        drow_list(7)
        self.crf.pack()

    #########end of customer funcs########################

    ###############developer funcs########################
    def d_project_frame(self):
        my_p = PROJECT_CREW.get_developer_projects(self.username.get())

        self.df.forget()
        self.head["text"] = "פרויקטים"

        def back():
            self.dpf.forget()
            self.developer_frame()

        Button(
            self.dpf,
            text="חזור",
            bd=3,
            font=("", 15),
            padx=1,
            pady=1,
            command=back, ).grid(row=0, column=1)

        Button(
            self.dpf,
            text="הצג פרויקט",
            bd=3,
            font=("", 15),
            padx=1,
            pady=1,
            command=self.dev_show_proj_frame, ).grid(row=1, column=1)

        i = 5
        Label(self.dpf, text="*****************", font=("", 20), pady=10, padx=10).grid(row=i, column=0)
        Label(self.dpf, text="*****************", font=("", 20), pady=10, padx=10).grid(row=i, column=1)
        i = i + 1
        Label(self.dpf, text="הפרויקטים אליהם אתה משוייך", font=("", 20), pady=10, padx=10).grid(row=i, column=1)
        i = i + 1

        Label(self.dpf, text="שם הפרויקט", font=("", 20, 'underline'), pady=10, padx=10).grid(row=i, column=0)
        Label(self.dpf, text="מזהה הפרויקט", font=("", 20, 'underline'), pady=10, padx=10).grid(row=i, column=1)
        i = i + 1
        for p in my_p:
            proj = PROJECT.get_project_by_projId(p[0])
            Label(self.dpf, text="   " + proj[1] + "   ", font=("", 20), pady=10, padx=10).grid(row=i, column=0)
            Label(self.dpf, text="   " + proj[0] + "    ", font=("", 20), pady=10, padx=10).grid(row=i, column=1)
            i = i + 1

        self.dpf.pack()

    def dev_show_proj_frame(self):
        def back():
            self.dspf.forget()
            self.d_project_frame()

        def chek_proj():
            projs = PROJECT_CREW.get_developer_projects(self.username.get())
            x = 0
            for p in projs:
                if p[0] == self.prjNum.get():
                    x = 1
                    self.dev_proj_editor_frame()

            if x == 0:
                ms.showerror("שגיאה", "הפרויקט המבוקש לא נמצא")

        self.dpf.forget()
        self.head["text"] = "הצגת פרויקט"
        Label(self.dspf, text="מספר מזהה של פרויקט: ", font=("", 20), pady=10, padx=10).grid(
            row=0, column=1
        )
        Entry(self.dspf, textvariable=self.prjNum, bd=5, font=("", 15)).grid(
            row=0, column=0
        )
        Button(
            self.dspf,
            text="הצג",
            bd=3,
            font=("", 15),
            padx=1,
            pady=1,
            command=chek_proj, ).grid(row=2, column=1)

        Button(
            self.dspf,
            text="חזור",
            bd=3,
            font=("", 15),
            padx=1,
            pady=1,
            command=back, ).grid(row=3, column=1)

        self.dspf.pack()

    def dev_proj_editor_frame(self):
        proj = PROJECT.get_project_by_projId(self.prjNum.get())
        if not proj:
            ms.showerror("שגיאה", "הפרויקט המבוקש לא נמצא")
            return
        self.scd.forget()
        self.dspf.forget()

        def back():
            self.dpef.forget()
            self.d_project_frame()

        Button(self.dpef,
               text=" משימות של ספרינט פעיל ",
               bd=3,
               font=("", 15),
               padx=5,
               pady=5,
               command=self.show_sprint_frame_dev,
               ).grid(row=8, column=1)
        Label(self.dpef, text=":שם הפרויקט ", font=("", 20), pady=10, padx=10).grid(row=1, column=1)
        Label(self.dpef, text=proj[1], font=("", 20), pady=10, padx=10).grid(row=1, column=0)
        Label(self.dpef, text=":מזהה הפרויקט ", font=("", 20), pady=10, padx=10).grid(row=2, column=1)
        Label(self.dpef, text=proj[0], font=("", 20), pady=10, padx=10).grid(row=2, column=0)
        Label(self.dpef, text=":מנהל הפרויקט ", font=("", 20), pady=10, padx=10).grid(row=3, column=1)
        Label(self.dpef, text=proj[2], font=("", 20), pady=10, padx=10).grid(row=3, column=0)

        Button(self.dpef,
               text=" סכימה ",
               bd=3,
               font=("", 15),
               padx=5,
               pady=5,
               command=self.schema_dev,
               ).grid(row=4, column=1)

        Button(self.dpef, text="משימות", bd=3, font=("", 15), padx=1, pady=1, command=self.dev_task_frame, ).grid(row=5,
                                                                                                                  column=1)
        self.prjName.set(proj[1])
        self.prjNum.set(proj[0])

        Button(self.dpef, text="חזור", bd=3, font=("", 15), padx=1, pady=1, command=back, ).grid(row=6, column=1)

        self.dpef.pack()

    def dev_task_frame(self):
        self.dpef.forget()

        tasks = TASK.get_tasks(self.prjNum.get())

        def back():
            self.dtf.forget()
            self.dev_proj_editor_frame()

        self.head["text"] = "ניהול משימות"
        Label(self.dtf, text=":משימות של הפרויקט ", font=("", 20), pady=10, padx=10).grid(row=0, column=1)
        Label(self.dtf, text=self.prjName.get(), font=("", 20), pady=10, padx=10).grid(row=0, column=0)

        Button(self.dtf, text="חזור", bd=3, font=("", 15), padx=1, pady=1, command=back, ).grid(row=1, column=1)
        Button(self.dtf, text="הוסף משימה", bd=3, font=("", 15), padx=1, pady=1,
               command=self.dev_add_task_frame, ).grid(
            row=2, column=1)
        Button(self.dtf, text="הצג משימה", bd=3, font=("", 15), padx=1, pady=1,
               command=self.dev_show_task_frame, ).grid(
            row=3, column=1)
        Button(self.dtf, text="ערוך משימה", bd=3, font=("", 15), padx=1, pady=1,
               command=self.dev_show_task_frame, ).grid(
            row=4, column=1)
        Button(self.dtf, text="מחק משימה", bd=3, font=("", 15), padx=1, pady=1,
               command=self.dev_remove_task_frame, ).grid(
            row=5, column=1)

        Label(self.dtf, text="******************", font=("", 20), pady=10, padx=10).grid(row=7, column=0)
        Label(self.dtf, text="******************", font=("", 20), pady=10, padx=10).grid(row=7, column=1)
        Label(self.dtf, text="******************", font=("", 20), pady=10, padx=10).grid(row=7, column=2)
        Label(self.dtf, text="משימות הקיימות בפרויקט", font=("", 20), pady=10, padx=10).grid(row=8, column=1)

        Label(self.dtf, text="מזהה משימה", font=("", 20, 'underline'), pady=10, padx=10).grid(row=9, column=2)
        Label(self.dtf, text="תאור", font=("", 20, 'underline'), pady=10, padx=10).grid(row=9, column=1)

        i = 10
        for t in tasks:
            Label(self.dtf, text="   " + t[1] + "   ", font=("", 20), pady=10, padx=10).grid(row=i, column=2)
            Label(self.dtf, text="   " + t[6] + "   ", font=("", 20), pady=10, padx=10).grid(row=i, column=1)
            i = i + 1

        Label(self.dtf, text="     ", font=("", 20), pady=10, padx=10).grid(row=i, column=2)
        Label(self.dtf, text="     ", font=("", 20), pady=10, padx=10).grid(row=i, column=1)

        i = i + 1

        Label(self.dtf, text="     ", font=("", 20), pady=10, padx=10).grid(row=i, column=1)
        Label(self.dtf, text="     ", font=("", 20), pady=10, padx=10).grid(row=i, column=0)

        self.dtf.pack()

    def dev_add_task_frame(self):
        self.dpef.forget()

        def back():
            self.datf.forget()
            self.dev_task_frame()

        def add_task():
            t = TASK(self.taskId.get(), self.time.get(), self.crew.get(), self.prjNum.get(), self.status.get(),
                     self.priorty.get(), self.description.get())
            t.insert_to_table()

        Button(self.datf, text="חזור", bd=3, font=("", 15), padx=1, pady=1, command=back, ).grid(row=0, column=1)
        Label(self.datf, text=":מזהה של משימה ", font=("", 20), pady=10, padx=10).grid(row=1, column=1)
        Entry(self.datf, textvariable=self.taskId, bd=5, font=("", 15)).grid(row=1, column=0)
        Label(self.datf, text=":מספר שעות מוערך להשלמת משימה ", font=("", 20), pady=10, padx=10).grid(row=2, column=1)
        Entry(self.datf, textvariable=self.time, bd=5, font=("", 15)).grid(row=2, column=0)
        Label(self.datf, text=":מספר צוות דרוש ", font=("", 20), pady=10, padx=10).grid(row=3, column=1)
        Entry(self.datf, textvariable=self.crew, bd=5, font=("", 15)).grid(row=3, column=0)
        Label(self.datf, text=":סטאטוס (IN PROGRES/DONE/DEF) ", font=("", 20), pady=10, padx=10).grid(row=4, column=1)
        Entry(self.datf, textvariable=self.status, bd=5, font=("", 15)).grid(row=4, column=0)
        Label(self.datf, text=":עדיפות H/L/M ", font=("", 20), pady=10, padx=10).grid(row=5, column=1)
        Entry(self.datf, textvariable=self.priorty, bd=5, font=("", 15)).grid(row=5, column=0)
        Label(self.datf, text=":תיאור המשימה ", font=("", 20), pady=10, padx=10).grid(row=6, column=1)
        Entry(self.datf, textvariable=self.description, bd=5, font=("", 15)).grid(row=6, column=0)
        Button(
            self.datf,
            text="הוסף",
            bd=3,
            font=("", 15),
            padx=1,
            pady=1,
            command=add_task,
        ).grid(row=7, column=0)

        self.head["text"] = "הוספת משימה"
        self.datf.pack()

    def dev_remove_task_frame(self):
        self.dpef.forget()

        def back():
            self.drtf.forget()
            self.dev_task_frame()

        def remove():
            TASK.delet_task(self.prjNum.get(), self.taskId.get())

        Button(self.drtf, text="חזור", bd=3, font=("", 15), padx=1, pady=1, command=back, ).grid(row=3, column=0)

        Label(self.drtf, text=":מזהה של משימה ", font=("", 20), pady=10, padx=10).grid(
            row=1, column=1
        )
        Entry(self.drtf, textvariable=self.taskId, bd=5, font=("", 15)).grid(
            row=1, column=0
        )

        Button(
            self.drtf,
            text="מחק",
            bd=3,
            font=("", 15),
            padx=1,
            pady=1,
            command=remove,
        ).grid(row=2, column=0)

        self.drtf.pack()

    def dev_show_task_frame(self):
        def back():
            self.dshtf.forget()
            self.dev_task_frame()

        self.dtf.forget()

        Button(self.dshtf, text="חזור", bd=3, font=("", 15), padx=1, pady=1, command=back, ).grid(row=3, column=0)

        Label(self.dshtf, text=":מזהה של משימה ", font=("", 20), pady=10, padx=10).grid(
            row=1, column=1
        )
        Entry(self.dshtf, textvariable=self.taskId, bd=5, font=("", 15)).grid(
            row=1, column=0
        )

        Button(
            self.dshtf,
            text="הצג",
            bd=3,
            font=("", 15),
            padx=1,
            pady=1,
            command=self.dev_task_editor_frame,
        ).grid(row=2, column=0)

        self.dshtf.pack()

    def dev_task_editor_frame(self):
        t = TASK.get_task(self.taskId.get(), self.prjNum.get())
        if not t:
            ms.showerror("error", "המשימה המבוקשת לא נמצאת")
            return

        def back():
            self.dtef.forget()
            self.dev_task_frame()

        def message_crew():
            crew = PROJECT_CREW.get_crew(self.prjNum.get())
            msg = "בפרויקט מספר "
            msg += self.prjNum.get()
            msg += "יש שינוי במשימה "
            msg += self.taskId.get()

            for c in crew:
                MESSAGE.new_message(self.username.get(), c[1], msg)
            MESSAGE.printAll()

        def change_h():
            TASK.update_hour(self.prjNum.get(), self.taskId.get(), self.time.get())
            Label(self.dtef, text=self.time.get(), font=("", 20), pady=10, padx=10).grid(
                row=1, column=0
            )
            message_crew()

        def change_c():
            TASK.update_crew(self.prjNum.get(), self.taskId.get(), self.crew.get())
            Label(self.dtef, text=self.crew.get(), font=("", 20), pady=10, padx=10).grid(
                row=2, column=0
            )
            message_crew()

        def change_s():
            TASK.update_status(self.prjNum.get(), self.taskId.get(), self.status.get())
            Label(self.dtef, text=self.status.get(), font=("", 20), pady=10, padx=10).grid(
                row=3, column=0
            )
            message_crew()

        def change_d():
            TASK.update_description(self.prjNum.get(), self.taskId.get(), self.description.get())
            Label(self.dtef, text=self.description.get(), font=("", 20), pady=10, padx=10).grid(
                row=5, column=0
            )
            message_crew()

        self.time.set(t[2])
        self.crew.set(t[3])
        self.status.set(t[4])
        self.priorty.set(t[5])
        self.description.set(t[6])
        self.dshtf.forget()

        Label(self.dtef, text=":מזהה משימה ", font=("", 20), pady=10, padx=10).grid(
            row=0, column=1
        )
        Label(self.dtef, text=self.taskId.get(), font=("", 20), pady=10, padx=10).grid(
            row=0, column=0
        )
        Label(self.dtef, text=":מספר שעות מוערך להשלמת משימה ", font=("", 20), pady=10, padx=10).grid(
            row=1, column=1
        )
        Label(self.dtef, text=self.time.get(), font=("", 20), pady=10, padx=10).grid(
            row=1, column=0
        )
        Label(self.dtef, text=":כמות אנשי צוות דרוש ", font=("", 20), pady=10, padx=10).grid(
            row=2, column=1
        )
        Label(self.dtef, text=self.crew.get(), font=("", 20), pady=10, padx=10).grid(
            row=2, column=0
        )
        Label(self.dtef, text=" :סטאטוס", font=("", 20), pady=10, padx=10).grid(
            row=3, column=1
        )
        Label(self.dtef, text=self.status.get(), font=("", 20), pady=10, padx=10).grid(
            row=3, column=0
        )
        Label(self.dtef, text=" :סטאטוס", font=("", 20), pady=10, padx=10).grid(
            row=3, column=1
        )
        Label(self.dtef, text=self.status.get(), font=("", 20), pady=10, padx=10).grid(
            row=3, column=0
        )
        Label(self.dtef, text=" :עדיפות", font=("", 20), pady=10, padx=10).grid(
            row=4, column=1
        )
        Label(self.dtef, text=self.priorty.get(), font=("", 20), pady=10, padx=10).grid(
            row=4, column=0
        )

        Label(self.dtef, text=" :תיאור", font=("", 20), pady=10, padx=10).grid(
            row=5, column=1
        )
        Label(self.dtef, text=self.description.get(), font=("", 20), pady=10, padx=10).grid(
            row=5, column=0
        )

        Button(self.dtef, text="הערות", bd=3, font=("", 15), padx=1, pady=1, command=self.dev_remark_frame, ).grid(
            row=6,
            column=1)

        Entry(self.dtef, textvariable=self.time, bd=5, font=("", 15)).grid(row=7, column=0)
        Button(self.dtef, text="שנה מספר שעות ", bd=3, font=("", 15), padx=1, pady=1, command=change_h, ).grid(row=7,
                                                                                                               column=1)

        Entry(self.dtef, textvariable=self.crew, bd=5, font=("", 15)).grid(row=8, column=0)
        Button(self.dtef, text="שנה כמות צוות", bd=3, font=("", 15), padx=1, pady=1, command=change_c, ).grid(row=8,
                                                                                                              column=1)

        Entry(self.dtef, textvariable=self.crew, bd=5, font=("", 15)).grid(row=9, column=0)
        Button(self.dtef, text="שנה סטאטוס", bd=3, font=("", 15), padx=1, pady=1, command=change_s, ).grid(row=9,
                                                                                                           column=1)

        Entry(self.dtef, textvariable=self.description, bd=5, font=("", 15)).grid(row=10, column=0)
        Button(self.dtef, text="שנה תיאור", bd=3, font=("", 15), padx=1, pady=1, command=change_d, ).grid(row=10,
                                                                                                          column=1)

        Button(self.dtef, text="חזור", bd=3, font=("", 15), padx=1, pady=1, command=back, ).grid(row=11, column=0)

        self.dtef.pack()

    def dev_remark_frame(self):
        self.dtef.forget()

        def back():
            self.drf.forget()
            self.dev_task_editor_frame()

        def drow_list(i):
            remarks = REMARK.get_task_remarks(self.prjNum.get(), self.taskId.get())
            Label(self.drf, text="************* ", font=("", 20), pady=10, padx=10).grid(row=i, column=1)
            Label(self.drf, text="************* ", font=("", 20), pady=10, padx=10).grid(row=i, column=0)
            Label(self.drf, text="************* ", font=("", 20), pady=10, padx=10).grid(row=i, column=2)
            i = i + 1
            Label(self.drf, text="הערות קיימות", font=("", 20), pady=10, padx=10).grid(row=i, column=2)
            i = i + 1
            Label(self.drf, text="כותרת", font=("", 20, 'underline'), pady=10, padx=10).grid(row=i, column=2)
            Label(self.drf, text="מאת", font=("", 20, 'underline'), pady=10, padx=10).grid(row=i, column=1)
            Label(self.drf, text="הערה", font=("", 20, 'underline'), pady=10, padx=10).grid(row=i, column=0)
            i = i + 1
            for r in remarks:
                Label(self.drf, text="   " + r[2] + "   ", font=("", 20), pady=10, padx=10).grid(row=i, column=2)
                Label(self.drf, text="   " + r[3] + "   ", font=("", 20), pady=10, padx=10).grid(row=i, column=1)
                Label(self.drf, text="   " + r[4] + "   ", font=("", 20), pady=10, padx=10).grid(row=i, column=0)
                i = i + 1

            Label(self.drf, text="     ", font=("", 20), pady=10, padx=10).grid(row=i, column=2)
            Label(self.drf, text="     ", font=("", 20), pady=10, padx=10).grid(row=i, column=1)
            Label(self.drf, text="     ", font=("", 20), pady=10, padx=10).grid(row=i, column=0)
            self.drf.pack()

        def add():
            REMARK.new_remark(self.prjNum.get(), self.taskId.get(), self.title.get(), self.username.get(),
                              self.remark.get())
            drow_list(7)

        def remove():
            REMARK.remove_remark(self.prjNum.get(), self.taskId.get(), self.title.get())
            drow_list(7)

        self.head["text"] = self.taskId.get() + " הערות על משימה "
        Label(self.drf, text="כותרת", font=("", 20), pady=10, padx=10).grid(row=1, column=1)
        Entry(self.drf, textvariable=self.title, bd=5, font=("", 15)).grid(row=1, column=0)
        Label(self.drf, text="הערה", font=("", 20), pady=10, padx=10).grid(row=2, column=1)
        Entry(self.drf, textvariable=self.remark, bd=5, font=("", 15)).grid(row=2, column=0)
        Button(self.drf, text="הוסף הערה", bd=3, font=("", 15), padx=1, pady=1, command=add, ).grid(row=3, column=1)

        Button(self.drf, text="מחק הערה (רשום כותרת הערה)", bd=3, font=("", 15), padx=1, pady=1, command=remove, ).grid(
            row=4, column=1)
        Entry(self.drf, textvariable=self.title, bd=5, font=("", 15)).grid(
            row=4, column=0
        )

        Button(self.drf, text="חזור", bd=3, font=("", 15), padx=1, pady=1, command=back, ).grid(row=5, column=1)

        drow_list(7)
        self.drf.pack()

    ###############end developer funcs########################

    ##################project editor functions##############################

    def project_frame(self):
        self.mf.forget()
        projects = PROJECT.get_projects(self.username.get())

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
            text="הצג פרויקט",
            bd=3,
            font=("", 15),
            padx=1,
            pady=1,
            command=self.show_proj_frame, ).grid(row=3, column=1)

        Label(self.pf, text="*******************", font=("", 20), pady=10, padx=10).grid(row=4, column=0)
        Label(self.pf, text="*******************", font=("", 20), pady=10, padx=10).grid(row=4, column=1)
        Label(self.pf, text="הפרויקטים שלך", font=("", 20), pady=10, padx=10).grid(row=5, column=1)
        Label(self.pf, text="שם הפרויקט", font=("", 20, 'underline'), pady=10, padx=10).grid(row=6, column=0)
        Label(self.pf, text="מזהה הפרויקט", font=("", 20, 'underline'), pady=10, padx=10).grid(row=6, column=1)
        i = 7
        for p in projects:
            Label(self.pf, text="   " + p[1] + "   ", font=("", 20), pady=10, padx=10).grid(row=i, column=0)
            Label(self.pf, text="   " + p[0] + "    ", font=("", 20), pady=10, padx=10).grid(row=i, column=1)
            i = i + 1

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
            text="",
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

    def show_proj_frame_c(self):
        def back():
            self.spfc.forget()
            self.custumer_frame()

        self.pf.forget()
        self.head["text"] = " הצגת פרויקט ללקוח"
        Label(self.spfc, text="מספר מזהה של פרויקט: ", font=("", 20), pady=10, padx=10).grid(
            row=0, column=1
        )
        Entry(self.spfc, textvariable=self.prjNum, bd=5, font=("", 15)).grid(
            row=0, column=0
        )
        Label(self.spfc, text=" מזהה של פרויקט שם: ", font=("", 20), pady=10, padx=10).grid(
            row=0, column=2
        )
        Entry(self.spfc, textvariable=self.prjName, bd=5, font=("", 15)).grid(
            row=0, column=3
        )
        Button(
            self.spfc,
            text="הצג",
            bd=3,
            font=("", 15),
            padx=1,
            pady=1,
            command=self.proj_editor_frame_c, ).grid(row=2, column=1)

        Button(
            self.spfc,
            text="חזור",
            bd=3,
            font=("", 15),
            padx=1,
            pady=1,
            command=back, ).grid(row=3, column=1)

        self.spfc.pack()

    def proj_editor_frame(self):
        self.sf.forget()
        proj = PROJECT.get_project(self.username.get(), self.prjNum.get())
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
        Button(self.pef, text="משימות", bd=3, font=("", 15), padx=1, pady=1, command=self.task_frame, ).grid(row=3,
                                                                                                             column=1)
        self.prjName.set(proj[1])
        Button(self.pef, text="צוות", bd=3, font=("", 15), padx=1, pady=1, command=self.crew_frame, ).grid(row=4,
                                                                                                           column=1)

        Button(self.pef, text="שייך לקוחות לפרויקט", bd=3, font=("", 15), padx=1, pady=1,
               command=self.proj_cust_frame, ).grid(row=5, column=1)

        Button(self.pef, text="ספרינטים", bd=3, font=("", 15), padx=1, pady=1, command=self.sprints_frame, ).grid(
            row=6,
            column=1)
        Button(self.pef, text="חזור", bd=3, font=("", 15), padx=1, pady=1, command=back, ).grid(row=7, column=1)

        self.pef.pack()

    def proj_cust_frame(self):
        self.pef.forget()
        self.head["text"] = "שיוןך לקוח לפרויקט"

        def back():
            self.pcf.forget()
            self.proj_editor_frame()

        def add():
            PROJECT_customer.add_cust(self.prjNum.get(), self.cust_username.get())

        Label(self.pcf, text=":שם משתמש של לקוח ", font=("", 20), pady=10, padx=10).grid(row=0, column=0)

        Entry(self.pcf, textvariable=self.cust_username, bd=5, font=("", 15)).grid(row=0, column=1)

        Button(self.pcf, text="הוסף", bd=3, font=("", 15), padx=1, pady=1, command=add, ).grid(row=2, column=0)
        Button(self.pcf, text="חזור", bd=3, font=("", 15), padx=1, pady=1, command=back, ).grid(row=3, column=0)

        self.pcf.pack()

    def proj_editor_frame_c(self):
        proj = PROJECT.get_project_c(self.prjName.get(), self.prjNum.get())
        if not proj:
            ms.showerror("שגיאה", "הפרויקט המבוקש לא נמצא")
            return

        self.spfc.forget()

        def back():
            self.pefc.forget()
            self.custumer_frame()

        Label(self.pefc, text=":שם הפרויקט ", font=("", 20), pady=10, padx=10).grid(row=1, column=1)
        Label(self.pefc, text=proj[1], font=("", 20), pady=10, padx=10).grid(row=1, column=0)
        Label(self.pefc, text=":מזהה הפרויקט ", font=("", 20), pady=10, padx=10).grid(row=2, column=1)
        Label(self.pefc, text=proj[0], font=("", 20), pady=10, padx=10).grid(row=2, column=0)
        Button(self.pefc, text="משימות", bd=3, font=("", 15), padx=1, pady=1, command=self.task_frame_c, ).grid(row=3,
                                                                                                                column=1)
        self.prjName.set(proj[1])
        Button(self.pefc, text="חזור", bd=3, font=("", 15), padx=1, pady=1, command=back, ).grid(row=5, column=1)
        self.pefc.pack()

    def complete_task(self, projid):
        connect = users
        cc = connect.cursor(buffered=True)

        sql = """SELECT * 
            FROM project_tasks 
            where projId=%s  AND status="DONE"       

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

    def crew_frame(self):
        self.pef.forget()

        def back():
            self.cf.forget()
            self.proj_editor_frame()

        def my_crew():
            j = 6
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
            c = self.users_db.cursor(buffered=True)
            sql = "SELECT * FROM users WHERE role = 'developer' AND username=%s "
            tp = (self.user_crew.get(),)
            try:
                c.execute(sql, tp)


            except:
                ms.showerror("שגיאה", "משתמש לא נמצא")
                return

            PROJECT_CREW.insert_to_table(self.prjNum.get(), self.user_crew.get())

            msg = "שוייכת לפרויקט מספר "
            msg += self.prjNum.get()

            MESSAGE.new_message(self.username.get(), self.user_crew.get(), msg)
            MESSAGE.printAll()
            my_crew()

        c = self.users_db.cursor(buffered=True)
        # Find user If there is any take proper action
        sql = "SELECT * FROM users WHERE role = 'developer' "
        try:
            c.execute(sql)
            users = c.fetchall()

        except:
            ms.showerror("שגיאה", "ניסיון של שליפת משתמשים נכשל")

        Button(
            self.cf,
            text="חזור",
            bd=3,
            font=("", 15),
            padx=1,
            pady=1,
            command=back,
        ).grid(row=2, column=2)

        Button(self.cf, text="הוסף לצוות שלי", bd=3, font=("", 15), padx=1, pady=1, command=add_crew_member, ).grid(
            row=3, column=0)

        Label(self.cf, text=":שם משתמש ", font=("", 20), pady=10, padx=10).grid(
            row=3, column=2
        )
        Entry(self.cf, textvariable=self.user_crew, bd=5, font=("", 15)).grid(
            row=3, column=1
        )

        Label(self.cf, text="*******************", font=("", 20), pady=10, padx=10).grid(row=4, column=0)
        Label(self.cf, text="עובדים קיימים", font=("", 20, 'underline'), pady=10, padx=10).grid(row=5, column=0)
        i = 6
        for u in users:
            Label(self.cf, text="   " + u[0] + "   ", font=("", 20), pady=10, padx=10).grid(row=i, column=0)

            i = i + 1

        Label(self.cf, text="            ", font=("", 20), pady=10, padx=10).grid(row=i, column=0)

        i = i + 1

        Label(self.cf, text="           ", font=("", 20), pady=10, padx=10).grid(row=i, column=0)
        i = i + 1

        my_crew()

        self.cf.pack()

    def remov_proj_frame(self):
        self.pf.forget()

        def chekUser():

            pu = PROJECT.projectManager(self.prjNum.get())

            return self.username.get() == pu

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
            newp = PROJECT(self.prjNum.get(), self.prjName.get(), self.username.get(),self.date.get())
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
        Label(self.apf, text=",תאריך סיום פרויקט: ", font=("", 20), pady=10, padx=10).grid(row=2, column=0)
        Entry(self.apf, textvariable=self.date, bd=5, font=("", 15)).grid(row=2, column=1)

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
    ####### Sprints editor #######
    def sprints_frame(self):
        self.apf.forget()
        self.pef.forget()
        self.pf.forget()
        self.asf.forget()
        self.ssf.forget()
        self.rsf.forget()
        self.esf.forget()
        self.ssfm.forget()
        self.head["text"] = "ספרינטים"
        Button(
            self.sf,
            text="הוסף ספרינט",
            bd=3,
            font=("", 15),
            padx=1,
            pady=1,
            command=self.add_sprint_frame,
        ).grid(row=0, column=0)
        Button(
            self.sf,
            text="מחק ספרינט",
            bd=3,
            font=("", 15),
            padx=1,
            pady=1,
            command=self.remove_sprint_frame,
        ).grid(row=1, column=0)
        Button(
            self.sf,
            text="הצג ספרינט",
            bd=3,
            font=("", 15),
            padx=1,
            pady=1,
            command=self.show_sprint_frame,
        ).grid(row=2, column=0)

        sprints = SPRINT(self.sprintNum.get(),
                         self.prjNum.get(), self.sprintTime.get(), self.sprintStatus.get())
        s = sprints.get_sprints(self.prjNum.get())

        Label(self.sf, text="מספר ספרינט", font=("", 20, 'underline'), pady=10, padx=10).grid(row=9, column=2)
        Label(self.sf, text="ימים", font=("", 20, 'underline'), pady=10, padx=10).grid(row=9, column=1)
        Label(self.sf, text="סטאטוס", font=("", 20, 'underline'), pady=10, padx=10).grid(row=9, column=0)
        i = 10
        for t in s:
            Label(self.sf, text="   " + t[0] + "   ", font=("", 20), pady=10, padx=10).grid(row=i, column=2)
            Label(self.sf, text="   " + t[2] + "   ", font=("", 20), pady=10, padx=10).grid(row=i, column=1)
            Label(self.sf, text="   " + t[3] + "   ", font=("", 20), pady=10, padx=10).grid(row=i, column=0)
            i = i + 1

        Label(self.sf, text="     ", font=("", 20), pady=10, padx=10).grid(row=i, column=2)
        Label(self.sf, text="     ", font=("", 20), pady=10, padx=10).grid(row=i, column=1)
        Label(self.sf, text="     ", font=("", 20), pady=10, padx=10).grid(row=i, column=0)
        i = i + 1
        Label(self.sf, text="     ", font=("", 20), pady=10, padx=10).grid(row=i, column=2)
        Label(self.sf, text="     ", font=("", 20), pady=10, padx=10).grid(row=i, column=1)
        Label(self.sf, text="     ", font=("", 20), pady=10, padx=10).grid(row=i, column=0)
        i = i + 1
        Button(
            self.sf,
            text="חזור",
            bd=3,
            font=("", 15),
            padx=1,
            pady=1,
            command=self.proj_editor_frame,
        ).grid(row=i, column=0)
        self.sf.pack()

    def add_sprint_frame(self):
        self.sf.forget()
        self.pef.forget()
        self.pf.forget()
        self.apf.forget()

        def add():
            t = SPRINT(self.sprintNum.get(), self.prjNum.get(), self.sprintTime.get(), self.sprintStatus.get())
            t.insert_to_table()

        self.head["text"] = "הוספת ספרינט"

        Label(self.asf, text="מספר הספרינט: ", font=("", 20), pady=10, padx=10).grid(
            row=0, column=0
        )

        Entry(self.asf, textvariable=self.sprintNum, bd=5, font=("", 15)).grid(
            row=0, column=1
        )
        Label(self.asf, text="ימים: ", font=("", 20), pady=10, padx=10).grid(row=1, column=0)
        Entry(self.asf, textvariable=self.sprintTime, bd=5, font=("", 15)).grid(row=1, column=1)

        Label(self.asf, text="סטאטוס: ", font=("", 20), pady=10, padx=10).grid(row=2, column=0)
        Entry(self.asf, textvariable=self.sprintStatus, bd=5, font=("", 15)).grid(row=2, column=1)
        Button(
            self.asf,
            text="הוסף",
            bd=3,
            font=("", 15),
            padx=1,
            pady=1,
            command=add,
        ).grid(row=3, column=1)

        Button(
            self.asf,
            text="חזור",
            bd=3,
            font=("", 15),
            padx=1,
            pady=1,
            command=self.sprints_frame,
        ).grid(row=3, column=2)

        self.asf.pack()

    def edit_sprint_frame(self):
        self.sf.forget()
        self.ssfm.forget()
        self.ssf.forget()
        self.head["text"] = "עריכת ספרינט"
        s = SPRINT.get_sprints_by_num(self.sprintNum.get(), self.prjNum.get())

        def change_n():
            SPRINT.update_num(self.sprintNum.get(), self.prjNum.get(), self.sprintTime.get(), self.sprintStatus.get())
            self.edit_sprint_frame()

        def change_t():
            SPRINT.update_time(self.sprintNum.get(), self.prjNum.get(), self.sprintTime.get(), self.sprintStatus.get())
            self.edit_sprint_frame()

        def change_s():
            SPRINT.update_status(self.sprintNum.get(), self.prjNum.get(), self.sprintTime.get(),
                                 self.sprintStatus.get())
            self.edit_sprint_frame()

        Label(self.esf, text=":מספר ספרינט ", font=("", 20), pady=10, padx=10).grid(
            row=0, column=1
        )
        Label(self.esf, text=s[0][0], font=("", 20), pady=10, padx=10).grid(
            row=0, column=0
        )
        Label(self.esf, text=":ימים ", font=("", 20), pady=10, padx=10).grid(
            row=1, column=1
        )
        Label(self.esf, text=s[0][2], font=("", 20), pady=10, padx=10).grid(
            row=1, column=0
        )
        Label(self.esf, text=":סטאטוס ", font=("", 20), pady=10, padx=10).grid(
            row=2, column=1
        )
        Label(self.esf, text=s[0][3], font=("", 20), pady=10, padx=10).grid(
            row=2, column=0
        )

        Entry(self.esf, textvariable=self.sprintNum, bd=5, font=("", 15)).grid(row=5, column=0)
        Button(self.esf, text="שנה מספר ספרינט ", bd=3, font=("", 15), padx=1, pady=1, command=change_n, ).grid(row=5,
                                                                                                                column=1)

        Entry(self.esf, textvariable=self.sprintTime, bd=5, font=("", 15)).grid(row=6, column=0)
        Button(self.esf, text="שנה מספר ימים", bd=3, font=("", 15), padx=1, pady=1, command=change_t, ).grid(row=6,
                                                                                                             column=1)

        Entry(self.esf, textvariable=self.sprintStatus, bd=5, font=("", 15)).grid(row=7, column=0)
        Button(self.esf, text="שנה סטאטוס", bd=3, font=("", 15), padx=1, pady=1, command=change_s, ).grid(row=7,
                                                                                                          column=1)

        Button(
            self.esf,
            text="חזור",
            bd=3,
            font=("", 15),
            padx=1,
            pady=1,
            command=self.sprints_frame,
        ).grid(row=8, column=2)

        self.esf.pack()

    def remove_sprint_frame(self):
        self.sf.forget()
        self.tf.forget()

        def back():
            self.rsf.forget()
            self.sprints_frame()

        def remove():
            SPRINT.delete_sprint(self.prjNum.get(), self.sprintNum.get())
            self.sprints_frame()

        Button(self.rsf, text="חזור", bd=3, font=("", 15), padx=1, pady=1, command=back, ).grid(row=3, column=0)

        Label(self.rsf, text=":מספר הספרינט ", font=("", 20), pady=10, padx=10).grid(
            row=1, column=1
        )
        Entry(self.rsf, textvariable=self.sprintNum, bd=5, font=("", 15)).grid(
            row=1, column=0
        )

        Button(
            self.rsf,
            text="מחק",
            bd=3,
            font=("", 15),
            padx=1,
            pady=1,
            command=remove,
        ).grid(row=2, column=0)

        self.rsf.pack()

    def show_sprint_frame(self):
        self.sf.forget()
        self.apf.forget()
        self.ssfm.forget()
        self.head["text"] = "הצגת ספרינט"

        def show():
            self.ssf.forget()

            if not SPRINT.get_sprints_by_num(self.sprintNum.get(), self.prjNum.get()):
                ms.showerror("שגיאה", "הספרינט המבוקש לא נמצא")
                return
            self.show_sprint_frame_main()

        Label(self.ssf, text=":מספר ספרינט ", font=("", 20), pady=10, padx=10).grid(row=0, column=0)

        Entry(self.ssf, textvariable=self.sprintNum, bd=5, font=("", 15)).grid(row=0, column=1)
        Button(self.ssf, text="הצג", bd=3,
               font=("", 15), padx=1, pady=1,
               command=show,
               ).grid(row=2, column=0)
        Button(
            self.ssf,
            text="חזור",
            bd=3,
            font=("", 15),
            padx=1,
            pady=1,
            command=self.developer_frame,
        ).grid(row=3, column=2)

        self.ssf.pack()

    def show_sprint_frame_dev(self):
        self.dpef.forget()
        self.apf.forget()
        self.ssfm.forget()
        self.head["text"] = " הצגת ספרינט למפתח"

        def showw():
            self.sst.forget()

            if not SPRINT.get_sprints_by_num(self.sprintNum.get(), self.prjNum.get()):
                ms.showerror("שגיאה", "הספרינט המבוקש לא נמצא")
                return
            self.show_sprint_frame_main_dev()

        Label(self.sst, text=":מספר ספרינט ", font=("", 20), pady=10, padx=10).grid(row=0, column=0)

        Entry(self.sst, textvariable=self.sprintNum, bd=5, font=("", 15)).grid(row=0, column=1)
        Button(self.sst, text="הצג", bd=3,
               font=("", 15), padx=1, pady=1,
               command=showw,
               ).grid(row=2, column=0)
        Button(
            self.sst,
            text="חזור",
            bd=3,
            font=("", 15),
            padx=1,
            pady=1,
            command=self.developer_frame,
        ).grid(row=3, column=2)
        self.sst.pack()

    def show_sprint_frame_main_dev(self):
        self.sst.forget()
        self.tasd.forget()
        self.head["text"] = " הצגת ספרינט מפתח"
        t = SPRINT.get_sprints_by_num(self.sprintNum.get(), self.prjNum.get())
        Label(self.ssfmd, text=":מספר ספרינט ", font=("", 20), pady=10, padx=10).grid(
            row=0, column=1
        )
        Label(self.ssfmd, text=self.sprintNum.get(), font=("", 20), pady=10, padx=10).grid(
            row=0, column=0
        )
        Label(self.ssfmd, text=":ימים ", font=("", 20), pady=10, padx=10).grid(
            row=1, column=1
        )
        Label(self.ssfmd, text=t[0][2], font=("", 20), pady=10, padx=10).grid(
            row=1, column=0
        )
        Label(self.ssfmd, text=":סטאטוס ", font=("", 20), pady=10, padx=10).grid(
            row=2, column=1
        )
        Label(self.ssfmd, text=t[0][3], font=("", 20), pady=10, padx=10).grid(
            row=2, column=0
        )

        Button(
            self.ssfmd,
            text="משימות משויכות",
            bd=3,
            font=("", 15),
            padx=1,
            pady=1,
            command=self.tasks_assign_sprint_dev,
        ).grid(row=4, column=1)

        Button(
            self.ssfmd,
            text="חזור",
            bd=3,
            font=("", 15),
            padx=1,
            pady=1,
            command=self.sprints_frame,
        ).grid(row=5, column=2)

        self.ssfmd.pack()

    def show_sprint_frame_main(self):
        self.ssf.forget()
        self.tas.forget()
        self.head["text"] = "הצגת ספרינט"
        t = SPRINT.get_sprints_by_num(self.sprintNum.get(), self.prjNum.get())
        Label(self.ssfm, text=":מספר ספרינט ", font=("", 20), pady=10, padx=10).grid(
            row=0, column=1
        )
        Label(self.ssfm, text=self.sprintNum.get(), font=("", 20), pady=10, padx=10).grid(
            row=0, column=0
        )
        Label(self.ssfm, text=":ימים ", font=("", 20), pady=10, padx=10).grid(
            row=1, column=1
        )
        Label(self.ssfm, text=t[0][2], font=("", 20), pady=10, padx=10).grid(
            row=1, column=0
        )
        Label(self.ssfm, text=":סטאטוס ", font=("", 20), pady=10, padx=10).grid(
            row=2, column=1
        )
        Label(self.ssfm, text=t[0][3], font=("", 20), pady=10, padx=10).grid(
            row=2, column=0
        )
        Button(
            self.ssfm,
            text="עדכן ספרינט",
            bd=3,
            font=("", 15),
            padx=1,
            pady=1,
            command=self.edit_sprint_frame,
        ).grid(row=3, column=1)
        Button(
            self.ssfm,
            text="משימות משויכות",
            bd=3,
            font=("", 15),
            padx=1,
            pady=1,
            command=self.tasks_assign_sprint,
        ).grid(row=4, column=1)

        Button(
            self.ssfm,
            text="חזור",
            bd=3,
            font=("", 15),
            padx=1,
            pady=1,
            command=self.sprints_frame,
        ).grid(row=5, column=2)

        self.ssfm.pack()

    def tasks_assign_sprint(self):
        self.ssfm.forget()
        self.ssfmd.forget()
        self.atts.forget()
        self.dtfs.forget()

        tasks = TASK_SPRINT.get_sprint_tasks(self.prjNum.get(), self.sprintNum.get())

        Label(self.tas, text="משימות המשויכות לספרינט", font=("", 20), pady=10, padx=10).grid(row=8, column=1)

        Label(self.tas, text="מזהה משימה", font=("", 20, 'underline'), pady=10, padx=10).grid(row=9, column=2)
        Label(self.tas, text="תאור", font=("", 20, 'underline'), pady=10, padx=10).grid(row=9, column=1)

        i = 10
        for t in tasks:
            Label(self.tas, text="   " + t[0] + "   ", font=("", 20), pady=10, padx=10).grid(row=i, column=2)
            Label(self.tas, text="   " + t[3] + "   ", font=("", 20), pady=10, padx=10).grid(row=i, column=1)
            i = i + 1

        Label(self.tas, text="     ", font=("", 20), pady=10, padx=10).grid(row=i, column=2)
        Label(self.tas, text="     ", font=("", 20), pady=10, padx=10).grid(row=i, column=1)

        i = i + 1

        Label(self.tas, text="     ", font=("", 20), pady=10, padx=10).grid(row=i, column=1)
        Label(self.tas, text="     ", font=("", 20), pady=10, padx=10).grid(row=i, column=0)
        i = i + 1
        Button(
            self.tas,
            text="הוסף משימה לספרינט",
            bd=3,
            font=("", 15),
            padx=1,
            pady=1,
            command=self.add_task_to_sprint,
        ).grid(row=2, column=2)
        Button(
            self.tas,
            text="הסרת משימה מהספרינט",
            bd=3,
            font=("", 15),
            padx=1,
            pady=1,
            command=self.delete_task_from_sprint,
        ).grid(row=3, column=2)

        Button(
            self.tas,
            text="חזור",
            bd=3,
            font=("", 15),
            padx=1,
            pady=1,
            command=self.show_sprint_frame_main,
        ).grid(row=4, column=2)
        self.tas.pack()

    def tasks_assign_sprint_dev(self):
        self.ssfmd.forget()
        self.ssfm.forget()
        self.atts.forget()
        self.dtfs.forget()

        tasks = TASK_SPRINT.get_sprint_tasks(self.prjNum.get(), self.sprintNum.get())

        Label(self.tasd, text="משימות המשויכות לספרינט", font=("", 20), pady=10, padx=10).grid(row=8, column=1)

        Label(self.tasd, text="מזהה משימה", font=("", 20, 'underline'), pady=10, padx=10).grid(row=9, column=2)
        Label(self.tasd, text="תאור", font=("", 20, 'underline'), pady=10, padx=10).grid(row=9, column=1)

        i = 10
        for t in tasks:
            Label(self.tasd, text="   " + t[0] + "   ", font=("", 20), pady=10, padx=10).grid(row=i, column=2)
            Label(self.tasd, text="   " + t[3] + "   ", font=("", 20), pady=10, padx=10).grid(row=i, column=1)
            i = i + 1

        Label(self.tasd, text="     ", font=("", 20), pady=10, padx=10).grid(row=i, column=2)
        Label(self.tasd, text="     ", font=("", 20), pady=10, padx=10).grid(row=i, column=1)

        i = i + 1

        Label(self.tasd, text="     ", font=("", 20), pady=10, padx=10).grid(row=i, column=1)
        Label(self.tasd, text="     ", font=("", 20), pady=10, padx=10).grid(row=i, column=0)
        i = i + 1

        Button(
            self.tasd,
            text="חזור",
            bd=3,
            font=("", 15),
            padx=1,
            pady=1,
            command=self.show_sprint_frame_main,
        ).grid(row=4, column=2)
        self.tasd.pack()

    def add_task_to_sprint(self):
        self.ssfm.forget()
        self.tas.forget()
        tasks = TASK.get_tasks(self.prjNum.get())

        def addTask():
            for t in tasks:
                if t[1] == self.taskId.get():
                    self.description.set(t[6])
            TASK_SPRINT.addTask(self.taskId.get(), self.prjNum.get(), self.sprintNum.get(), self.description.get())

        Label(self.atts, text="משימות הקיימות בפרויקט", font=("", 20), pady=10, padx=10).grid(row=8, column=1)

        Label(self.atts, text="מזהה משימה", font=("", 20, 'underline'), pady=10, padx=10).grid(row=9, column=2)
        Label(self.atts, text="תיאור", font=("", 20, 'underline'), pady=10, padx=10).grid(row=9, column=1)

        i = 10
        for t in tasks:
            Label(self.atts, text="   " + t[1] + "   ", font=("", 20), pady=10, padx=10).grid(row=i, column=2)
            Label(self.atts, text="   " + t[6] + "   ", font=("", 20), pady=10, padx=10).grid(row=i, column=1)
            i = i + 1

        Label(self.atts, text="     ", font=("", 20), pady=10, padx=10).grid(row=i, column=2)
        Label(self.atts, text="     ", font=("", 20), pady=10, padx=10).grid(row=i, column=1)

        i = i + 1

        Label(self.atts, text="     ", font=("", 20), pady=10, padx=10).grid(row=i, column=1)
        Label(self.atts, text="     ", font=("", 20), pady=10, padx=10).grid(row=i, column=0)
        i = i + 1

        Label(self.atts, text="מזהה של משימה:", font=("", 20), pady=10, padx=10).grid(row=i, column=2)

        Entry(self.atts, textvariable=self.taskId, bd=5, font=("", 15)).grid(
            row=i, column=1
        )
        i = i + 1
        Button(
            self.atts,
            text="הוסף משימה",
            bd=3,
            font=("", 15),
            padx=1,
            pady=1,
            command=addTask,
        ).grid(row=i, column=2)
        i = i + 1
        Button(
            self.atts,
            text="חזור",
            bd=3,
            font=("", 15),
            padx=1,
            pady=1,
            command=self.tasks_assign_sprint,
        ).grid(row=i, column=2)
        self.atts.pack()

    def delete_task_from_sprint(self):
        self.tas.forget()

        def remove():
            TASK_SPRINT.deleteTask(self.taskId.get(), self.prjNum.get(), self.sprintNum.get())
            self.tasks_assign_sprint()

        self.head["text"] = "הסרת משימה"
        Label(self.dtfs, text="מספר מזהה של משימה: ", font=("", 20), pady=10, padx=10).grid(
            row=0, column=1
        )
        Entry(self.dtfs, textvariable=self.taskId, bd=5, font=("", 15)).grid(
            row=0, column=0
        )
        Button(
            self.dtfs,
            text="הסרת משימה",
            bd=3,
            font=("", 15),
            padx=1,
            pady=1,
            command=remove,
        ).grid(row=1, column=2)
        Button(
            self.dtfs,
            text="חזור",
            bd=3,
            font=("", 15),
            padx=1,
            pady=1,
            command=self.tasks_assign_sprint,
        ).grid(row=2, column=2)
        self.dtfs.pack()

    def message_to_manager(self):

        def back():
            self.dspf.forget()
            self.custumer_frame()

        def send():
            self.prjNum.set(PROJECT_customer.get_proj(self.username.get())[0][0])
            x = PROJECT.projectManager(self.prjNum.get())
            MESSAGE.new_message(self.username.get(), x, self.messageTo.get())
            self.message_to_manager()

        self.dpf.forget()
        self.cusf.forget()
        self.head["text"] = "שליחת הודעה למנהל הפרויקט"

        Label(self.dspf, text="הודעה:: ", font=("", 20), pady=10, padx=10).grid(
            row=0, column=1
        )
        Entry(self.dspf, textvariable=self.messageTo, bd=5, font=("", 15)).grid(
            row=0, column=0
        )
        Button(
            self.dspf,
            text="שלח",
            bd=3,
            font=("", 15),
            padx=1,
            pady=1,
            command=send, ).grid(row=2, column=1)

        Button(
            self.dspf,
            text="חזור",
            bd=3,
            font=("", 15),
            padx=1,
            pady=1,
            command=back, ).grid(row=3, column=1)

        self.dspf.pack()

    ###########task editor##############

    def add_task_frame(self):
        self.tf.forget()

        def back():
            self.atf.forget()
            self.task_frame()

        def add_task():
            t = TASK(self.taskId.get(), self.time.get(), self.crew.get(), self.prjNum.get(), self.status.get(),
                     self.priorty.get(), self.description.get())
            t.insert_to_table()

        Button(self.atf, text="חזור", bd=3, font=("", 15), padx=1, pady=1, command=back, ).grid(row=0, column=1)
        Label(self.atf, text=":מזהה של משימה ", font=("", 20), pady=10, padx=10).grid(row=1, column=1)
        Entry(self.atf, textvariable=self.taskId, bd=5, font=("", 15)).grid(row=1, column=0)
        Label(self.atf, text=":מספר שעות מוערך להשלמת משימה ", font=("", 20), pady=10, padx=10).grid(row=2, column=1)
        Entry(self.atf, textvariable=self.time, bd=5, font=("", 15)).grid(row=2, column=0)
        Label(self.atf, text=":מספר צוות דרוש ", font=("", 20), pady=10, padx=10).grid(row=3, column=1)
        Entry(self.atf, textvariable=self.crew, bd=5, font=("", 15)).grid(row=3, column=0)
        Label(self.atf, text=":סטאטוס (IN PROGRES/DONE/DEF) ", font=("", 20), pady=10, padx=10).grid(row=4, column=1)
        Entry(self.atf, textvariable=self.status, bd=5, font=("", 15)).grid(row=4, column=0)
        Label(self.atf, text=":עדיפות H/L/M ", font=("", 20), pady=10, padx=10).grid(row=5, column=1)
        Entry(self.atf, textvariable=self.priorty, bd=5, font=("", 15)).grid(row=5, column=0)
        Label(self.atf, text=":תיאור המשימה ", font=("", 20), pady=10, padx=10).grid(row=6, column=1)
        Entry(self.atf, textvariable=self.description, bd=5, font=("", 15)).grid(row=6, column=0)
        Button(
            self.atf,
            text="הוסף",
            bd=3,
            font=("", 15),
            padx=1,
            pady=1,
            command=add_task,
        ).grid(row=7, column=0)

        self.head["text"] = "הוספת משימה"
        self.atf.pack()

    def add_task_frame_developer(self):
        self.tf.forget()
        self.df.forget()

        def back():
            self.atf.forget()
            self.task_frame()

        def add_task_developer():
            t = TASK(self.taskId.get(), self.time.get(), self.crew.get(), self.prjNum.get(), self.status.get(),
                     self.priorty.get())
            t.insert_to_table()

        Button(self.atf, text="חזור", bd=3, font=("", 15), padx=1, pady=1, command=self.developer_frame, ).grid(row=8,
                                                                                                                column=1)
        Label(self.atf, text=":מזהה של משימה ", font=("", 20), pady=10, padx=10).grid(row=1, column=1)
        Entry(self.atf, textvariable=self.taskId, bd=5, font=("", 15)).grid(row=1, column=0)
        Label(self.atf, text=":מזהה של פרוייקט ", font=("", 20), pady=10, padx=10).grid(row=6, column=1)
        Entry(self.atf, textvariable=self.prjNum, bd=5, font=("", 15)).grid(row=6, column=0)
        Label(self.atf, text=":מספר שעות מוערך להשלמת משימה ", font=("", 20), pady=10, padx=10).grid(row=2, column=1)
        Entry(self.atf, textvariable=self.time, bd=5, font=("", 15)).grid(row=2, column=0)
        Label(self.atf, text=":מספר צוות דרוש ", font=("", 20), pady=10, padx=10).grid(row=3, column=1)
        Entry(self.atf, textvariable=self.crew, bd=5, font=("", 15)).grid(row=3, column=0)
        Label(self.atf, text=":סטאטוס (IN PROGRES/DONE/DEF) ", font=("", 20), pady=10, padx=10).grid(row=4, column=1)
        Entry(self.atf, textvariable=self.status, bd=5, font=("", 15)).grid(row=4, column=0)
        Label(self.atf, text=":עדיפות H/L/M ", font=("", 20), pady=10, padx=10).grid(row=5, column=1)
        Entry(self.atf, textvariable=self.priorty, bd=5, font=("", 15)).grid(row=5, column=0)
        Button(
            self.atf,
            text="הוסף",
            bd=3,
            font=("", 15),
            padx=1,
            pady=1,
            command=add_task_developer,
        ).grid(row=8, column=0)

        self.head["text"] = "הוספת משימה"
        self.atf.pack()

    def remove_task_frame(self):
        self.tf.forget()

        def back():
            self.rtf.forget()
            self.task_frame()

        def remove():
            TASK.delet_task(self.prjNum.get(), self.taskId.get())

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
            self.developer_frame

        def remove():
            TASK.delet_task(self.prjNum.get(), self.taskId.get())

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
        t = TASK.get_task(self.taskId.get(), self.prjNum.get())
        if not t:
            ms.showerror("error", "המשימה המבוקשת לא נמצאת")
            return

        def back():
            self.dtef.forget()
            self.developer_frame

        def message_crew():
            crew = PROJECT_CREW.get_crew(self.prjNum.get())
            msg = "בפרויקט מספר "
            msg += self.prjNum.get()
            msg += "יש שינוי במשימה "
            msg += self.taskId.get()

            for c in crew:
                MESSAGE.new_message(self.username.get(), c[1], msg)
            MESSAGE.printAll()

        def change_h():
            TASK.update_hour(self.prjNum.get(), self.taskId.get(), self.time.get())
            Label(self.det, text=self.time.get(), font=("", 20), pady=10, padx=10).grid(
                row=1, column=0
            )
            message_crew()

        def change_c():
            TASK.update_crew(self.prjNum.get(), self.taskId.get(), self.crew.get())
            Label(self.det, text=self.crew.get(), font=("", 20), pady=10, padx=10).grid(
                row=2, column=0
            )
            message_crew()

        def change_s():
            TASK.update_status(self.prjNum.get(), self.taskId.get(), self.status.get())
            Label(self.det, text=self.crew.get(), font=("", 20), pady=10, padx=10).grid(
                row=2, column=0
            )
            message_crew()

        self.status.set(t[4])
        self.time.set(t[2])
        self.crew.set(t[3])
        self.dtef.forget()

        Label(self.det, text=":מזה משימה ", font=("", 20), pady=10, padx=10).grid(
            row=0, column=1
        )
        Label(self.det, text=self.taskId.get(), font=("", 20), pady=10, padx=10).grid(
            row=0, column=0
        )
        Label(self.det, text=":מספר שעות מוערך להשלמת משימה ", font=("", 20), pady=10, padx=10).grid(
            row=1, column=1
        )
        Label(self.det, text=self.time.get(), font=("", 20), pady=10, padx=10).grid(
            row=1, column=0
        )
        Label(self.det, text=":כמות אנשי צוות דרוש ", font=("", 20), pady=10, padx=10).grid(
            row=2, column=1
        )
        Label(self.det, text=self.crew.get(), font=("", 20), pady=10, padx=10).grid(
            row=2, column=0
        )

        Entry(self.det, textvariable=self.time, bd=5, font=("", 15)).grid(row=3, column=0)
        Button(self.det, text="שנה מספר שעות ", bd=3, font=("", 15), padx=1, pady=1, command=change_h, ).grid(row=3,
                                                                                                              column=1)

        Entry(self.dtef, textvariable=self.crew, bd=5, font=("", 15)).grid(row=4, column=0)
        Button(self.det, text="שנה כמות צוות", bd=3, font=("", 15), padx=1, pady=1, command=change_c, ).grid(row=4,
                                                                                                             column=1)
        Entry(self.det, textvariable=self.status, bd=5, font=("", 15)).grid(row=5, column=0)
        Button(self.det, text="שנה סטאטוס:", bd=3, font=("", 15), padx=1, pady=1, command=change_s, ).grid(row=5,
                                                                                                           column=1)

        Button(self.det, text="חזור", bd=3, font=("", 15), padx=1, pady=1, command=back, ).grid(row=6, column=0)

        self.det.pack()

    def task_editor_frame(self):
        t = TASK.get_task(self.taskId.get(), self.prjNum.get())
        if not t:
            ms.showerror("error", "המשימה המבוקשת לא נמצאת")
            return

        def back():
            self.dtef.forget()
            self.task_frame()

        def message_crew():
            crew = PROJECT_CREW.get_crew(self.prjNum.get())
            msg = "בפרויקט מספר "
            msg += self.prjNum.get()
            msg += "יש שינוי במשימה "
            msg += self.taskId.get()

            for c in crew:
                MESSAGE.new_message(self.username.get(), c[1], msg)
            MESSAGE.printAll()

        def change_h():
            TASK.update_hour(self.prjNum.get(), self.taskId.get(), self.time.get())
            Label(self.dtef, text=self.time.get(), font=("", 20), pady=10, padx=10).grid(
                row=1, column=0
            )
            message_crew()

        def change_c():
            TASK.update_crew(self.prjNum.get(), self.taskId.get(), self.crew.get())
            Label(self.dtef, text=self.crew.get(), font=("", 20), pady=10, padx=10).grid(
                row=2, column=0
            )
            message_crew()

        def change_s():
            TASK.update_status(self.prjNum.get(), self.taskId.get(), self.status.get())
            Label(self.dtef, text=self.status.get(), font=("", 20), pady=10, padx=10).grid(
                row=3, column=0
            )
            message_crew()

        def change_d():
            TASK.update_description(self.prjNum.get(), self.taskId.get(), self.description.get())
            Label(self.dtef, text=self.description.get(), font=("", 20), pady=10, padx=10).grid(
                row=5, column=0
            )
            message_crew()

        self.time.set(t[2])
        self.crew.set(t[3])
        self.status.set(t[4])
        self.priorty.set(t[5])
        self.description.set(t[6])
        self.shtf.forget()

        Label(self.dtef, text=":מזהה משימה ", font=("", 20), pady=10, padx=10).grid(
            row=0, column=1
        )
        Label(self.dtef, text=self.taskId.get(), font=("", 20), pady=10, padx=10).grid(
            row=0, column=0
        )
        Label(self.dtef, text=":מספר שעות מוערך להשלמת משימה ", font=("", 20), pady=10, padx=10).grid(
            row=1, column=1
        )
        Label(self.dtef, text=self.time.get(), font=("", 20), pady=10, padx=10).grid(
            row=1, column=0
        )
        Label(self.dtef, text=":כמות אנשי צוות דרוש ", font=("", 20), pady=10, padx=10).grid(
            row=2, column=1
        )
        Label(self.dtef, text=self.crew.get(), font=("", 20), pady=10, padx=10).grid(
            row=2, column=0
        )
        Label(self.dtef, text=" :סטאטוס", font=("", 20), pady=10, padx=10).grid(
            row=3, column=1
        )
        Label(self.dtef, text=self.status.get(), font=("", 20), pady=10, padx=10).grid(
            row=3, column=0
        )
        Label(self.dtef, text=" :סטאטוס", font=("", 20), pady=10, padx=10).grid(
            row=3, column=1
        )
        Label(self.dtef, text=self.status.get(), font=("", 20), pady=10, padx=10).grid(
            row=3, column=0
        )
        Label(self.dtef, text=" :עדיפות", font=("", 20), pady=10, padx=10).grid(
            row=4, column=1
        )
        Label(self.dtef, text=self.priorty.get(), font=("", 20), pady=10, padx=10).grid(
            row=4, column=0
        )

        Label(self.dtef, text=" :תיאור", font=("", 20), pady=10, padx=10).grid(
            row=5, column=1
        )
        Label(self.dtef, text=self.description.get(), font=("", 20), pady=10, padx=10).grid(
            row=5, column=0
        )

        Entry(self.dtef, textvariable=self.time, bd=5, font=("", 15)).grid(row=7, column=0)
        Button(self.dtef, text="שנה מספר שעות ", bd=3, font=("", 15), padx=1, pady=1, command=change_h, ).grid(row=7,
                                                                                                               column=1)

        Entry(self.dtef, textvariable=self.crew, bd=5, font=("", 15)).grid(row=8, column=0)
        Button(self.dtef, text="שנה כמות צוות", bd=3, font=("", 15), padx=1, pady=1, command=change_c, ).grid(row=8,
                                                                                                              column=1)

        Entry(self.dtef, textvariable=self.crew, bd=5, font=("", 15)).grid(row=9, column=0)
        Button(self.dtef, text="שנה סטאטוס", bd=3, font=("", 15), padx=1, pady=1, command=change_s, ).grid(row=9,
                                                                                                           column=1)

        Entry(self.dtef, textvariable=self.description, bd=5, font=("", 15)).grid(row=10, column=0)
        Button(self.dtef, text="שנה תיאור", bd=3, font=("", 15), padx=1, pady=1, command=change_d, ).grid(row=10,
                                                                                                          column=1)

        Button(self.dtef, text="חזור", bd=3, font=("", 15), padx=1, pady=1, command=back, ).grid(row=11, column=0)

        self.dtef.pack()

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

        tasks = TASK.get_tasks(self.prjNum.get())

        def back():
            self.tf.forget()
            self.project_frame()

        self.head["text"] = "ניהול משימות"
        Label(self.tf, text=":משימות של פרויקט ", font=("", 20), pady=10, padx=10).grid(row=0, column=1)
        Label(self.tf, text=self.prjName.get(), font=("", 20), pady=10, padx=10).grid(row=0, column=0)

        Button(self.tf, text="חזור", bd=3, font=("", 15), padx=1, pady=1, command=back, ).grid(row=1, column=1)
        Button(self.tf, text="הוסף משימה", bd=3, font=("", 15), padx=1, pady=1, command=self.add_task_frame, ).grid(
            row=2, column=1)
        Button(self.tf, text="הצג משימה", bd=3, font=("", 15), padx=1, pady=1, command=self.show_task_frame, ).grid(
            row=3, column=1)
        Button(self.tf, text="מחק משימה", bd=3, font=("", 15), padx=1, pady=1, command=self.remove_task_frame, ).grid(
            row=4, column=1)

        Label(self.tf, text="משימות הקיימות בפרויקט", font=("", 20), pady=10, padx=10).grid(row=8, column=1)

        Label(self.tf, text="מזהה משימה", font=("", 20, 'underline'), pady=10, padx=10).grid(row=9, column=2)
        Label(self.tf, text="תאור", font=("", 20, 'underline'), pady=10, padx=10).grid(row=9, column=1)

        i = 10
        for t in tasks:
            Label(self.tf, text="   " + t[1] + "   ", font=("", 20), pady=10, padx=10).grid(row=i, column=2)
            Label(self.tf, text="   " + t[6] + "   ", font=("", 20), pady=10, padx=10).grid(row=i, column=1)
            i = i + 1

        Label(self.tf, text="     ", font=("", 20), pady=10, padx=10).grid(row=i, column=2)
        Label(self.tf, text="     ", font=("", 20), pady=10, padx=10).grid(row=i, column=1)

        i = i + 1

        Label(self.tf, text="     ", font=("", 20), pady=10, padx=10).grid(row=i, column=1)
        Label(self.tf, text="     ", font=("", 20), pady=10, padx=10).grid(row=i, column=0)

        self.tf.pack()

    def task_frame_c(self):
        self.pefc.forget()

        tasks = TASK.get_tasks(self.prjNum.get())

        def back():
            self.tfc.forget()
            self.custumer_frame()

        self.head["text"] = "ניהול משימות"
        Label(self.tfc, text=":משימות של פרויקט ", font=("", 20), pady=10, padx=10).grid(row=0, column=1)
        Label(self.tfc, text=self.prjName.get(), font=("", 20), pady=10, padx=10).grid(row=0, column=0)

        Button(self.tfc, text="חזור", bd=3, font=("", 15), padx=1, pady=1, command=back, ).grid(row=1, column=1)

        Label(self.tfc, text="******************", font=("", 20), pady=10, padx=10).grid(row=7, column=0)
        Label(self.tfc, text="******************", font=("", 20), pady=10, padx=10).grid(row=7, column=1)
        Label(self.tfc, text="******************", font=("", 20), pady=10, padx=10).grid(row=7, column=2)
        Label(self.tfc, text="משימות קיימות בפרויקט", font=("", 20), pady=10, padx=10).grid(row=8, column=1)

        Label(self.tfc, text="מזהה משימה", font=("", 20, 'underline'), pady=10, padx=10).grid(row=9, column=2)
        Label(self.tfc, text="סטאטוס", font=("", 20, 'underline'), pady=10, padx=10).grid(row=9, column=1)
        Label(self.tfc, text="מספר צוות דרוש", font=("", 20, 'underline'), pady=10, padx=10).grid(row=9, column=0)
        i = 10
        for t in tasks:
            Label(self.tfc, text="   " + t[1] + "   ", font=("", 20), pady=10, padx=10).grid(row=i, column=2)
            Label(self.tfc, text="   " + t[4] + "   ", font=("", 20), pady=10, padx=10).grid(row=i, column=1)
            Label(self.tfc, text="   " + t[3] + "   ", font=("", 20), pady=10, padx=10).grid(row=i, column=0)
            i = i + 1

        Label(self.tfc, text="     ", font=("", 20), pady=10, padx=10).grid(row=i, column=2)
        Label(self.tfc, text="     ", font=("", 20), pady=10, padx=10).grid(row=i, column=1)
        Label(self.tfc, text="     ", font=("", 20), pady=10, padx=10).grid(row=i, column=0)
        i = i + 1
        Label(self.tfc, text="     ", font=("", 20), pady=10, padx=10).grid(row=i, column=2)
        Label(self.tfc, text="     ", font=("", 20), pady=10, padx=10).grid(row=i, column=1)
        Label(self.tfc, text="     ", font=("", 20), pady=10, padx=10).grid(row=i, column=0)

        self.tfc.pack()

    #########end of task editor##############

    def messages(self, Widgets, r):  #### show the messages the the user have
        # width----the frame u use ( --self.df--- for example)
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
