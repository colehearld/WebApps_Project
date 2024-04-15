from flask import Blueprint, render_template, redirect, url_for, request, session
from models import User, db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
                
        user = User.query.filter_by(username=username).first()
        
        if user:
            if user.password == password:
                session['username'] = username
                print('successful login user: ' + session['username'])
                return redirect(url_for('profile'))
            else:
                print('incorrect password')
                return redirect(url_for('auth.login'))          
    
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('auth.login'))

@auth_bp.route('/signup', methods=['GET', 'POST'])
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
            print('user: ' + username + ' created!')
            session['username'] = username
            return redirect(url_for('profile'))
        
    return render_template('signup.html')