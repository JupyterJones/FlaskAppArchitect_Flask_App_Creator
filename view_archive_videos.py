import os
from flask import render_template, Blueprint
from flask.helpers import send_from_directory
import logging
from logging.handlers import RotatingFileHandler

# Create a Blueprint object
view_archive_videos_bp = Blueprint('view_archive_videos', __name__)

# Define the directory where your MP4 videos are stored
video_directory = 'static/Archive_Videos'

# Create a logger for this Blueprint
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

@view_archive_videos_bp.route('/video_index')
def video_index():
    # Get a list of all MP4 files in the directory
    video_files = [file for file in os.listdir(video_directory) if file.endswith('.mp4')]
    print(video_files)    
    # Create a list to store video information (name and path)
    video_list = []
    
    for video_file in video_files:
        video_path = os.path.join(video_directory, video_file)
        video_name = os.path.splitext(video_file)[0]  # Remove file extension
        
        # Append video name and path to the list
        video_list.append({
            'name': video_name,
            'path': video_path
        })
    
    # Render the HTML template with the list of videos
    return render_template('video_index.html', videos=video_list)

@view_archive_videos_bp.route('/archive_videos/<video_name>')
def play_video(video_name):
    # Construct the full path to the selected video
    video_path = os.path.join(video_directory, f'{video_name}.mp4')
    print(video_path)   
    # Log the video_name and video_path
    logger.debug("video_name: %s, video_path: %s", video_name, video_path)
    
    # Use the 'send_from_directory' function to send the video file
    return send_from_directory(video_directory, f'{video_name}.mp4')
