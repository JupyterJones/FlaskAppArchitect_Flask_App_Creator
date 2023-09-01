#!/home/jack/Desktop/StoryMaker/env/bin/python
from moviepy.editor import *
from flask import Flask, request, redirect, url_for, send_from_directory, Response, flash, request, session,jsonify, render_template
from flask import send_file, g
import os
import pygame
from gtts import gTTS
import cv2
import dlib
import numpy as np
from random import randint
from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip
from moviepy.editor import concatenate_videoclips, AudioFileClip
import moviepy.editor as mp
import moviepy.editor
import subprocess
from pathlib import Path as change_ext
import re
from io import BytesIO
import matplotlib.pyplot as plt
import sqlite3
import random
import glob
import signal
import base64
import tempfile
import datetime
import imageio
import time
from werkzeug.utils import secure_filename
import shutil
from search import search
import clean_images
from time import sleep
from pydub import AudioSegment
from PIL import Image, ImageDraw, ImageFont
import uuid
import logging
from logging.handlers import RotatingFileHandler
from flask_cors import CORS
# Initialize Flask app
app = Flask(__name__)
# allow CORS
CORS(app) 


app.secret_key = os.urandom(24)
# Create a logger object
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create a formatter for the log messages
formatter = logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')

# Create a file handler to write log messages to a file
file_handler = RotatingFileHandler(
    'Logs/app.log', maxBytes=10000, backupCount=1)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

# Add the file handler to the logger
logger.addHandler(file_handler)

# Set up logging for the Flask app
app.logger.addHandler(file_handler)
# Define a route for your Flask app


@app.route('/hello_world')
def hello_world():
    TExt = "TEXT TEST 6789"
    logger.debug('This is a debug message: %s', TExt)

    TEXT = "TEXT TEST abcd"
    logger.debug('This is a debug message: %s', TEXT)

    return "Hello, World!"

css_dir = 'static/css'
original_css_dir = os.path.join(css_dir, 'original')
os.makedirs(original_css_dir, exist_ok=True)

def load_original_css_file(filename):
    original_file_path = os.path.join(css_dir, filename)
    with open(original_file_path, 'r') as file:
        return file.read()

def save_original_css_file(filename, content):
    now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    new_filename = f"{filename}_{now}.css"
    new_file_path = os.path.join(original_css_dir, new_filename)
    with open(new_file_path, 'w') as file:
        file.write(content)

def edit_and_save_css_file(filename, content):
    save_original_css_file(filename, content)
    edited_file_path = os.path.join(css_dir, filename)
    with open(edited_file_path, 'w') as file:
        file.write(content)

@app.route('/')
def edit_css():
    filenames = [f for f in os.listdir(css_dir) if f.endswith('.css')]
    filenames = sorted(filenames)
    #render template
    return render_template ('edit_css.html', filenames=filenames)

@app.route('/edit_css_page')
def edit_css_page():
    selected_filename = request.args.get('filename')
    original_content = load_original_css_file(selected_filename)
    return render_template('edit_css_page.html', selected_filename=selected_filename, original_content=original_content)

@app.route('/edit_css_save', methods=['POST'])
def edit_css_save():
    edited_content = request.form['edited_content']
    selected_filename = request.form['filename']
    edit_and_save_css_file(selected_filename, edited_content)
    return redirect(url_for('edit_css'))



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5100)
