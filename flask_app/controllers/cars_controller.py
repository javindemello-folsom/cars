from flask import Flask, render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.user_model import User
from flask_app.models.car_model import Car
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/cars/new')
def new_car():
    if 'user_id' not in session:
        return redirect('/')
    return render_template("new_car.html")


@app.route('/cars/add', methods=["POST"])
def add_car():
    if not Car.validate_car(request.form):
        return redirect('/cars/new')
    data = {
        "price": request.form["price"],
        "model": request.form["model"],
        "make": request.form["make"],
        "year": request.form["year"],
        "description": request.form["description"],
        "user_id": session['user_id'],
        "seller": session['fname']
    }
    Car.save(data)
    return redirect('/dashboard')

@app.route('/cars/view/<int:car_id>')
def view_car(car_id):
    if 'user_id' not in session:
        return redirect('/')
    car = Car.get_one(car_id)
    print(car.user_id,session['user_id'])
    user = User.get_by_car(car_id)
    # Created new classmethod because I couldn't figure out how to do it with User.get_by_id().
    return render_template('view_car.html', car=car, user=user)


@app.route('/cars/edit/<int:car_id>')
def edit_page(car_id):
    user = User.get_by_car(car_id)
    if session['user_id'] != user.id:
        return redirect('/dashboard')
    car = Car.get_one(car_id)
    return render_template("edit_car.html", car_id = car_id, car = car)

@app.route('/update/<int:car_id>', methods=["POST"])
def update(car_id):
    if not Car.validate_car(request.form):
        return redirect(f'/cars/edit/{car_id}')
    Car.update(request.form)
    return redirect('/dashboard')

@app.route('/cars/delete/<int:car_id>')
def delete_car(car_id):
    Car.delete(car_id)
    return redirect('/dashboard')

@app.route('/purchase/<int:car_id>', methods=["POST"])
def buy(car_id):
    data = {
        "car_id": car_id,
        "user_id": session['user_id']
    }
    Car.buy(data)
    return redirect('/dashboard')