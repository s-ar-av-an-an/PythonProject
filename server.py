from flask import Flask, render_template, request, redirect, url_for
import database

app = Flask(__name__)
nrcount = 0
@app.route('/')
def launch():
    return render_template('login.html')

@app.route('/form_login', methods=['POST', 'GET'])
def authenticate():
    global temp_tname
    user = request.form["username"]
    passwd = request.form["password"]
    if database.establishConnection(user, passwd) == 1:
        return redirect(url_for('dashboard'))
    else:
        return render_template('login.html', status="Invalid Credentials")

@app.route('/dashboard', methods=['POST', 'GET'])
def dashboard():
    return render_template("home.html")
@app.route('/modify_bill',methods=['POST','GET'])
def modify_bill():
    return render_template('modifybills.html', bills=database.showTablesList(), content='Bills', visibilty="invisible", size=nrcount)
@app.route('/new_tbl')
def new_tbl():
    database.createTable()
    return redirect(url_for('modify_bill'))
@app.route('/view_tables', methods=['POST', 'GET'])
def view_tables():
    return render_template("bills.html", bills=database.showTablesList(),content='Bills')

@app.route('/view_tables/bills', methods=['POST', 'GET'])
def viewBills():
    temp_tname=request.form.get("action")
    rows = database.printBill(temp_tname)
    return render_template('invoice.html', rows=rows,bills=database.showTablesList(),content='Bills', total=database.total_amount(temp_tname))

@app.route('/table_name', methods=['POST', 'GET'])
def vBills():
    global temp_tname
    temp_tname = request.form.get("action")
    rows = database.printBill(temp_tname)
    col_names = database.col_names(temp_tname)
    col_names.remove('id')
    return render_template('modifybills.html', rows=rows, bills=database.showTablesList(), content='Bills', col_names = col_names, visibilty="wrapper", size=nrcount)
@app.route('/modify_table', methods=['POST', 'GET'])
def modify_bills():
    global temp_tname,nrcount
    flag = database.modify(temp_tname, request.form)
    nrcount-=flag
    rows = database.printBill(temp_tname)
    col_names = database.col_names(temp_tname)
    col_names.remove('id')
    return render_template('modifybills.html', rows=rows, bills=database.showTablesList(), content='Bills', col_names = col_names, size=nrcount)
@app.route('/remove',methods=["POST","GET"])
def remove_table():
    global temp_tname
    database.remove_table(temp_tname)
    return redirect(url_for("modify_bill"))
@app.route('/plus')
def add_row():
    global nrcount
    rows = database.printBill(temp_tname)
    col_names = database.col_names(temp_tname)
    col_names.remove('id')
    nrcount+=1
    return render_template('modifybills.html', extras=[i for i in range(nrcount)], rows=rows,
                           bills=database.showTablesList(), content='Bills', col_names=col_names, size=nrcount)

@app.route('/remove_row',methods=['POST','GET'])
def rem_row():
    global temp_tname
    value = list(dict(request.form).values())[0]
    if value == "x":
        database.remove_row(temp_tname,request.form)
        rows = database.printBill(temp_tname)
        col_names = database.col_names(temp_tname)
        col_names.remove('id')
        return render_template('modifybills.html', rows=rows, bills=database.showTablesList(), content='Bills', col_names = col_names, visibilty="wrapper", size=nrcount)
@app.route('/minus')
def minus():
    global nrcount
    nrcount-=2
    return redirect(url_for('add_row'))

if __name__ == '__main__':
    app.run(debug=True)
