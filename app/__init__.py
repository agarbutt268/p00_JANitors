from flask import Flask, render_template, request, session, redirect
import sqlite3
import csv

DB_FILE="data.db"
db = sqlite3.connect(DB_FILE)
c = db.cursor()

c.execute("DROP TABLE if exists users")
command = 'CREATE TABLE users (username TEXT, password TEXT);'
c.execute(command)

c.execute("DROP TABLE if exists stories")
command = 'CREATE TABLE stories (title TEXT, content TEXT, author TEXT);'
c.execute(command)

c.execute("DROP TABLE if exists newest")
command = 'CREATE TABLE newest (title TEXT, content TEXT, author TEXT);'
c.execute(command)

db.commit()

app = Flask(__name__)    #create Flask object

app.secret_key = 'JANitors_@1'

#==========================pages============================

@app.route("/", methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect("/welcome")#render_template('home.html', user=session['username'])
    return render_template('login.html')


@app.route("/start", methods=['GET', 'POST'])
def starting():
    return render_template('start.html')


@app.route("/register", methods=['GET', 'POST'])
def registered():
    # to enter registered username and password into data.db
    our_username = request.form.get('register_username')
    our_password = request.form.get('register_pswd')

    # need to add this because if we don't we get a programming error that says it's not in the same thread
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute("SELECT * FROM users;")
    user_info = c.fetchall()
    for user in user_info:
        if our_username == user[0]:
            return render_template('register.html', status="invalid username")
    #c.execute("INSERT INTO users VALUES (?,?);"), (our_username, our_password)
    c.execute("INSERT INTO users VALUES ('" + our_username + "', '" + our_password + "');")
    db.commit()

    #c.execute(f"INSERT INTO users VALUES ('{our_username}' , '{our_password}')")
    return render_template('register.html', status="registered! Go login!")


@app.route("/welcome", methods=['GET', 'POST'])
def logged_in():
    if 'username' in session:
        return render_template('home.html', user=session['username'])

    u = request.form.get('user_name')
    p = request.form.get('pswd')

    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute("SELECT * FROM users")
    user_info = c.fetchall()
    for user in user_info:
        if u == user[0] and p == user[1]:
            session['username'] = u
            return render_template('home.html', user=u)
        if u == user[0] and p != user[1]:
            return render_template('login.html', status="wrong password")
    return render_template('login.html', status="user does not exist")


@app.route("/create", methods=['GET', 'POST'])
def create_story():
    return render_template('create.html')


@app.route("/create-response-page", methods=['GET', 'POST'])
def add_story():
    story_title = request.form.get('story_name')
    story_content = request.form.get('new_story')
    story_author = session['username']

    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    #add story information to database
    command = "INSERT INTO stories VALUES ('" + story_title + "', '" + story_content + "', '" + story_author + "');"
    c.execute(command)
    c.execute("INSERT INTO newest VALUES ('" + story_title + "', '" + story_content + "', '" + story_author + "');")
    db.commit() #need this line for stories to be saved
    return render_template('createresponse.html', title = story_title, content = story_content, author = story_author)


# to add to an existing story
@app.route("/edit", methods=['GET', 'POST'])
def edit_story():
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("SELECT * FROM newest")
    all_stories = c.fetchall()
    str = ""
    for story in all_stories:
        if (story[2] != session['username']):
            str += story[0] + ": " + story[1] + "------->"
    db.commit()
    return render_template('edit.html', stories=str)


# after adding on to an existing story
@app.route("/edit-response-page", methods=['GET', 'POST'])
def edit_success():
    edit_title = request.form.get('edit_name')
    edit_content = request.form.get('adding_on')
    edit_author = session['username']

    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute("SELECT * FROM newest")
    all_stories = c.fetchall()
    str = ""
    for story in all_stories:
        if story[0] == edit_title:
            c.execute("DELETE FROM newest WHERE title=?", [edit_title])

    command = "INSERT INTO stories VALUES ('" + edit_title + "', '" + edit_content + "', '" + edit_author + "');"
    c.execute(command)

    db.commit()
    return render_template('editresponse.html', title=edit_title, content=edit_content, author=edit_author)


@app.route("/view", methods=['GET', 'POST'])
def view_edits():
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("SELECT * FROM stories")
    all_stories = c.fetchall()
    str1 = ""
    for story in all_stories:
        if story[2] == session['username']: # CHECK THIS PARTTTTTTT
            str1 += story[0] + ': ' + story[1] + "------>"
    return render_template('view.html', your_edits=str1)


@app.route("/logout", methods=['GET', 'POST'])
def logout():
    session.pop('username')
    return redirect("/")


if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True
    app.run()

db.commit()
db.close()