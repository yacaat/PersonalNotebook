from flask import Flask, render_template, redirect, url_for, request, session
import sqlite3
from datetime import datetime


app = Flask(__name__)

app.secret_key = b'xmZC11SnNhksPaVM'

@app.route('/')
def index():
    title = "Personel Notebook"
    login = False
    user = ''
    if 'admin' in session:
        login = True
        user = session['admin']
    return render_template('index.html', title=title, login=login, user=user)

@app.route('/test')
def test():
    title = "Personel Notebook"
    return render_template('test.html', title=title)

@app.route('/login', methods=['GET', 'POST'])
def login():
    title = "Personel Notebook"
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'admin':
            session[username] = username
            return redirect(url_for('index'))
        else:
            error = 'Invalid Credentials. Please try again.'
    return render_template('login.html', error=error, title=title)

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('admin', None)
    return redirect(url_for('index'))

@app.route('/rawitems', methods=['GET', 'POST'])
def rawitems():
    if request.method == 'POST':
        with sqlite3.connect("pn.db") as database:
            cursor = database.cursor()
            cursor.execute('insert into rawitems (item) values ("' + request.form['content'] + '")')
        return redirect(url_for('rawitems'))
    elif request.method == 'GET':
        title = "PN Raw Items"
        login = False
        user = ''
        items = []
        if 'admin' in session:
            login = True
            user = session['admin']
        with sqlite3.connect("pn.db") as database:
            cursor = database.cursor()
            cursor.execute("SELECT * FROM rawitems")
            rows = cursor.fetchall()
        for row in rows:
            items.append(row)
        return render_template('rawitems.html', title=title, login=login, user=user, items=items)

@app.route('/words', methods=['GET', 'POST'])
def words():
    if request.method == 'POST':
        with sqlite3.connect("pn.db") as database:
            cursor = database.cursor()
            print('insert into words (word, story) values ("' + request.form['word'] + '","' + request.form['story'] + '")')
            print(str(datetime.now())[:10])
            cursor.execute('insert into words (word, story, date) values ("' + request.form['word'] + '","' + request.form['story'] + '","' + str(datetime.now())[:10] + '")')
        return redirect(url_for('words'))
    elif request.method == 'GET':
        title = "PN Raw Items"
        login = False
        user = ''
        items = []
        if 'admin' in session:
            login = True
            user = session['admin']
        with sqlite3.connect("pn.db") as database:
            cursor = database.cursor()
            cursor.execute("SELECT * FROM words ORDER BY id DESC")
            rows = cursor.fetchall()
        for row in rows:
            items.append(row)
        return render_template('words.html', title=title, login=login, user=user, items=items)

@app.route('/delete/<int:id>')
def delete(id):
    if "rawitems" in request.referrer:
        with sqlite3.connect("pn.db") as database:
            print(request.referrer)
            cursor = database.cursor()
            cursor.execute('DELETE FROM rawitems WHERE id=' + str(id))
        return redirect(url_for('rawitems'))
    if "words" in request.referrer:
        with sqlite3.connect("pn.db") as database:
            print(request.referrer)
            cursor = database.cursor()
            cursor.execute('DELETE FROM words WHERE id=' + str(id))
        return redirect(url_for('words'))

@app.route('/_53')
def _53():
    title = "5-3 Stopwatch"
    login = False
    if 'admin' in session:
        login = True
        user = session['admin']
    return render_template('_53.html', title=title, login=login)
@app.route('/_94')
def _94():
    title = "9-4 Stopwatch"
    login = False
    if 'admin' in session:
        login = True
        user = session['admin']
    return render_template('_94.html', title=title, login=login)


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(host="0.0.0.0", threaded=True, port=5000)
