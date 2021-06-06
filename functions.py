import mysql.connector


users = mysql.connector.connect(
    host="b0cqj1javyo2et169rya-mysql.services.clever-cloud.com",
    user="usqjg0g0nbwvdfdf",
    passwd="88KJ85sZX1CKqSFyzJ09",
    database="b0cqj1javyo2et169rya"
)



def insert_to_table(pj,n,us,end):
    connect = users
    cc = connect.cursor(buffered=True)
    sql = '''INSERT INTO projects VALUES(%s,%s,%s,%s)'''



    dats_tuple = (pj, n, us,end)
    try:
        cc.execute(sql, dats_tuple)
        connect.commit()
        return 1
    except Exception:
        return -1




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



def userInproj(projid):
    connect = users
    cc = connect.cursor(buffered=True)

    sql = """SELECT user
                    FROM project_crew 
                    where projId=%s         

                                    """
    dt = (projid,)
    cc.execute(sql, dt)
    user = cc.fetchone()

    if not user:
        return -1

    ru = user[0]
    return ru

    connect.commit()
  ####################################################

Maneger = "manager"
Developer = "developer"
Custumer = "customer"

def new_user(username, password, role):

    if role not in [Custumer, Maneger, Developer]:
        return -1

    connect = users
    cc = connect.cursor(buffered=True)

    sql = "INSERT INTO users(username, password, role) VALUES(%s,%s,%s)"
    dt = (username, password, role)

    try:
        cc.execute(sql, dt)
        return 1

    except Exception:
            return -1










def login(username,password):


    connect = users
    cc = connect.cursor(buffered=True)

    sql = "SELECT * FROM users WHERE username = %s and password = %s"

    dt = (username,password)

    try:

        cc.execute(sql, dt)
        user = cc.fetchone()
        if user:
            return user[2]

        else:
            return -1

    except Exception:
            return -1








