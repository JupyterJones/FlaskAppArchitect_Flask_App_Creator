from flask import Blueprint

# Create a blueprint instance for the main app
main_bp = Blueprint('main', __name__)

# Import the views/routes that belong to the main app
from . import app

# Register the main app blueprint
app.register_blueprint(main_bp)

# Import and register the database blueprint
from . import database
app.register_blueprint(database.database_bp)

