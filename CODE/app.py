from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os
from flask import render_template
from flask import Blueprint

code_blueprint = Blueprint('code', __name__)

app = Flask(__name__, template_folder='templates')

# Function to create the database and table
def create_databaseD():
    db_path = os.path.join(os.path.dirname(__file__), 'code.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # ... rest of the code to create the table ...

# ... existing routes and view functions ...
@code_blueprint.route('/')
def index():
    return render_template('index.html')

# Route to access the database using a link
@code_blueprint.route('/access_database')
def access_database():
    db_path = os.path.join(os.path.dirname(__file__), 'code.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM snippets')
    code = cursor.fetchall()
    conn.close()
    return render_template('database.html', code=code)




# Function to create the database and table
def create_databaseD():
    conn = sqlite3.connect('code.db')
    cursor = conn.cursor()
    #cursor.execute("CREATE TABLE snippets (description TEXT, code TEXT, keywords TEXT)")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS snippets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            code TEXT,
            keywords TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Route to display all code
@code_blueprint.route('/code', methods=['GET'])
def display_code():
    conn = sqlite3.connect('code.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM snippets')
    code = cursor.fetchall()
    conn.close()
    
    # Define the HTML code for the form
    form_code = """
    <h1>Add New code</h1>
    <form action="/code" method="post">
        <label for="description">Description:</label>
        <textarea type="description" name="description" rows="8" cols="90%"></textarea><br />
        <label for="code">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Code:</label>
        <textarea type="text" name="code" rows="8" cols="90%"></textarea><br>
        <label for="keywords">Keywords:</label>
        <input style="width:53%;height: 25px;" type="keywords" name="keywords"><br>
        <input type="submit" value="Add code">
    </form>
    """

    return render_template('code.html', code=code, form_code=form_code)
    
# Route to add a new code
@code_blueprint.route('/code', methods=['POST'])
def add_code():
    description = request.form['description']
    code = request.form['code']
    keywords = request.form['keywords']
    
    conn = sqlite3.connect('code.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO snippets (description, code, keywords) VALUES (?, ?, ?)',
                   (description, code, keywords))
    conn.commit()
    conn.close()
    return redirect(url_for('display_code'))

# Route to edit a code
@code_blueprint.route('/edit_code/<int:code_id>', methods=['GET', 'POST'])
def edit_code(code_id):
    conn = sqlite3.connect('code.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        description = request.form['description']
        code = request.form['code']
        keywords = request.form['keywords']
        
        cursor.execute('UPDATE snippets SET description=?, code=?, keywords=? WHERE id=?',
                       (description, code, keywords, code_id))
        conn.commit()
        conn.close()
        return redirect(url_for('display_code'))
    
    cursor.execute('SELECT * FROM snippets WHERE id = ?', (code_id,))
    code = cursor.fetchone()
    conn.close()
    return render_template('edit_code.html', code=code)

# Route to delete a code
@code_blueprint.route('/delete_code/<int:code_id>', methods=['POST'])
def delete_code(code_id):
    conn = sqlite3.connect('code.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM snippets WHERE id = ?', (code_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('display_code'))

if __name__ == '__main__':
    create_databaseD()  # Create the database and table before starting the app
    app.run(debug=True)

