from market import app, db
from flask import render_template, redirect, url_for, flash
from market.models import Item, User
from market.forms import RegisterForm, LoginForm
from flask_login import login_user

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html') 

@app.route('/products')
def products_page():
    items = Item.query.all()
    return render_template('products.html', items=items)

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data,
                            email=form.email.data,
                            password_hash=form.password1.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('products_page'))

    if form.errors != {}:
        for msg in form.errors.values():
            flash(msg, category="danger")

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        curr_user = User.query.filter_by(email=form.email.data).first()
        if curr_user and curr_user.check_password(password=form.password.data):
            login_user(curr_user)
            flash(f'You are logged in as: {curr_user.username}', category="success")
            return redirect(url_for('home_page'))
        flash("Invalid credentials!", category="danger")

    return render_template('login.html', form=form)
