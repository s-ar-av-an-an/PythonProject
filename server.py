from flask import Flask, render_template, request, redirect, url_for
import database

app = Flask(__name__)
nrcount = 0
flag = False
@app.route('/')
def launch():
    return render_template('login.html')

@app.route('/form_login', methods=['POST', 'GET'])
def authenticate():
    global temp_tname,flag
    user = request.form["username"]
    passwd = request.form["password"]
    if database.establishConnection(user, passwd) == 1:
        flag = True
        return redirect(url_for('dashboard'))
    else:
        return render_template('login.html', status="Invalid Credentials")

@app.route('/dashboard', methods=['POST', 'GET'])
def dashboard():
    if flag:
        return render_template("home.html")
    else:
        return "YOU HAVE BEEN LOGGED OUT"
@app.route('/modify_bill',methods=['POST','GET'])
def modify_bill():
    if flag:
        return render_template('modifybills.html', bills=database.showTablesList(), content='Bills', visibilty="invisible", size=nrcount, sidebar="visible")
    else:
        return "YOU HAVE BEEN LOGGED OUT"
@app.route('/new_tbl')
def new_tbl():
    if flag:
        database.createTable()
        return redirect(url_for('modify_bill'))
    else:
        return "YOU HAVE BEEN LOGGED OUT"
@app.route('/view_tables', methods=['POST', 'GET'])
def view_tables():
    if flag:
        return render_template("invoice.html", bills=database.showTablesList(),content='Bills',stat="hidden")
    else:
        return "YOU HAVE BEEN LOGGED OUT"

@app.route('/view_tables/bills', methods=['POST', 'GET'])
def viewBills():
    if flag:
        temp_tname = request.form.get("action")
        rows = database.printBill(temp_tname)
        return render_template('invoice.html', rows=rows,bills=database.showTablesList(),content='Bills', total=database.total_amount(temp_tname),stat="visible")
    else:
        return "YOU HAVE BEEN LOGGED OUT"

@app.route('/table_name', methods=['POST', 'GET'])
def vBills():
    if flag:
        global temp_tname
        temp_tname = request.form.get("action")
        rows = database.printBill(temp_tname)
        col_names = database.col_names(temp_tname)
        col_names.remove('id')
        return render_template('modifybills.html', rows=rows, bills=database.showTablesList(), content='Bills', col_names = col_names, visibilty="wrapper", size=nrcount)
    else:
        return "YOU HAVE BEEN LOGGED OUT"
@app.route('/modify_table', methods=['POST', 'GET'])
def modify_bills():
    if flag:
        global temp_tname,nrcount
        c = database.modify(temp_tname, request.form)
        nrcount-=c
        rows = database.printBill(temp_tname)
        col_names = database.col_names(temp_tname)
        col_names.remove('id')
        return render_template('modifybills.html', rows=rows, bills=database.showTablesList(), content='Bills', col_names = col_names, size=nrcount, visibilty="wrapper")
    else:
        return "YOU HAVE BEEN LOGGED OUT"
@app.route('/remove',methods=["POST","GET"])
def remove_table():
    if flag:
        global temp_tname
        database.remove_table(temp_tname)
        return redirect(url_for("modify_bill"))
    else:
        return "YOU HAVE BEEN LOGGED OUT"
@app.route('/plus')
def add_row():
    if flag:
        global nrcount
        rows = database.printBill(temp_tname)
        col_names = database.col_names(temp_tname)
        col_names.remove('id')
        nrcount+=1
        return render_template('modifybills.html', extras=[i for i in range(nrcount)], rows=rows,
                               bills=database.showTablesList(), content='Bills', col_names=col_names, size=nrcount,visibilty="wrapper")
    else:
        return "YOU HAVE BEEN LOGGED OUT"

@app.route('/remove_row',methods=['POST','GET'])
def rem_row():
    if flag:
        global temp_tname
        value = list(dict(request.form).values())[0]
        if value == "x":
            database.remove_row(temp_tname,request.form)
            rows = database.printBill(temp_tname)
            col_names = database.col_names(temp_tname)
            col_names.remove('id')
            return render_template('modifybills.html', rows=rows, bills=database.showTablesList(), content='Bills', col_names = col_names, visibilty="wrapper", size=nrcount)
    else:
        return "YOU HAVE BEEN LOGGED OUT"
@app.route('/minus')
def minus():
    if flag:
        global nrcount
        nrcount-=2
        return redirect(url_for('add_row'))
    else:
        return "YOU HAVE BEEN LOGGED OUT"
@app.route('/signout')
def sign_out():
    global flag
    database.signout()
    flag = False
    return redirect(url_for('launch'))

if __name__ == '__main__':
    app.run(debug=True)
