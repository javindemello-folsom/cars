from flask import Flask, render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.user_model import User
from flask_app.models.car_model import Car
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/register', methods=["POST"])
def register():
    # Create session variables for register form here
    if not User.validate_user(request.form):
        return redirect('/')
    session.clear()
    
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    
    data = {
        "fname": request.form['fname'],
        "lname": request.form['lname'],
        "email": request.form['email'],
        "password" : pw_hash
    }
    user_id = User.save(data)
    session['user_id'] = user_id 
    session['fname'] = data['fname']
    session['lname'] = data['lname']
    
    return redirect("/dashboard")


@app.route('/login', methods=["POST"])
def login():
    data = { "email" : request.form["email"] }
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash(u"Invalid Email/Password","login")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash(u"Invalid Email/Password","login")
        return redirect('/')
    session['user_id'] = user_in_db.id
    session['fname'] = user_in_db.first_name
    return redirect("/dashboard")


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    cars = Car.get_all()
    print(session['user_id'])
    return render_template('dashboard.html', user = User.get_one(session['user_id']) , all_cars = cars)

@app.route('/user/<int:user_id>')
def my_cars(user_id):
    if session['user_id'] != user_id:
        return redirect('/dashboard')
    if 'user_id' not in session:
        return redirect('/')
    listed = Car.get_by_user(user_id)
    purchased = Car.get_by_buyer(user_id)
    return render_template('user_cars.html', user_id = session['user_id'] , listed_cars = listed, purchased_cars = purchased)

@app.route('/logout', methods=["POST"])
def logout():
    session.clear()
    return redirect('/')