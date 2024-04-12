from flask import Flask, render_template, redirect, url_for, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required, current_user, UserMixin
from functools import wraps
import os

basedir = os.path.abspath(os.path.dirname(__file__))

# create a Flask instance
app = Flask(__name__)
app.config['SECRET_KEY'] = 'this_is_the_secret_key'

# define SQLAlchemy URL, a configuration parameter
app.config['SQLALCHEMY_DATABASE_URI'] =\
'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# The db object instantiated from the class SQLAlchemy represents the database and
# provides access to all the functionality of Flask-SQLAlchemy
db = SQLAlchemy(app)

# create tables for db
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    username = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.String(20))
    
    catches = db.relationship('Catch', backref='user')
    
    def __repr__(self):
        return '<User %r>' % self.username

class Catch(db.Model):
    __tablename__ = 'catches'
    
    catch_id = db.Column(db.Integer, primary_key=True)
    fish_type = db.Column(db.String(20))
    weight = db.Column(db.Double)
    length = db.Column(db.Double)
    lure_used = db.Column(db.String(20))
    location = db.Column(db.String(20))
    
    user_username = db.Column(db.String(20), db.ForeignKey('users.username'))
    
    def __repr__(self):
        return '<Catch %r>' % self.catch_id
    
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function
    
@app.route('/', methods=['GET', 'POST'])
@login_required
def index():        
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == None or password == None:
            return redirect(url_for('login'))
                
        user = User.query.filter_by(username=username).first()
        
        if user:
            if user.password == password:
                session['username'] = username
                print('successful login')
                print(session['username'])
                return redirect(url_for('profile'))
            else:
                print('incorrect password')
                return redirect(url_for('login'))          
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        
        user = User.query.filter_by(username=username).first()
        if user:
            print('username is taken')
        elif password1 != password2:
            print('passwords do not match')
        else:
            new_user = User(username=username, password=password1)
            db.session.add(new_user)
            db.session.commit()
            print('user created!')
            session['username'] = username
            return render_template('profile.html')
        
    return render_template('signup.html')

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@app.route('/addcatch')
@login_required
def addcatch():
    return render_template('addcatch.html')

@app.route('/discovery')
@login_required
def discovery():
    return render_template('discovery.html')

if __name__ == "__main__":
    # only run when initially setting up tables for the db
    # with app.app_context():
    #     db.create_all()
    app.run(debug=True) 