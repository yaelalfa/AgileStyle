import mysql.connector


users = mysql.connector.connect(
    host="b0cqj1javyo2et169rya-mysql.services.clever-cloud.com",
    user="usqjg0g0nbwvdfdf",
    passwd="88KJ85sZX1CKqSFyzJ09",
    database="b0cqj1javyo2et169rya"
)



def insert_to_table(pj,n,us):
    connect = users
    cc = connect.cursor(buffered=True)
    sql = '''INSERT INTO projects VALUES(%s,%s,%s)
     '''
    dats_tuple = (pj, n, us)
    try:
        cc.execute(sql, dats_tuple)
        return 1
    except Exception:
        return -1
    connect.commit()



def projectManager(id):
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
        return -1

    ru = user[0]
    return ru

    connect.commit()




def insert_user(u,p,r):
    connect = users
    cc = connect.cursor(buffered=True)
    sql = '''INSERT INTO projects VALUES(%s,%s,%s)
     '''
    dats_tuple = (u,p,r)
    try:
        cc.execute(sql, dats_tuple)
        return 1
    except Exception:
        return -1
    connect.commit()

def new_message(sender, to, message):
    conect = users
    cc = conect.cursor(buffered=True)
    sql = '''INSERT INTO user_message VALUES(%s,%s,%s)
                        '''
    dats_tuple = (sender, to, message)

    try:
        cc.execute(sql, dats_tuple)
        return 1

    except Exception:
        return -1

    conect.commit()



def userInproj(pid):
    connect = users
    cc = connect.cursor(buffered=True)

    sql = """SELECT user
                    FROM project_crew 
                    where projId=%s         

                                    """
    dt = (pid,)
    cc.execute(sql, dt)
    user = cc.fetchone()

    if not user:
        return -1

    ru = user[0]
    return ru

    connect.commit()

