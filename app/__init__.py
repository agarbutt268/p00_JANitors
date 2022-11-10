from flask import Flask, render_template, request, session, redirect
import sqlite3
import csv

DB_FILE="data.db"
db = sqlite3.connect(DB_FILE)
c = db.cursor()

command = 'create table users (username text, password text);'
c.execute(command)

app = Flask(__name__)    #create Flask object

app.secret_key = 'JANitors_@1'


@app.route("/", methods=['GET', 'POST'])
def starting():
    if 'username' in session:
        return render_template('home.html', user=our_username)
    return render_template('start.html')


@app.route("/REGISTER", methods=['GET', 'POST'])
def register():
    # to enter registered username and password into data.db
    our_username = request.form.get('register_username')
    our_password = request.form.get('register_pswd')
    command = "insert into user('" + our_username + "'," + our_password + ");"
    c.execute(command)
    return render_template('register.html')


@app.route("/LOGIN", methods=['GET', 'POST'])
def login():
    return render_template('login.html')


@app.route("/welcome", methods=['GET', 'POST'])
def logged_in():
    if request.form.get('user_name') == our_username and request.form.get('pswd') == our_password:
        session['username'] = request.form.get('user_name')
        return render_template('home.html', user=our_username)
    # wrong username and password
    elif request.form.get('user_name') != our_username and request.form.get('pswd') != our_password:
        error_msg = "No such user exists"
    # wrong username
    elif request.form.get('user_name') != our_username:
        error_msg = "Incorrect username"
    # wrong password
    elif request.form.get('pswd') != our_password:
        error_msg = "Incorrect password"
    return render_template('login.html', msg = error_msg)


@app.route("/logout", methods=['GET', 'POST'])
def logout():
    session.pop('username')
    return redirect("/")


if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True
    app.run()
