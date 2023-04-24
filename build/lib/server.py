from flask import Flask, render_template, request, redirect, url_for
import database

app = Flask(__name__)


@app.route('/')
def launch():
    return render_template('login.html')


@app.route('/form_login', methods=['POST', 'GET'])
def authenticate():
    user = request.form["username"]
    passwd = request.form["password"]
    if database.establishConnection(user, passwd) == 1:
        return render_template('home.html')
    else:
        return render_template('login.html', status="Invalid Credentials")

@app.route('/create_bill',methods=['POST','GET'])
def create_bill():
    database.createTable()
    return redirect(url_for('view_tables'))

@app.route('/view_tables', methods=['POST', 'GET'])
def view_tables():
    return render_template('bills.html', bills=database.showTablesList(),content='Bills')

@app.route('/view_tables/bills', methods=['POST', 'GET'])
def viewBills():
    req=request.form.get("action")
    rows = database.printBill(req)
    return render_template('invoice.html', rows=rows,bills=database.showTablesList(),content='Bills', total=database.total_amount(req))

if __name__ == '__main__':
    app.run(debug=True)
