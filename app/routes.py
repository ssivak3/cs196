from flask import render_template, flash, request, redirect, url_for
from app import app
from app.forms import LoginForm
from app.forms import SignUpForm
from app.forms import createScore
import json

# class User(object):
#     def __init__(self, email, username, password):
#         self.email  = email
#         self.username = username
#         self.password = password
#
#     def createUser(email, username, password):
#         user = User(email = email, username = username, password = password)
#         #json.dumps(user.__dict__)

#function to retrieve a specific user
def get_user(username):
    all_users = get_all_users()
    current_user = None
    print(username)
    for user in all_users:
        print(user['username'])
        if (user['username'] == username):
            current_user = user
            break
    return current_user
#function to read json file containg user data
def get_all_users():
    users = None
    with open('/Users/sandhyasivakumar/cs196/app/data.json') as jsonfile:
        users = json.load(jsonfile)
    return users
#function to create user and write information into json file
def make_user(email, username, password):
    #user = User(email, username, password)
    new_user = {'email' : email, 'username' : username, 'password' : password}
        #json.dumps(user)
    users = get_all_users()
    users.append(new_user)
    json_string = json.dumps([user for user in users])
    file = open("/Users/sandhyasivakumar/cs196/app/data.json", "w")
    print(json_string)
    file.write(json_string)
    return new_user
#function to verify that username matches password
def verify_user(username, password):
    user = get_user(username)
    if username == user['username'] and password == user['password']:
        return True
    else:
        return False
#function to get scores associated with a username
def get_scores(username):
    scores = None
    with open('/Users/sandhyasivakumar/cs196/app/scores.json') as jsonfile:
        scores = json.load(jsonfile)
    return scores
        #for score in scores:
#function to create a score for a user
def make_score(title, composer, timesignature):
    new_score = {'title' : title, 'composer' : composer, 'timesignature' : timesignature}
    scores = get_scores()
    scores.append(new_score)
    json_score = json.dumps([score for score in scores])
    file = open("/Users/sandhyasivakumar/cs196/app/scores.json", "w")
    print(json_score)
    file.write(json_score)
    return new_score

#routes
@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'bob',
            'password': 'xxxx'
            'email: bob@email.com'
            }
    posts = [
        {
            'author': {'username': 'mr. bean'},
            'body': 'zelda theme music'
        },
        {
            'author': {'username': 'winnie the pooh'},
            'body': 'summertime'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'GET':
        return render_template('login.html')
    #if request.method == 'POST':
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    if verify_user(form.username.data, form.password.data) == False:
        flash('USERNAME AND PASSWORD DO NOT MATCH')
    user = get_user(form.username.data)
    return render_template('createscore.html', title='Sign In', form=form, user=user)

@app.route('/login/signup', methods=['GET', 'POST'])
def registerUser():
    form = SignUpForm()
    if request.method == 'GET':
        return render_template('signup.html')
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        print('Did i reach here2?')
        user = make_user(email = email, username = username, password = password)
        return render_template('createscore.html', title='Sign In', form=form, user=user)

@app.route('/createscore', methods=['GET', 'POST'])
def createscore():
    form = createScore()
    if request.method == 'GET':
        return render_template('createscore.html')
    if request.method == 'POST':
        title = request.form['title']
        composer = request.form['composer']
        timesignature = request.form['timesignature']
        score = make_score(title = title, composer = composer, timesignature = timesignature)
        return render_template('music.html', title='new score', form=form, user=user)

@app.route('/login/music.html', methods=['GET', 'POST'])
def getMusic():
    if request.method == 'GET':
        return render_template('music.html')
    if request.method == 'POST':
        return render_template('music.html')

@app.route('/music.html', methods=['GET', 'POST'])
def plsgetmusic():
    if request.method == 'GET':
        return render_template('music.html')
    if request.method == 'POST':
        return render_template('music.html')
