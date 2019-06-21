from flask import Flask, request, render_template, redirect, url_for, session, flash
from sys import argv
from random import choice, random
import string
from uuid import uuid4
uuid = uuid4
from ServerSideSession import VolatileServerSideSessionInterface

app = Flask(__name__)
app.session_interface = VolatileServerSideSessionInterface()

users = {
        'user': 'pass'
        }

articles = [
        (1, 'A'),
        (2, 'B'),
        (3, 'C')
        ]
max_notes = 3

def isLoginSession():
    return 'user' in session

def newCSRFToken():
    session['csrftoken'] = "".join([choice(string.ascii_letters) for i in range(32)])

def CSRFValidation():
    try:
        sessionToken = session['csrftoken']
        newCSRFToken()
        return sessionToken == request.form['csrftoken']
    except:
        return False

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/login', methods=['POST', 'GET'])
def login():
    if isLoginSession():
        return redirect(url_for('home'))

    if request.method == 'GET':
        return render_template("login.html")
    elif request.method == 'POST':
        username = request.form['user']
        try:
            password = users[username]
        except KeyError:
            return render_template("login.html", message="User " + username + " unknown!")

        if password == request.form['pass']:
            session['user'] = username
            newCSRFToken()
            if 'redirectto' in request.form:
                return redirect(url_for(request.form['redirectto']))
        else:
            return render_template("login.html", message="Login failed!")

@app.route('/logout')
def logout():
    session.clear()
    return render_template("login.html", message="Succesfully logged out.")

@app.route('/CSRFProtected', methods=['POST', 'GET'])
def CSRFProtection():
    if not isLoginSession():
        return redirect(url_for('login', redirectto='CSRFProtection'))

    if request.method == 'GET':
        return render_template("CSRFForm.html")
    elif request.method == 'POST':
        if not CSRFValidation():
            return render_template("message.html", message="CSRF validation failed!")
        else:
            return render_template("CSRFShow.html")

@app.route('/ProbabilisticLogout', methods=['POST', 'GET'])
def ProbabilisticLogout():
    if not isLoginSession():
        return redirect(url_for('login', redirectto='ProbabilisticLogout'))

    if request.method == 'GET':
        return render_template("ProbForm.html", fields=list(string.ascii_lowercase))
    elif request.method == 'POST':
        if random() < 0.2:
            return logout()
        else:
            if CSRFValidation():
                return render_template("ProbShow.html", fields=list(string.ascii_lowercase))
            else:
                return render_template("message.html", message="CSRF validation failed!")

@app.route('/Workflow/<int:step>', methods=['POST', 'GET'])
def Workflow(step):
    if not isLoginSession():
        return redirect(url_for('login', redirectto='ProbabilisticLogout'))

    if 'step' not in session:
        session['step'] = 1
    if session['step'] < step:
        return render_template("message.html", message="Workflow request doesn't matches workflow state!")
    if session['step'] != step:
        session['step'] = step 

    if request.method == 'GET':
        return render_template("Workflow-Step{}.html".format(step), articles=articles)
    elif request.method == 'POST':
        if not CSRFValidation():
            return render_template("message.html", message="CSRF validation failed!")

        if step < 4:
            for param in request.form:
                session['wf_' + param] = request.form[param]
            session['step'] += 1
            return redirect(url_for('Workflow', step=session['step']))
        else:
            session['step'] = 1
            return render_template("message.html", message="Thanks for your order! It will be delivered soon!")

@app.route('/Notes', methods=['POST', 'GET'])
def Notes():
    if not isLoginSession():
        return redirect(url_for('login', redirectto='Notes'))

    if 'notes' not in session:
        session['notes'] = dict()

    if request.method == 'GET':
        pass
    if request.method == 'POST':
        if request.form['action'] == 'add':
            if len(session['notes']) >= max_notes:
                flash("No more notes allowed!")
            else:
                note = { 'subject': request.form['subject'], 'content': request.form['content'] }
                session['notes'][str(uuid())] = note
                flash("Note was added")
        if request.form['action'] == 'delete':
            nid = request.form['id']
            if nid in session['notes']:
                subject = session['notes'][nid]['subject']
                del session['notes'][nid]
                flash("Note '%s' deleted" % (subject))
            else:
                flash("Note with id '%s' doesn\'t exists" % nid)

    return render_template("notes.html", notes=session['notes'])

if __name__ == '__main__':
    try:
        listen_addr = argv[1]
    except IndexError:
        listen_addr = '127.0.0.1'
    app.run(host=listen_addr, port=8001, debug=False)
