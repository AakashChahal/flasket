from market import app, db
from flask import render_template, redirect, url_for, flash
from market.models import Item, User
from market.forms import RegisterForm

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
                            password=form.password1.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('products_page'))

    if form.errors != {}:
        for msg in form.errors.values():
            flash(msg, category="danger")

    return render_template('register.html', form=form)
