from flask import Blueprint, render_template, request, g
import sqlite3

database_bp = Blueprint('database', __name__)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('code.db')
    return db

@database_bp.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@database_bp.route('/search_database', methods=['GET', 'POST'])
def search_database():
    # ... Your search_database route code ...

@database_bp.route('/insert_data', methods=['POST'])
def insert_data():
    # ... Your insert_data route code ...

# ... Add other database-related routes ...


