from market import app
from flask import render_template
from market.models import Item

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html') 

@app.route('/products')
def products_page():
    items = Item.query.all()
    return render_template('products.html', items=items)