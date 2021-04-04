import sqlite3
from tkinter import *
from tkinter import messagebox as ms
import os

class TASK:
    def __init__(self,taskId,time,crewN):
        self.taskId=taskId
        self.time=time
        self.crewNum=crewN


    def insert_to_table(self):
        conn = sqlite3.connect('myDb.db')
        c = conn.cursor()
        sql = '''INSERT INTO tasks VALUES(?,?,?)
         '''
        dats_tuple = (self.taskId,self.time,self.crewNum)

        try:
            c.execute(sql, dats_tuple)
            ms.showinfo("משימה חדשה נוצרה בהצלחה")

        except Exception:
            ms.showerror("שגיאה! נסיון להכניס משימה חדשה לטבלה נכשל")

        conn.commit()
        conn.close()

    @classmethod
    def printAll(cls):
        conn = sqlite3.connect('myDb.db')
        c = conn.cursor()

        sql = 'SELECT * FROM tasks'
        c.execute(sql)
        rows = c.fetchall()

        for row in rows:
            print(row)
        conn.commit()
        conn.close()

