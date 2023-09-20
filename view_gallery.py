#!/home/jack/Desktop/FlaskAppArchitect_Flask_App_Creator/env/bin/python
from flask import  render_template, request, redirect, url_for,Blueprint
import os
import logging
from logging.handlers import RotatingFileHandler
view_gallery_bp = Blueprint('view_gallery', __name__)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create a formatter for the log messages
formatter = logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')

# Create a file handler to write log messages to a file
file_handler = RotatingFileHandler(
    'Logs/View_gallery.log', maxBytes=10000, backupCount=1)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

# Add the file handler to the logger
logger.addHandler(file_handler)
# Function to get a list of subdirectories in static/images/
def get_image_directories():
    image_dir = 'static/images'
    return [d for d in os.listdir(image_dir) if os.path.isdir(os.path.join(image_dir, d))]

@view_gallery_bp.route('/gallery_index')
def gallery_index():
    directories = get_image_directories()
    logger.info('Gallery index page accessed')
    logger.debug('Directories: %s', directories)
    return render_template('gallery_index.html', directories=directories)

@view_gallery_bp.route('/gallery', methods=['POST', 'GET'])
def generate_gallery():
    selected_directory = request.form['directory']
    logger.info('Generate gallery page accessed')
    logger.debug('Selected directory: %s', selected_directory)
    return redirect(url_for('view_gallery.image_gallery', directory_name=selected_directory))


@view_gallery_bp.route('/gallery/<directory_name>')
def image_gallery(directory_name):
    logger.info('Image gallery page accessed') 
    logger.debug('Directory name: %s', directory_name) 
    selected_directory = os.path.join('static/images', directory_name)

    # Check if the selected directory exists
    if not os.path.exists(selected_directory):
        # Handle the case where the directory does not exist
        return "Directory not found", 404

    image_files = [f for f in os.listdir(selected_directory) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))]
    logger.debug('Image files: %s', image_files)
    image_urls = [os.path.join('/static/images', directory_name, image) for image in image_files]
    logger.debug('Image URLs: %s', image_urls)
    return render_template('view_gallery.html', image_urls=image_urls)



