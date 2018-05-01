from app import app
from flask import Flask, render_template, request

#app = Flask(cadenza)

@app.route('/')
@app.route('/music_page')
# def index():
#     return "Hello, World!"

# @app.route('/sheet', methods=['GET', 'POST'])
# def sheet():
#     notes = "tabstave notation=true tablature=false"
#     return render_template('musicpage.html')



# def render(cadenza, template_folder = 'musicpage.html'):
#     # insert here



# Reads the HTML from "musicpage.html" and processes it to render the music editor.
@app.route('/')
def music_page():
    return render_template('musicpage.html', notes="")

# Requests the text that is inputted by the user to be formatted into notes.
@app.route('/', methods=['POST'])
def music_page_post():
    text = request.form['text']
    processed_text = text.upper()
    return render_template('musicpage.html', notes=processed_text)