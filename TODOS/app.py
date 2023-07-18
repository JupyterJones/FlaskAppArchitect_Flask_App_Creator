from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__, template_folder='templates')

# Function to create the database and table
def create_database():
    db_path = os.path.join(os.path.dirname(__file__), 'products.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # ... rest of the code to create the table ...

# ... existing routes and view functions ...
@app.route('/')
def index():
    return render_template('index.html')

# Route to access the database using a link
@app.route('/access_database')
def access_database():
    db_path = os.path.join(os.path.dirname(__file__), 'products.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products')
    products = cursor.fetchall()
    conn.close()
    return render_template('database.html', products=products)




# Function to create the database and table
def create_database():
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            price REAL
        )
    ''')
    conn.commit()
    conn.close()

# Route to display all products
@app.route('/products', methods=['GET'])
def display_products():
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products')
    products = cursor.fetchall()
    conn.close()
    return render_template('products.html', products=products)

# Route to add a new product
@app.route('/products', methods=['POST'])
def add_product():
    name = request.form['name']
    description = request.form['description']
    price = float(request.form['price'])
    
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO products (name, description, price) VALUES (?, ?, ?)',
                   (name, description, price))
    conn.commit()
    conn.close()
    return redirect(url_for('display_products'))

# Route to edit a product
@app.route('/edit_product/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = float(request.form['price'])
        
        cursor.execute('UPDATE products SET name=?, description=?, price=? WHERE id=?',
                       (name, description, price, product_id))
        conn.commit()
        conn.close()
        return redirect(url_for('display_products'))
    
    cursor.execute('SELECT * FROM products WHERE id = ?', (product_id,))
    product = cursor.fetchone()
    conn.close()
    return render_template('edit_product.html', product=product)

# Route to delete a product
@app.route('/delete_product/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM products WHERE id = ?', (product_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('display_products'))

if __name__ == '__main__':
    create_database()  # Create the database and table before starting the app
    app.run(debug=True)

