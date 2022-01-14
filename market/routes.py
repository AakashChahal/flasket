from market import app, db
from flask import render_template, redirect, url_for, flash, request
from market.models import Item, User
from market.forms import RegisterForm, LoginForm, PurchaseForm, SellForm
from flask_login import login_user, logout_user, login_required, current_user

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html') 

@app.route('/products', methods=['GET', 'POST'])
@login_required
def products_page():
    items = Item.query.all()
    purchase_form = PurchaseForm()
    if request.method == 'POST':
        purchased_item = request.form.get('purchased_item')
        purchased_object = Item.query.filter_by(name=purchased_item).first()
        if purchased_object:
            purchased_object.owner = current_user.id
            current_user.budget -= purchased_object.price
            db.session.commit()

    items = Item.query.filter_by(owner=None)

    return render_template('products.html', items=items, purchase_form=purchase_form)

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data,
                            email=form.email.data,
                            password_hash=form.password1.data)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        flash(f'You are logged in as {new_user.username}', category="success")
        return redirect(url_for('home_page'))

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

@app.route('/logout')
def logout_page():
    logout_user()
    flash("You are now signed out!", category='info')
    return redirect(url_for('home_page'))