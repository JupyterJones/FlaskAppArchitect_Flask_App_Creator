import os
from flask import Flask, render_template, request, redirect, url_for
import glob
import logging
from logging.handlers import RotatingFileHandler
from werkzeug.utils import secure_filename
import shutil
import random
import cv2
from PIL import Image
app = Flask(__name__)
# Create a logger object
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create a formatter for the log messages
formatter = logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')

# Create a file handler to write log messages to a file
file_handler = RotatingFileHandler(
    'Logs/FADE.log', maxBytes=10000, backupCount=1)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

# Add the file handler to the logger
logger.addHandler(file_handler)

# Set up logging for the Flask app
logger.addHandler(file_handler)
# Define a route for your Flask app

SDIR = "static/"
# Define the file path to store the script content
script_file = os.path.join(os.getcwd(),SDIR, 'scripts', 'scripts.js')
app.secret_key = os.urandom(24)
@app.route('/hello_world')
def hello_world():
    TExt = "TEXT TEST 6789"
    logger.debug('This is a debug message: %s', TExt)

    TEXT = "TEXT TEST abcd"
    logger.debug('This is a debug message: %s', TEXT)

    return "Hello, World!"
app = Flask(__name__)

# Function to list available image directories
def list_image_directories():
    image_directories = glob.glob("static/images/*")
    return image_directories

@app.route('/')
def fade_index():
    # List available image directories
    image_directories = list_image_directories()
    logger.debug(image_directories)
    return render_template('fade_index.html', image_directories=image_directories)

@app.route('/generate_video', methods=['POST'])
def generate_video():
    try:
        selected_directory = request.form['selected_directory']

        if not selected_directory:
            return redirect(url_for('fade_index'))

        # List all image files in the selected directory
        image_files = []
        logger.debug("selected_directory: ", selected_directory)
        for root, dirs, files in os.walk(selected_directory):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                    image_files.append(os.path.join(root, file))

        if not image_files:
            return render_template('fade_index.html', video='')

        # Sort the image files to ensure they are in the correct order
        #image_files.sort()
        #shuffle the images mix
        random.shuffle(image_files)

        # Create a temporary directory to store the resized images
        temp_dir = 'temp/'
        os.makedirs(temp_dir, exist_ok=True)

        # Load and resize the images
        resized_images = []
        for image_file in image_files:
            im = Image.open(image_file)
            SIZE = im.size

            img = cv2.imread(image_file)
            img = cv2.resize(img, SIZE)  # Resize to the same size as the original image
            resized_images.append(img)

        # Create a video writer
        out_path = 'static/assets/output.mp4'
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # You may need to change the codec depending on your system
        out = cv2.VideoWriter(out_path, fourcc, 30, SIZE)

        # Create the video with fading transitions
        for i in range(len(resized_images)):
            img1 = resized_images[i]
            img2 = resized_images[(i + 1) % len(resized_images)]  # Wrap around to the first image
            for alpha in range(0, 101):  # Gradually change alpha from 0 to 100 for fade effect
                alpha /= 100.0
                blended = cv2.addWeighted(img1, 1 - alpha, img2, alpha, 0)
                out.write(blended)

        out.release()
        return render_template('fade_index.html', video='assets/output.mp4')

    except Exception as e:
        # Handle any exceptions
        return "An error occurred. Please check the logs for details."

if __name__ == '__main__':
    print("Served on port 5500")
    app.run(debug=True, port=5500)

