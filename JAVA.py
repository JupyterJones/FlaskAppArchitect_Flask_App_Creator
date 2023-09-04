#!/home/jack/Desktop/FlaskAppArchitect_Flask_App_Creator/env/bin/python
from flask import Flask, render_template, redirect, url_for, request, session
import logging
from logging.handlers import RotatingFileHandler
import os
import datetime
import random

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Create a logger object
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create a formatter for the log messages
formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')

# Create a file handler to write log messages to a file
file_handler = RotatingFileHandler('Logs/CANVAS.log', maxBytes=10000, backupCount=1)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

# Add the file handler to the logger
logger.addHandler(file_handler)

# Define paths and directories
canvas_dir = 'static/canvas'
original_canvas_dir = os.path.join(canvas_dir, 'original')
os.makedirs(original_canvas_dir, exist_ok=True)
@app.route('/hello_world')
def hello_world():
    TExt = "TEXT TEST 6789"
    logger.debug('This is a debug message: %s', TExt)

    TEXT = "TEXT TEST abcd"
    logger.debug('This is a debug message: %s', TEXT)

    return "Hello, World!"

def findvideos():
    videoroot_directory = "static"
    MP4 = []
    for dirpath, dirnames, filenames in os.walk(videoroot_directory):
        for filename in filenames:
            if filename.endswith(".mp4") and "Final" in filename:
                MP4.append(os.path.join(dirpath, filename))
    if MP4:
        last_video = session.get("last_video")
        new_video = random.choice([video for video in MP4 if video != last_video])
        session["last_video"] = new_video
        return new_video
    else:
        return None



# Function to load the original canvas file
def load_original_canvas_file(filename):
    original_file_path = os.path.join(canvas_dir, filename)
    with open(original_file_path, 'r') as file:
        logger.debug("original_file_path:",original_file_path)
        return file.read()

# Function to save the original canvas file with a timestamp
def save_original_canvas_file(filename, content):
    now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    new_filename = f"{filename}_{now}canvas.js"
    new_file_path = os.path.join(original_canvas_dir, new_filename)
    with open(new_file_path, 'w') as file:
        file.write(content)

# Function to edit and save the canvas file
def edit_and_save_canvas_file(filename, content):
    save_original_canvas_file(filename, content)
    logger.debug("filename:",filename)
    logger.debug("content:",content)
    edited_file_path = os.path.join(canvas_dir, filename)
    with open(edited_file_path, 'w') as file:
        file.write(content)

@app.route('/')
def index():
    return redirect(url_for('edit_canvas'))

@app.route('/edit_canvas')
def edit_canvas():
    filenames = [f for f in os.listdir(canvas_dir) if f.endswith('canvas.js')]
    filenames = sorted(filenames)
    logger.debug("FILENAMES:",filenames)
    fvideo = findvideos()  # Assuming findvideos() is defined elsewhere
    logger.debug("FVIDEO:",fvideo)
    return render_template('edit_canvas.html', filenames=filenames, video=fvideo)

@app.route('/edit_canvas_page')
def edit_canvas_page():
    selected_filename = request.args.get('filename')
    logger.debug("selected_filename:",selected_filename)
    original_content = load_original_canvas_file(selected_filename)
    logger.debug("original_content:",original_content)
    return render_template('edit_canvas_page.html', selected_filename=selected_filename, original_content=original_content)

@app.route('/edit_canvas_save', methods=['POST'])
def edit_canvas_save():
    edited_content = request.form['edited_content']
    selected_filename = request.form['filename']
    edit_and_save_canvas_file(selected_filename, edited_content)
    return redirect(url_for('edit_canvas'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5400)
