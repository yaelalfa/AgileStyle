import sqlite3
from project import PROJECT
from tkinter import *
from tkinter import messagebox as ms
import tkinter as tk
import os

# creat database if not exist and get conecction to it
conn = sqlite3.connect('myDb.db')

# get a cursor to execute sql statements
c = conn.cursor()

# creat table
sql = '''CREATE TABLE IF NOT EXISTS projects
         (projId text PRIMARY KEY,
          name text,
          managerId text )'''
c.execute(sql)
conn.commit()
conn.close()

root = tk.Tk()
root.withdraw()
name_var = tk.StringVar()
pId_var = tk.StringVar()
mId_var = tk.StringVar()


def creat_proj_frame():
    root.destroy()
    creat = tk.Tk()
    creat.title("creat a new project")

    def creat_proj():
        name = name_entry.get()
        pId = pId_entry.get()
        mid = mId_entry.get()

        creat.destroy()

        newp = PROJECT(pId, name, mid)
        newp.insert_to_table()

        PROJECT.printAll()

    # creating labels
    head = Label(creat, text="יצירת פקוירט חדש", font=("", 35), pady=10)
    head.grid(row=0, column=1)

    pId_l = Label(creat, text=":מספר מזה", font=('calibre', 10, 'bold'))
    name_l = Label(creat, text=":שם הפרויקט", font=('calibre', 10, 'bold'))
    mId_l = Label(creat, text=":תז מנהל פקוירט", font=('calibre', 10, 'bold'))
    # creatin entrys
    pId_entry = tk.Entry(creat, textvariable=pId_var, font=('calibre', 10, 'normal'))
    name_entry = tk.Entry(creat, textvariable=name_var, font=('calibre', 10, 'normal'))
    mId_entry = tk.Entry(creat, textvariable=mId_var, font=('calibre', 10, 'normal'))

    enter_but = tk.Button(creat, text="הוסף", command=creat_proj)

    name_l.grid(row=3, column=0)
    name_entry.grid(row=3, column=1)
    pId_l.grid(row=4, column=0)
    pId_entry.grid(row=4, column=1)
    mId_l.grid(row=5, column=0)
    mId_entry.grid(row=5, column=1)
    enter_but.grid(row=6, column=1)
    creat.mainloop()


def remove_proj_frame():
    root.destroy()
    remove = tk.Tk()
    remove.title("remove project")

    def remove_proj():
        pId = pId_entry.get()
        PROJECT.remove_by_id(pId)
        remove.destroy()

    head = Label(remove, text="מחיקת פרויקט", font=("", 35), pady=10)
    head.grid(row=0, column=1)
    pId_l = Label(remove, text=":מספר מזהה פרויקט למחיקה", font=('calibre', 10, 'bold'))
    pId_entry = tk.Entry(remove, textvariable=pId_var, font=('calibre', 10, 'normal'))

    enter_but = tk.Button(remove, text="מחק", command=remove_proj)

    pId_l.grid(row=3, column=0)
    pId_entry.grid(row=3, column=1)

    enter_but.grid(row=4, column=1)
    remove.mainloop()


def menu():
    root.deiconify()
    root.title("project editor")
    head = Label(root, text="ניהול פרויקט", font=("", 35), pady=10)
    head.pack()
    Addproj = tk.Button(root, text="צור פרויקט חדש", padx=10, pady=10, command=creat_proj_frame)
    Addproj.pack()
    removeproj = tk.Button(root, text="מחק פרויקט", padx=10, pady=10, command=remove_proj_frame)
    removeproj.pack()
    root.mainloop()




