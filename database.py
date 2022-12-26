import tkinter.messagebox

import mysql.connector as connector
from datetime import datetime

def establishConnection(user,passwd):
    try:
        global con
        con = connector.connect(user=user, host="localhost", password=passwd)

        if con.is_connected():
            global cur
            cur = con.cursor();
            cur.execute("use bills")
            return 1
    except:
        pass

    return 0

def createTable():

    # Creating a table
    now = datetime.now()
    global table_name
    table_name = "_" + now.strftime("%m_%d_%Y_%H_%M_%S")

    create_table = """CREATE TABLE IF NOT EXISTS {}(
    ITEMS VARCHAR(30),
    WEIGHT FLOAT(8,2),
    MC VARCHAR(10),
    RATE FLOAT(8,2),
    AMOUNT FLOAT(8,2),
    id int auto_increment,
    primary key(id));""".format(table_name)

    cur.execute(create_table)
    con.commit()

def showTablesList():
    cur.execute('show tables')
    tables=[]
    for i in cur.fetchall():
        for j in i:
            tables.append(j)
    return tables

def col_names(tname):
    cur.execute("describe {};".format(tname))
    col_names = [x[0] for x in cur.fetchall()]
    return col_names

def printBill(tname):
    cur.execute('select * from {};'.format(tname))
    bill=cur.fetchall();
    return bill

def total_amount(tname):
    cur.execute("SELECT SUM(Amount) FROM {};".format(tname))
    tot = cur.fetchall()[0][0]
    return tot

def modify(tname, req):
    count = 0
    if req.get("action1") == "make changes":
        col_name = col_names(tname)
        cur.execute("select * from {};".format(tname))
        data = cur.fetchall()
        i=0
        for col in col_name:
            mitems = req.getlist(col)
            cur.execute("select {} from {};".format(col,tname))
            col_values = [x[0] for x in cur.fetchall()]
            print(mitems,col_values)
            if len(req.getlist("new")) == 0:
                for i in range(len(mitems)):
                    if mitems[i] != str(col_values[i]):
                            if type(col_values[i]) == str:
                                cur.execute("""update {}
                                                set {}='{}'
                                                where id={};
                                            """.format(tname, col, mitems[i], data[i][col_name.index("id")]))
                            else:
                                cur.execute("""update {}
                                                set {}={}
                                                where id={};
                                            """.format(tname, col, mitems[i], data[i][col_name.index("id")]))
                            con.commit()

            else:
                mitems = req.getlist("new")
                fin_list = [checknchange(x) for x in mitems[i:i+5]]
                i = i+5
                try:
                    print(fin_list)
                    query = "insert into {} values ('{}',{},{},{},{},0);".format(tname,*fin_list)
                    print(query)
                    cur.execute(query)
                    con.commit()
                    count += 1
                except:
                    pass

    return count
def remove_table(tname):
    cur.execute("drop table {};".format(tname))
    con.commit()
def compare_lists(l1, l2):
    for i in range(len(l1)):
        if l1[i] != l2[i]:
            return i
    return -1

def remove_row(tname,req):
    id = list(dict(req).keys())[0]
    cur.execute("DELETE FROM {} WHERE id = {};".format(tname, int(id)))
    con.commit()

def checknchange(n):
    if n == "":
        return "null"

    try:
        result = int(n)
    except:
        result = n
    return result