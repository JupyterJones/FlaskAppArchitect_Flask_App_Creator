from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os
import sys
import sqlite3
from flask import Flask, g

app = Flask(__name__)

# Configuration
app.config['DATABASE'] = 'products.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config['DATABASE'])
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.before_first_request
def create_table():
    db = get_db()
    cursor = db.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            price REAL
        )
    ''')

    db.commit()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(app, '_database', None)
    if db is not None:
        db.close()


@app.route('/')
def index():
    return redirect('/products')


@app.route('/products', methods=['GET', 'POST'])
def products():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']

        db = get_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO products (name, description, price) VALUES (?, ?, ?)",
                       (name, description, price))
        db.commit()

    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()

    return render_template('products.html', products=products)


@app.route('/edit/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']

        db = get_db()
        cursor = db.cursor()
        cursor.execute("UPDATE products SET name=?, description=?, price=? WHERE id=?",
                       (name, description, price, product_id))
        db.commit()

        return redirect('/products')

    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM products WHERE id=?", (product_id,))
    product = cursor.fetchone()

    return render_template('edit_product.html', product=product)


@app.route('/delete/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM products WHERE id=?", (product_id,))
    db.commit()

    return redirect('/products')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5200)
