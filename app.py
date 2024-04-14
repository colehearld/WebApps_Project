import os
from models import *
from auth import auth_bp
from config import Config
from flask import Flask, render_template, redirect, url_for, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required, current_user, UserMixin
from functools import wraps

basedir = os.path.abspath(os.path.dirname(__file__))

# create a Flask instance
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
app.register_blueprint(auth_bp)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function
    
@app.route('/', methods=['GET', 'POST'])
@login_required
def index():        
    return render_template('home.html')

@app.route('/profile', methods=['GET'])
@login_required
def profile():
    username = session['username']
    
    catches = Catch.query.join(User).filter(User.username == username).all()
    
    return render_template('profile.html', catches=catches)

@app.route('/addcatch', methods=['GET', 'POST'])
@login_required
def addcatch():
    username = session['username']
    
    if request.method == 'POST':
        fish_type = request.form.get('fish_type')
        weight = request.form.get('weight')
        length = request.form.get('length')
        lure = request.form.get('lure')
        location = request.form.get('location')
        
        if (fish_type == None or weight == None or length == None or
            lure == None or location == None):
            print('empty fields in catch form')
            return render_template('addcatch.html')
        else:        
            new_catch = Catch(fish_type=fish_type, weight=weight, length=length, lure=lure, location=location, user_username=username)
            print(new_catch)
            db.session.add(new_catch)
            db.session.commit()
            print('catch added!')
            print(new_catch)
            return render_template('addcatch.html')
    
    return render_template('addcatch.html')

@app.route('/discovery')
@login_required
def discovery():
    return render_template('discovery.html')

if __name__ == "__main__":
    #only run when initially setting up tables for the db
    # with app.app_context():
    #     db.drop_all()
    #     db.create_all()
    app.run(debug=True)