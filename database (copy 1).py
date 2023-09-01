from flask import Flask, render_template, request, redirect, url_for, g
import sqlite3
import logging

app = Flask(__name__)
app.config['DATABASE'] = 'code.db'

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config['DATABASE'])
    return db

@app.route('/')
def indexdb():
    logger.debug("Accessing indexdb route")
    return render_template('indexdb.html')

@app.route('/select_by_id_form', methods=['POST', 'GET'])
def select_by_id_form():
    logger.debug("Accessing select_by_id_form route")
    return render_template('select_by_id_form.html')

@app.route('/search_by_rowid', methods=['GET', 'POST'])
def search_by_rowid():
    logger.debug("Accessing search_by_rowid route")
    return render_template('search_by_rowid.html')

# ...

# ...

@app.route('/edit_data_page', methods=['GET', 'POST'])
@app.route('/edit_data_page/<int:rowid>', methods=['GET', 'POST'])
def edit_data_page(rowid=None):
    db = get_db()
    cursor = db.cursor()

    if request.method == 'POST':
        description = request.form['description']
        code = request.form['code']
        keywords = request.form['keywords']

        if rowid is not None:
            # Update the data in the database for the given rowid
            cursor.execute("UPDATE snippets SET description = ?, code = ?, keywords = ? WHERE rowid = ?",
                           (description, code, keywords, rowid))
        else:
            # Insert the data into the database as a new row
            cursor.execute("INSERT INTO snippets (description, code, keywords) VALUES (?, ?, ?)",
                           (description, code, keywords))

        db.commit()

        # Close the database connection
        cursor.close()
        db.close()

        return redirect(url_for('indexdb'))

    if rowid is not None:
        # If a rowid is provided, retrieve the data from the database
        # based on the provided rowid and render the edit_data.html template
        cursor.execute("SELECT * FROM snippets WHERE rowid = ?", (rowid,))
        data = cursor.fetchone()

        if data is None:
            # If no data is found for the given rowid, return an error message
            return "Error: Data not found for the provided Row ID."

        # Convert the fetched data to a dictionary for easier access in the template
        data = {
            'rowid': data[0],
            'description': data[1],
            'code': data[2],
            'keywords': data[3]
        }

    else:
        # If no rowid is provided, create an empty data dictionary
        data = {}

    # Close the database connection
    cursor.close()
    db.close()

    return render_template('edit_data.html', data=data)

# ...
@app.route('/get_rowid_form', methods=['GET', 'POST'])
def get_rowid_form():
    if request.method == 'POST':
        rowid = request.form['rowid']
        return redirect(url_for('edit_data_page', rowid=rowid))
    return render_template('get_rowid_form.html')

# ...



@app.route('/search_database', methods=['POST', 'GET'])
def search_database():
    logger.debug("Accessing search_database route")
    if request.method == 'POST':
        search_term = request.form['search_term']
        search_area = request.form['search_area']
    else:
        # For GET requests, get the search_term and search_area from the query string
        search_term = request.args.get('search_term')
        search_area = request.args.get('search_area')

    if not search_term or not search_area:
        logger.debug("Redirecting to indexdb due to missing search_term or search_area")
        return redirect('/indexdb')  # Redirect to the main index page if search_term or search_area is missing

    db = get_db()
    cursor = db.cursor()

    if search_area == 'rowid':
        cursor.execute("SELECT rowid, * FROM snippets WHERE rowid = ?", (search_term,))
    elif search_area == 'description':
        cursor.execute("SELECT rowid, * FROM snippets WHERE description LIKE ?", ('%' + search_term + '%',))
    elif search_area == 'code':
        cursor.execute("SELECT rowid, * FROM snippets WHERE code LIKE ?", ('%' + search_term + '%',))
    elif search_area == 'keywords':
        cursor.execute("SELECT rowid, * FROM snippets WHERE keywords LIKE ?", ('%' + search_term + '%',))
    else:
        logger.debug("Redirecting to indexdb due to invalid search area")
        return redirect('/indexdb')  # Redirect to the main index page if an invalid search area is provided

    results = cursor.fetchall()
    logger.debug("Rendering db_results.html template with search results")
    return render_template('db_results.html', results=results)

@app.route('/insert_data', methods=['POST','GET'])
def insert_data():
    logger.debug("Accessing insert_data route")
    if request.method == 'POST':
        description = request.form['description']
        code = request.form['code']
        keywords = request.form['keywords']

        # Assuming you have the database connection and cursor defined
        db = get_db()
        cursor = db.cursor()

        cursor.execute("INSERT INTO snippets (description, code, keywords) VALUES (?, ?, ?)",
                       (description, code, keywords))
        db.commit()

        # Close the database connection
        cursor.close()
        db.close()

        logger.debug("Redirecting to indexdb after inserting data")
        return redirect(url_for('indexdb'))

    # If the request method is not POST (e.g., GET), render the insert_data.html template
    logger.debug("Rendering insert_data.html template")
    return render_template('insert_data.html')

@app.route('/select_by_id', methods=['POST', 'GET'])
def handle_select_by_id():
    logger.debug("Accessing select_by_id route")
    if request.method == 'POST':
        row_id = request.form['search_term']
    else:
        row_id = request.args.get('search_term')

    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM snippets WHERE rowid = ?", (row_id,))
    data = cursor.fetchone()

    cursor.close()
    db.close()

    if data is not None:
        id_value = data[0]
        description = data[1]
        code = data[2]
        keywords = data[3]

        logger.debug("Rendering display_data.html template with selected data")
        return render_template('display_data.html', id_value=id_value, description=description, code=code, keywords=keywords)
    else:
        logger.debug("Rendering display_data.html template with no data found")
        return render_template('display_data.html', id_value=row_id, description="", code="", keywords="")

if __name__ == '__main__':
    app.run(debug=True, port=5200)
