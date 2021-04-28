from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
import sqlite3 as sql

#conn = sql.connect('students.db')
#print("Opened database");

#conn.execute('CREATE TABLE students (name TEXT, major TEXT, studentid TEXT)')
#print("Table created");
#conn.close()

app = Flask(__name__)
Bootstrap(app)


@app.route("/")
def welcome_page():
    return render_template('welcome.html')

@app.route("/classes")
def class_list():
    return render_template('classes.html')

@app.route("/systemlogin")
def system_login():
    return render_template('login.html')

@app.route("/login", methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.form['nm']
        return redirect(url_for('success',name = user))
    else:
        user = request.args.get('nm')
        return redirect(url_for('success',name = user))

@app.route("/success/<name>")
def success(name):
    if name == 'admin':
        return render_template('admin.html', admin = name)
    if name == 'advisor':
        return render_template('advisor.html', advisor = name)
    else:
        return render_template('student.html', student = name)

@app.route("/addrec",methods = ['POST'])
def addrec():
    if request.method == "POST":
        name = request.form["nm"]
        classone = request.form["firstclass"]
        classtwo = request.form["secondclass"]

        with sql.connect("studentclass.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO classes (name, classone, classtwo) VALUES (?, ?, ?)", [name, classone, classtwo])
        con.commit()

        return '<html><body><a href="/list">View Class Selections</a></body></html>'

@app.route("/newstudent",methods = ['POST'])
def newstudent():
    if request.method == "POST":
        name = request.form["name"]
        major = request.form["major"]
        studentid = request.form["studentid"]

        with sql.connect("students.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO students (name, major, studentid) VALUES (?,?,?)", [name,major,studentid])
        con.commit()

        return '<html><body><a href="/users">View Current Students</a> * <a href="/success/admin">Return to Admin Panel</a></body></html>'

@app.route("/users")
def user_list():
    con = sql.connect("students.db")
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("SELECT * FROM students")

    rows = cur.fetchall();
    return render_template("users.html",rows = rows)

@app.route('/list')
def list_results():
    con = sql.connect("studentclass.db")
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("SELECT * FROM classes")

    rows = cur.fetchall();
    return render_template("selected.html",rows = rows)


@app.route("/info")
def help_page():
    return render_template('help.html')

if __name__ == '__main__':
    app.run(debug=True)
