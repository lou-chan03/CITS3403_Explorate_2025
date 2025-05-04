from app import app
from flask import render_template

@app.route('/')
def home():
    return render_template('Data_Entry.html')  # Replace 'index.html' with your main HTML file name
@app.route('/adventure')
def adventure():
    return render_template('Adv_name.html')  # This assumes the file is in the `templates/` directory
@app.route('/questions')
def questions():
    return render_template('Data_Ent_Q1.html')  # This assumes the file is in the `templates/` directory
@app.route('/email_share')
def email_share():
    return render_template('email_share.html')