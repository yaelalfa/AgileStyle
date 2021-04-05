import sqlite3
from task import TASK
from tkinter import *
from tkinter import messagebox as ms
import tkinter as tk
import os


#creat database if not exist and get conecction to it
conn = sqlite3.connect('myDb.db')

#get a cursor to execute sql statements
c = conn.cursor()

#creat table
sql = '''CREATE TABLE IF NOT EXISTS tasks
         (taskId text PRIMARY KEY,
          time INT,
          crewNum INT )'''
c.execute(sql)
conn.commit()
conn.close()



def creat_task_fram():

    root=tk.Tk()
    t_var = tk.StringVar()
    h_var = tk.IntVar()
    c_var = tk.IntVar()
    root.title("create a new task")

    def creat_task():

        t = t_entry.get()
        h = h_entry.get()
        c = c_entry.get()

        root.destroy()

        newt = TASK(t, h, c)
        newt.insert_to_table()



    # creating labels
    head = Label(root, text="create new task", font=("", 35), pady=10)
    head.grid(row=0, column=1)

    t_l = Label(root, text="task ID: ", font=('calibre', 10, 'bold'))
    h_l = Label(root, text="estimated time required (hours)", font=('calibre', 10, 'bold'))
    c_l = Label(root, text="estimated number of crew required :", font=('calibre', 10, 'bold'))

    # creatin entrys
    t_entry = tk.Entry(root, textvariable=t_var, font=('calibre', 10, 'normal'))
    h_entry = tk.Entry(root, textvariable=h_var, font=('calibre', 10, 'normal'))
    c_entry = tk.Entry(root, textvariable=c_var, font=('calibre', 10, 'normal'))

    enter_but = tk.Button(root, text="submit", command=creat_task)

    t_l.grid(row=3, column=0)
    t_entry.grid(row=3, column=1)
    h_l.grid(row=4, column=0)
    h_entry.grid(row=4, column=1)
    c_l.grid(row=5, column=0)
    c_entry.grid(row=5, column=1)
    enter_but.grid(row=6, column=1)
    root.mainloop()





