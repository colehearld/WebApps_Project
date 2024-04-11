from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/addcatch')
def addcatch():
    return render_template('addcatch.html')

@app.route('/discovery')
def discovery():
    return render_template('discovery.html')

if __name__ == "__main__":
    app.run(debug=True)