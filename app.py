import json
from pathlib import Path

from flask import Flask, render_template


app = Flask(__name__)
app.config['SECRET_KEY'] = 'some_secret_key'

BASE_DIR = Path(__file__).resolve().parent


def load_data():
    with open(BASE_DIR / 'data' / 'flowers.json', encoding='utf-8') as flowers_file:
        flowers = json.load(flowers_file)

    with open(BASE_DIR / 'data' / 'addons.json', encoding='utf-8') as addons_file:
        addons = json.load(addons_file)

    return flowers, addons


@app.route('/')
def index():
    flowers, addons = load_data()
    featured_flowers = {
        flower: details
        for flower, details in flowers.items()
        if details.get('in_stock')
    }
    return render_template(
        'index.html',
        flowers=flowers,
        featured_flowers=featured_flowers,
        addons=addons
    )

if __name__ == '__main__':
    app.run(debug=True)
