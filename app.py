import json
from pathlib import Path

from flask import Flask, flash, redirect, render_template, request, session, url_for


app = Flask(__name__)
app.config['SECRET_KEY'] = 'some_secret_key'

BASE_DIR = Path(__file__).resolve().parent


def load_data():
    with open(BASE_DIR / 'data' / 'flowers.json', encoding='utf-8') as flowers_file:
        flowers = json.load(flowers_file)

    with open(BASE_DIR / 'data' / 'addons.json', encoding='utf-8') as addons_file:
        addons = json.load(addons_file)

    return flowers, addons


def calculate_total(cart):
    total = sum(item['price'] * item['quantity'] for item in cart.values())
    return total


@app.route('/')
def index():
    flowers, addons = load_data()
    cart = session.get('cart', {})
    total = calculate_total(cart)
    featured_flowers = {
        flower: details
        for flower, details in flowers.items()
        if details.get('in_stock')
    }
    return render_template(
        'index.html',
        flowers=flowers,
        featured_flowers=featured_flowers,
        addons=addons,
        cart=cart,
        total=total
    )


@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    flower = request.form['flower']
    quantity = int(request.form['quantity'])
    flowers, _addons = load_data()
    cart = session.get('cart', {})

    if flower not in flowers:
        flash('Invalid flower selected.')
        return redirect(url_for('index'))

    if flower in cart:
        cart[flower]['quantity'] += quantity
    else:
        cart[flower] = {
            'price': flowers[flower]['price'],
            'quantity': quantity
        }

    session['cart'] = cart
    session.modified = True
    flash(f'{quantity} {flower}(s) added to cart.')
    return redirect(url_for('index'))


@app.route('/remove_from_cart/<item>')
def remove_from_cart(item):
    cart = session.get('cart', {})

    if item in cart:
        del cart[item]
        session['cart'] = cart
        session.modified = True
        flash(f'Removed all {item.capitalize()} from the cart.')
    else:
        flash('Item not found in cart.')

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
