import os
from flask import Flask, url_for, render_template, request, flash, redirect, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from reddit import Reddit
from memecl import Memes
from registration_form import *

'''
This class uses the User, 
, Meme and Category classes 
to render the user and category pages.

This is done using a Flask app. Read more about Flask here:
http://flask.pocoo.org/

'''

app = Flask('Memes')

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
db = SQLAlchemy(app)

from userClass import *
from categoryClass import *

# Number of posts to render

NUM_POSTS = 100

def init_category(name):
    '''
    Creates a new category object which points to the category with
    the specified name.

    @param: the name of the category
    @return: Category object pointing to given category
    '''
    return Category(name)

def init_user(name):
    '''
    Creates a new public user object which points to the user with
    the specified name.

    @param: the name of the user
    @return: PublicUser object pointing to a given user 
    '''
    return User(name)

def get_category(category):
    '''
    Gets the information from the specified public category object.

    @param: Category object representing the target category
    @return: a 2D parallel list: [img_urls, titles, scores, authors]
    '''
    
    # initializes the reddit praw wrapper
    reddit = Reddit(category.subreddit, NUM_POSTS)

    # gets the data from reddit
    img_urls = reddit.getImageUrl()
    titles = reddit.getTitle()
    scores = reddit.getScore()
    authors = reddit.getAuthor()

    return [img_urls, titles, scores, authors]

def get_user(user):
    '''
    Gets the information from the specified public user object.

    @param: the PublicUser object that points to the target user
    @return: a 2D parallel list: [img_urls, titles, scores, authors]
    '''
    # initializes the reddit praw wrapper
    reddit = Reddit(user.returnSubreddit()[2], NUM_POSTS)

    # gets the data from reddit
    img_urls = reddit.getImageUrl()
    titles = reddit.getTitle()
    scores = reddit.getScore()
    authors = reddit.getAuthor()

    return [img_urls, titles, scores, authors]

def createUser(username, password, first_name, second_name):
    '''
    Creates a new User and adds it to the database.

    @param Username, Password, first and last name for the User.
    '''

    #Creates new User
    user = Users(username = username, password = password, first_name = first_name, second_name = second_name, bio = None, picture = None, age = None, education = None, geography = None, subreddit = None)
    
    #Adds it to the database.
    db.session.add(user)
    db.session.commit()

@app.route('/')
def index():
    '''
    Renders the index page.

    @return: html of index page
    '''
    return render_template('index.html')

# user home page
# @app.route('/users')

# def user():
# 	name = request.args.get('user')
# 	user = User(name)
# 	[urls, titles, scores, authors] = get_user(user)
# 	return render_template('category_page.html',name=name, img_1_url=urls[0], img_2_url=urls[1], img_3_url=urls[2], source_img="content/reddit_logo.png")

# user profile
@app.route('/profile')
def user():
    if 'username' not in session:
        return redirect(url_for('login_page'))

    return redirect(url_for('profile', username=session['username']))

@app.route('/users/<username>')
def profile(username):
    return render_template('profile.html')

@app.route('/users/123/user_edit_name', methods=['GET','POST'])
def user_edit_name():

    return

@app.route('/signout')
def signout():
 
  if 'username' not in session:
    return redirect(url_for('login_page'))
     
  session.pop('username', None)
  session.pop('first', None)
  return redirect(url_for('index'))

def public_user_page():
    '''
    Renders the user page.

    @return: html of index page with image URLs
    '''

    # Gets the target category from the URL
    name = request.args.get('user')

    # Initializes the PublicUser object
    user = init_user(name)
    
    # Gets the data from the API
    [img_urls, titles, scores, authors] = get_user(user)

    return render_template('category_page.html', name=name,
    img_1_url=img_urls[0], img_2_url=img_urls[1], img_3_url=img_urls[2],
    source_img="content/reddit_logo.png")


@app.route('/category')

def category_page():
    '''
    Renders the category page.

    @return: html of cateogry page with image URLs
    '''

    # Gets the target category from the URL
    name = request.args.get('cat')

    # Initializes the PublicUser object
    category = init_category(name)
    
    # Gets the data from the API
    [img_urls, titles, scores, authors] = get_category(category)

    return render_template('category_page.html', numPost=range(NUM_POSTS), name=name, 
        img_urls=img_urls, titles=titles, scores=scores, authors=authors,
        source_img="static/content/reddit_logo.png")

#Login the user
@app.route('/login', methods=['GET','POST'])

def login_page():
    '''
    Allow the user to login onto their account

    @return html of home page if it works, returns login page if it fails.
    '''


    if request.method == 'GET':
        return render_template('loginPage.html')

    if request.method == 'POST':
        username = request.form['user']
        psw = request.form['password']
        error = None
        #Check to see if the username is in the database.
        if Users.query.filter(Users.username==username).all() != []:

            #Checks if password entered matches the password the user entered.
            if(Users.query.filter(Users.username==username).all()[0].password == psw):
                return render_template('profile.html')
            else:
                return render_template('loginPage.html', error =  'Invalid Password')
        else:
            return render_template('loginPage.html', error =  'Invalid Username')

    return render_template('loginPage.html')

#Sign up a User
@app.route('/login/signup', methods=['GET', 'POST'])

def register():
    '''
    Allow a person to Register an account

    @return home page if it works, return the signup page if it doesn't.
    '''


    if request.method == 'GET':
        return render_template('form.html')

    if request.method == 'POST':

        #Checks to see if username is not unique in database, return signup page if it is not unique.
        username = request.form['username']
        usernames = db.session.query(Users.username)
        for listOfUsernames in usernames:
            if(username in listOfUsernames):
                return render_template('form.html', error = 'Username already taken.')

        #If username is unique, add it to database.
        first = request.form['fname']
        last = request.form['lname']
        email = request.form['email']
        password = request.form['password']
        password2 = request.form['password2']

        if (password != password2):
            return render_template('form.html', error = 'Passwords do not match')

        createUser(username,password,first,last)

        session['username'] = username
        session['first'] = first
        session['second'] = last
        session['email'] = email
        return render_template('index.html')

if __name__ == '__main__':
    app.secret_key = 'blah'
    app.run(debug=True)

from userClass import *
from categoryClass import *
