from flask import Flask, render_template, request, redirect, url_for, session
# from flaskext.mysql import MySQL
# from os import urandom

app = Flask('__name__')
app.secret_key = b'ae604a27b0fa8d69430479e12688d2781f1fe8a568ddaabd45c1990acd2b1a9c'

# # MySQL Config
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'xovert'
# app.config['MYSQL_PASSWORD'] = 'password'
# app.config['MYSQL_DB'] = 'project'

# mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)