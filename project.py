import sqlite3
from tkinter import *
from tkinter import messagebox as ms
import os


class PROJECT:
    def __init__(self, projId, name, mId):
        self.projId = projId
        self.name = name
        self.mId = mId

    def insert_to_table(self):
        conn = sqlite3.connect('myDb.db')
        c = conn.cursor()
        sql = '''INSERT INTO projects VALUES(?,?,?)
        '''
        dats_tuple = (self.projId, self.name, self.mId)

        try:
            c.execute(sql, dats_tuple)
            ms.showinfo("פרויקט חדש נוצר בהצלחה")

        except Exception:
            ms.showerror("שגיאה! נסיון להכניס פרויקט חדש לטבלה נכשל")

        conn.commit()

        conn.close()

    def remove_from_table(self):
        conn = sqlite3.connect('myDb.db')
        c = conn.cursor()
        sql = """DELETE FROM projects 
                WHERE projId=? 
                 """
        c.execute(sql, (self.projId))
        conn.commit()
        conn.close()

    @classmethod
    def remove_by_id(cls, id):
        conn = sqlite3.connect('myDb.db')
        c = conn.cursor()
        sql = """DELETE FROM projects 
                       WHERE projId=? 

                        """
        try:
            c.execute(sql, (id))
            ms.showinfo("נמחק פרויקט: " + id)

        except Exception:
            ms.showerror("שגיאה במחיקה")
        conn.commit()
        conn.close()

    @classmethod
    def printAll(cls):

        conn = sqlite3.connect('myDb.db')
        c = conn.cursor()

        sql = 'SELECT * FROM projects'
        c.execute(sql)
        rows = c.fetchall()

        for row in rows:
            print(row)
        conn.commit()
        conn.close()

