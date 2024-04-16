import os
from models import *
from auth import auth_bp
from config import Config
from flask import Flask, render_template, redirect, url_for, request, session, current_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from flask_login import login_required
from functools import wraps

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
    return redirect(url_for('profile'))

@app.route('/profile', methods=['GET'])
@login_required
def profile():
    username = session['username']
    
    catches = Catch.query.join(User).filter(User.username == username).all()
    
    return render_template('profile.html', username=username, catches=catches)

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
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')
        
        image_file = request.files['image']
        
        upload_directory = os.path.join('static', 'images')

        os.makedirs(upload_directory, exist_ok=True)

        image_path = os.path.join(upload_directory, image_file.filename)
        image_file.save(image_path)
            
        new_catch = Catch(
            fish_type=fish_type, 
            weight=weight, 
            length=length, 
            lure=lure, 
            location=location, 
            latitude=latitude, 
            longitude=longitude, 
            image=image_path, 
            user_username=username
        )
        db.session.add(new_catch)
        db.session.commit()        
        print('catch added!')
        print(new_catch)
    
    return render_template('addcatch.html')

@app.route('/discovery')
@login_required
def discovery():    
    top_5_catches = Catch.query.order_by(desc(Catch.weight)).limit(5).all()
    return render_template('discovery.html', top_catches=top_5_catches)

@app.route('/delete-catch', methods=['POST'])
def delete_catch():
    catch_id = request.form.get('catchId')
    if catch_id is None:
        return print('error: Catch ID is required, 400')

    delete_catch = Catch.query.filter_by(catch_id=catch_id).first()
    
    if delete_catch:
        db.session.delete(delete_catch)
        db.session.commit()
        print(str(delete_catch) + ' deleted')
        return render_template('profile.html')
    else:
        return 'error: Catch not found', 404

if __name__ == "__main__":
    # only run when initially setting up tables for the db
    with app.app_context():
        db.drop_all()
        db.create_all()
    app.run(debug=True)