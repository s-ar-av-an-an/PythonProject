import mysql.connector as connector
from datetime import date

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
    global table_name
    table_name = "_" + date.today().strftime("%Y_%m_%d")

    create_table = """CREATE TABLE IF NOT EXISTS {}(
    ITEMS VARCHAR(30),
    WEIGHT FLOAT(8,2),
    MC VARCHAR(10),
    RATE FLOAT(8,2),
    AMOUNT FLOAT(8,2));""".format(table_name)

    cur.execute(create_table)

    cur.execute("""SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_name = '{0}' """.format(table_name))

    if cur.fetchone()[0] == 1:
        con.commit()
        return 1

    return 0

def showTablesList():
    cur.execute('show tables')
    tables=[]
    for i in cur.fetchall():
        for j in i:
            tables.append(j)
    return tables

def printBill(tname):
    cur.execute('select * from {};'.format(tname))
    bill=cur.fetchall();
    return bill
