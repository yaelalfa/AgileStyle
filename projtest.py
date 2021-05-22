import sqlite3

import pytest
class PROJECT:
    def __init__(self, projId, name, us):
        self.projId = projId
        self.name = name
        self.user = us  # usrename

    @classmethod
    def get_ID(cls, proj_id):
        connect = sqlite3.connect('myDb.db')
        cc = connect.cursor()
        sql = """SELECT managerId FROM projects 
                        WHERE  projId=?
                            """
                            
        dt = (proj_id)
        try:
            cc.execute(sql, dt)
            row = cc.fetchone()

            return row



        except Exception:
            ms.showerror("שגיאה", "שגיאה בזמן משיכת פרויקט")
        connect.commit()
        connect.close()
                            
    @classmethod
    def get_project(cls, manger_id, proj_id):
        connect = sqlite3.connect('myDb.db')
        cc = connect.cursor()
        sql = """SELECT * FROM projects 
                            WHERE  managerId=? 
                AND projId=?


                            """

        dt = (manger_id, proj_id)
        try:
            cc.execute(sql, dt)
            row = cc.fetchone()

            return row



        except Exception:
            ms.showerror("שגיאה", "שגיאה בזמן משיכת פרויקט")
        connect.commit()
        connect.close()

def test_get_project():
    project = PROJECT(projId="4",name="aa",us="linm")
    assert project.get_ID(proj_id="4")=="linm"
        
        