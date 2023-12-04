from flask import render_template
from airpol import airpol


@airpol.route('/')
def initial():
    return render_template('initial_page.html')

@airpol.route('/index')
def index():
    # This is where you'll call your AI model and pass the results to the template
    # Replace this with your AI model logic
    return render_template('index.html')
