from flask import Flask, render_template, request, redirect, url_for
import database

app = Flask(__name__)
nrcount = 0
flag = False
grab = None
user = ""
company_details = {}
customer_details = []
cid = 1
cust_count = 0
customers = []

@app.route('/')
def launch():
    return render_template('login.html')

@app.route('/form_login', methods=['POST', 'GET'])
def authenticate():
    global temp_tname, flag, company_details, customer_details, user, cust_count, customers
    if not flag:
        user = request.form["username"]
        passwd = request.form["password"]
        if database.establishConnection(user, passwd) == 1:
            flag = True
            with open('{}_comp.txt'.format(user), 'r') as f:
                company_details = eval(f.read())
            with open('{}_cust.txt'.format(user), 'r') as f:
                l = f.readlines()
                for i in l:
                    k = eval(i)
                    customer_details.append(k)
                    cust_count  += 1
                    customers.append(k['cid'])
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', status="Invalid Credentials")
    else:
        return redirect(url_for('dashboard'))

@app.route('/dashboard', methods=['POST', 'GET'])
def dashboard():
    if flag:
        return render_template("home.html")
    else:
        return "YOU HAVE BEEN LOGGED OUT"
@app.route('/modify_bill', methods=['POST','GET'])
def modify_bill():
    global temp_tname, cust_count, cid
    if flag:
        bills = database.showTablesList(cid)
        rows = []
        col_names = []
        if bills:
            temp_tname = bills[0]
            rows = database.printBill(temp_tname)
            col_names = database.col_names(temp_tname)
            col_names.remove('id')
        return render_template('modifybills.html', rows=rows, bills=database.showTablesList(cid), content='Bills', col_names = col_names, visibilty="wrapper", size=nrcount,  cust = [x for x in customers])
    else:
        return "YOU HAVE BEEN LOGGED OUT"
@app.route('/new_tbl')
def new_tbl():
    if flag:
        database.createTable(cid)
        return redirect(url_for('modify_bill'))
    else:
        return "YOU HAVE BEEN LOGGED OUT"
@app.route('/view_tables', methods=['POST', 'GET'])
def view_tables():
    global grab, temp_tname
    if flag:
        grab = None
        bills = database.showTablesList(cid)
        temp_tname = bills[0]
        return render_template("invoice.html", bills=bills, content='Bills', stat="hidden",
                               gal="visible", temp1="hidden", temp2="hidden", company_details=company_details,
                               customer_details=customer_details)
    else:
        return "YOU HAVE BEEN LOGGED OUT"

@app.route('/view_tables/bills', methods=['POST', 'GET'])
def viewBills():
    global temp_tname
    if flag:
        temp_tname = request.form.get("action")
        return redirect(url_for("template"))
    else:
        return "YOU HAVE BEEN LOGGED OUT"


@app.route('/view_tables/template', methods=['POST', 'GET'])
def template():
    global grab, cid
    rows = database.printBill(temp_tname)
    total = database.total_amount(temp_tname)
    if grab is None:
        grab = request.form.get("temp")
    if flag and grab is not None:
        if grab == "template1":
            return render_template('invoice.html', rows=rows,bills=database.showTablesList(cid),content='Bills',total=total, tax=0.18*total,final=total+0.18*total ,temp1="visible",temp2="hidden",gal = "hidden", company_details = company_details, customer_details = customer_details)
        if grab == "template2":
            return render_template('invoice.html', rows=rows, bills=database.showTablesList(cid), content='Bills',
                                   total=total, tax=0.18 * total, final=total + 0.18 * total, temp2="visible",temp1="hidden",gal = "hidden",company_details = company_details, customer_details = customer_details)
    elif flag:
        return render_template("invoice.html", bills=database.showTablesList(cid),content='Bills',stat="hidden",gal = "visible",temp1="hidden",temp2="hidden", company_details = company_details, customer_details = customer_details)
    else:
        return "YOU HAVE BEEN LOGGED OUT"

@app.route('/table_name', methods=['POST', 'GET'])
def vBills():
    if flag:
        global temp_tname, cid
        bills = database.showTablesList(cid)
        if bills:
            col_names = database.col_names(bills[0])
            rows = database.printBill(bills[0])
            col_names.remove('id')
            visibility = 'wrapper'

        else:
            return render_template('modifybills.html', rows=[], bills=bills, content='Bills', col_names=[],
                                   visibilty='invisible', size=nrcount, cust=[x for x in customers])

        if request.form.get("cust_id"):
            cid = request.form.get("cust_id").strip('#')
            return redirect(url_for('vBills'))

        if request.form.get("action"):
            temp_tname = request.form.get("action")
            rows = database.printBill(temp_tname)
            col_names = database.col_names(temp_tname)
            col_names.remove('id')
        return render_template('modifybills.html', rows=rows, bills=bills, content='Bills', col_names = col_names, visibilty=visibility, size=nrcount, cust = [x for x in customers])
    else:
        return "YOU HAVE BEEN LOGGED OUT"
@app.route('/modify_table', methods=['POST', 'GET'])
def modify_bills():
    if flag:
        global nrcount, temp_tname, cid
        if request.method == 'POST':
            if request.form.get("plus") == '+':
                nrcount += 1
            elif request.form.get("minus") == '-':
                nrcount -= 1
            elif request.form.get("action1") == "Remove":
                database.remove_table(temp_tname)
                return redirect(url_for("modify_bill"))
            else:
                c = database.modify(temp_tname, request.form)
                nrcount -= c
        rows = database.printBill(temp_tname)
        col_names = database.col_names(temp_tname)
        col_names.remove('id')
        return render_template('modifybills.html', rows=rows, extras=[i for i in range(nrcount)], bills=database.showTablesList(cid), content='Bills', col_names = col_names, size=nrcount, visibilty="wrapper")
    else:
        return "YOU HAVE BEEN LOGGED OUT"

@app.route('/remove_row',methods=['POST', 'GET'])
def rem_row():
    if flag:
        global temp_tname, cid
        value = list(dict(request.form).values())[0]
        if value == "x":
            database.remove_row(temp_tname,request.form)
            rows = database.printBill(temp_tname)
            col_names = database.col_names(temp_tname)
            col_names.remove('id')
            return render_template('modifybills.html', rows=rows, bills=database.showTablesList(cid), content='Bills', col_names = col_names, visibilty="wrapper", size=nrcount)
    else:
        return "YOU HAVE BEEN LOGGED OUT"

@app.route('/signout')
def sign_out():
    global flag
    database.signout()
    flag = False
    return redirect(url_for('launch'))

@app.route('/comp_info', methods=['POST', 'GET'])
def cmp_info():
    if flag:
        global user, company_details
        data = request.form
        if data.get("submit"):
            with open("{}_comp.txt".format(user),"w") as f:
                f.write(str(dict(data)))
                company_details = dict(data)
                return redirect(url_for("dashboard"))
        return render_template("comp_info.html", cmp_det = company_details)
    else:
        return "YOU HAVE BEEN LOGGED OUT"

@app.route('/customer', methods = ['POST', 'GET'])
def customer():
    if flag:
        global user, customer_details, cid, cust_count, customers
        c_det = customer_details[0]
        data = request.form

        if data.get('action'):
            cust_count += 1
            cid = cust_count

            c_det = {'cid': cust_count, 'firstname': 'unnamed', 'lastname': '', 'email': '', 'phone': '', 'address': '', 'state': '', 'country': '', 'post': '', 'area': ''}

        if data.get('choose'):
            id = data.get("choose").strip('#')
            for i in customer_details:
                if i['cid'] == id:
                    cid = id
                    c_det = i
                    break
        if data.get('delete'):
            with open("{}_cust.txt".format(user), "w") as f:
                for i in customer_details:
                    if i['cid'] != cid:
                         f.write(str(i)+"\n")
                    else:
                         key = customer_details.index(i)
                         customer_details.pop(key)
                         customers.remove(i['cid'])
        if data.get("submit"):
            k = dict(data)
            with open("{}_cust.txt".format(user), "w") as f:
                 for i in customer_details:
                     if i['cid'] != cid:
                         f.write(str(i)+"\n")
                     else:
                         f.write(str(k)+"\n")
                         customer_details[customer_details.index(i)] = k
                 if k['cid'] not in customers:
                    f.write(str(k)+"\n")
                    customers.append(k['cid'])
                    customer_details.append(k)

            return redirect(url_for("dashboard"))
        return render_template("customer.html", cus_det=c_det, cust = [x for x in customers])
    else:
        return "YOU HAVE BEEN LOGGED OUT"

@app.route('/customers', methods = ['POST', 'GET'])
def choose_cust():
    if flag:
        global cid
        bills = database.showTablesList(cid)
        temp_tname = bills[0]
        rows = database.printBill(temp_tname)
        col_names = database.col_names(temp_tname)
        col_names.remove('id')

        return render_template('modifybills.html', rows=rows, bills=database.showTablesList(cid), content='Bills', col_names = col_names, visibilty="wrapper", size=nrcount)
    else:
        return "YOU HAVE BEEN LOGGED OUT"

if __name__ == '__main__':
    app.run(debug=True)
