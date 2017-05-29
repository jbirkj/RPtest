# Blog.py - controller

# imports
from flask import Flask, render_template, request, session, flash, redirect, url_for, g
from functools import wraps
from flask_sqlalchemy import SQLAlchemy

from flask.ext.heroku import Heroku

app = Flask(__name__)

#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/localdb3'
heroku = Heroku(app)
db = SQLAlchemy(app)

class Posts(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True)
    post = db.Column(db.String(120), unique=True)

    def __init__(self, title, post):
        self.title = title
        self.post = post

    def __repr__(self):
        return '<title %r, post %r >' % (self.title, self.post)


# configuration
USERNAME = 'a'
PASSWORD = 'a'
SECRET_KEY = ''

# pulls in configurations by looking for UPPERCASE variables
app.config.from_object(__name__)

def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to log in first.')
            return redirect(url_for('login'))
    return wrap

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    status_code = 200
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME'] or request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid Credentials. Please try again.'
            status_code = 401
        else:
            session['logged_in'] = True
            return redirect(url_for('main'))
    return render_template('login.html', error=error), status_code

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('login'))

@app.route('/main')
@login_required
def main():
    posts = Posts.query.all()
    return render_template('main.html', posts=posts)

@app.route('/add', methods=['POST'])
@login_required
def add():
    title = request.form['title']
    post = request.form['post']
    if not title or not post:
        flash("All fields are required. Please try again.")
        return redirect(url_for('main'))
    else:
        p1 = Posts(request.form['title'], request.form['post'])
        db.session.add(p1)
        db.session.commit()
        flash('New entry was successfully posted!')
        return redirect(url_for('main'))


if __name__ == '__main__':
    app.run(debug=True)
