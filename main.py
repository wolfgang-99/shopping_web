from flask import Flask, render_template, session, redirect, url_for
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("secret_key")

# Sample product data
products = [
    {'id': 1, 'name': 'Product 1', 'price': 10, 'image_url': '/static/eye wear_img.jpeg'},
    {'id': 2, 'name': 'Product 2', 'price': 15, 'image_url': '/static/glass_img.jpg'},
    {'id': 3, 'name': 'Product 3', 'price': 20, 'image_url': '/static/wine glass_img.jpeg'},
]


# Initialize an empty cart in the session
@app.before_request
def before_request():
    if 'cart' not in session:
        session['cart'] = []


@app.route('/')
def index():
    return render_template('index.html', products=products)


@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if product:
        cart = session['cart']
        if product not in cart:
            cart.append(product)
            session['cart'] = cart
    return redirect(url_for('index'))


@app.route('/cart')
def view_cart():
    cart = session['cart']
    total_price = sum(item['price'] for item in cart)
    return render_template('cart.html', cart=cart, total_price=total_price)


@app.route('/remove_from_cart/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    cart = session['cart']
    for item in cart:
        if item['id'] == product_id:
            cart.remove(item)
            session['cart'] = cart
            break
    return redirect(url_for('view_cart'))


if __name__ == '__main__':
    app.run(debug=True)
