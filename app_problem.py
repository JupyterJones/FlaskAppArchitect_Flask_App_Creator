#!/home/jack/Desktop/StoryMaker/env/bin/python
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, Response,flash
from flask import send_file, make_response,g, jsonify
import os
import pygame
from gtts import gTTS
import cv2
import dlib
import numpy as np
from random import randint
from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip
from moviepy.editor import concatenate_videoclips, AudioFileClip, TextClip
import moviepy.editor
import subprocess 
import shutil  
import logging
from io import BytesIO
import sqlite3
import random
import glob
import base64
import tempfile
import datetime
import imageio
import time
from werkzeug.utils import secure_filename
import shutil
import json
import sys
import logging
#from . import search
from . import clean_images
from time import sleep
from pydub import AudioSegment
from PIL import Image, ImageDraw, ImageFont
from logging.handlers import RotatingFileHandler
import moviepy.editor as mp
from flask import Flask
#sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'CODE'))
from CODE import code_blueprint
app = Flask(__name__, template_folder='templates')
app.secret_key = os.urandom(24)
import uuid
# Register the Blueprint
app.register_blueprint(code_blueprint, name='code_blueprint')
# Create a logger object
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create a formatter for the log messages
formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')

# Create a file handler to write log messages to a file
file_handler = RotatingFileHandler('/home/jack/Desktop/Project/StoryMaker/Logs/app.log', maxBytes=10000, backupCount=1)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

# Add the file handler to the logger
logger.addHandler(file_handler)

# Now you can use the logger to log messages
TExt = "TEXT TEST 12345"
logger.debug('This is a debug message: %s', TExt)
TExt = "TEXT TEST 6789"
logger.debug('This is a debug message: %s', TExt)
TExt = "TEXT TEST abcd"
logger.debug('This is a debug message: %s', TExt)
# Set up logging for the Flask app
app.logger.addHandler(file_handler)
# Create a logger object
logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__, static_url_path='/static')
app.config['UPLOAD_FOLDER'] = 'static/images/uploads'
app.config['RESULTS_FOLDER'] = 'static/videos/results'
app.config['THUMBNAILS_FOLDER'] = 'static/images/thumbnails'
app.config['CHECKPOINT_PATH'] = 'checkpoints/wav2lip_gan.pth'
app.config['AUDIO_PATH'] = 'sample_data/input_audio.wav'
app.config['video_PATH'] = 'sample_data/input_videio.mp4'
app.config['DATABASE'] = 'code.db'  # SQLite database file
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

# use the search function as a route
app.add_url_rule('/search', 'search')
# load the conversations JSON file
with open('/home/jack/Desktop/Project/StoryMaker/static/chat/conversations.json', 'r') as f:
    conversations = json.load(f)

@app.route('/search')
def search():
    # get the search query from the request parameters
    query = request.args.get('q')

    # search the conversations for the query
    results = []
    for conversation in conversations:
        if 'messages' in conversation:
            for message in conversation['messages']:
                if 'content' in message and query.lower() in message['content'].lower():
                    results.append(message)

    # return the search results as JSON
    return jsonify(results)
def zip_lists(list1, list2):
    return zip(list1, list2)

app.jinja_env.filters['zip'] = zip_lists

directory_path = 'temp'  # Replace with the desired directory path
# Create the directory if it doesn't exist
os.makedirs(directory_path, exist_ok=True)

@app.route('/')
def index():
    image_dir = os.path.join(os.path.dirname(__file__), 'static', 'images')
    #image_dir = 'static/images'
    image_files = [f for f in os.listdir(image_dir) if f.endswith('.jpg')]
    random_image_file = random.choice(image_files)
    return render_template('index.html', random_image_file="images/"+random_image_file)

def generate_output():
    # Specify the path to your Bash script
    bash_script_path = '/home/jack/Desktop/content/MakeVideo'

    # Execute the Bash script
    subprocess.run(['bash', bash_script_path])
    # Backup the result_videoxx.mp4 file
    current_datetime = str(int(time.time()))
    unique_id = str(uuid.uuid4().hex)  # Generate a unique identifier
    #backup_filename = f"static/{current_datetime}_{unique_id}.mp4"
    backup_filename = "static/{}_{}.mp4".format(current_datetime, unique_id)
    shutil.copyfile("results/result_voice.mp4", backup_filename)    
    redirect('/final_lipsync')
    return "Generated output"


@app.route('/create_avatar', methods=['GET', 'POST'])
def create_avatar():
      if request.method == 'POST':
          #check_point = os.path.join(app.config['CHECKPOINT_PATH'], 'checkpoints/wav2lip_gan.pth')

          return Response(generate_output(), mimetype='text/plain')
      else:
          return render_template('create_avatar.html')
  

@app.route('/run_command', methods=['GET'])
def run_command():
    # Specify the path to your Bash script
    bash_script_path = 'MakeVideo'

    # Execute the Bash script
    subprocess.run(['bash', bash_script_path])
    # Backup the result_videoxx.mp4 file
    current_datetime = str(int(time.time())) 
    backup_filename = f"static/{current_datetime}.mp4"
    shutil.copyfile("results/result_voice.mp4", backup_filename)    
    redirect('/final_lipsync')

@app.route('/result/<filename>')
def result(filename):
    return render_template('result.html', filename=filename)
  
@app.route('/convert_mp3_to_wav', methods=['GET', 'POST'])
def convert_mp3_to_wav():
    if request.method == 'POST':
        mp3_file = request.files['mp3_file']
        mp3_filename = mp3_file.filename
        mp3_path = os.path.join(app.static_folder, 'audio_mp3', mp3_filename)
        mp3_file.save(mp3_path)

        wav_filename = 'input_audio.wav'
        wav_path = os.path.join('sample_data', wav_filename)

        sound = AudioSegment.from_mp3(mp3_path)
        sound.export(wav_path, format='wav')

        return 'MP3 file converted to WAV successfully'
    else:
        return render_template('convert_mp3_to_wav.html')
 
 
@app.route('/final_lipsync')
def final_lipsync():
    VIDEO = 'result/result_voice.mp4'
    return render_template('final_lipsync.html', video=VIDEO)
   
@app.route('/text_mp3', methods=['GET', 'POST'])
def text_mp3():
    if request.method == 'POST':
        # Get the text from the textarea
        text = request.form['text']
        text0 = text
        # Remove whitespace from the text
        text = text.replace(" ", "")
        # Create a filename based on the first 25 characters of the text
        filename = "static/audio_mp3/" + text[:25] + ".mp3"
        textname = text[:25] + ".txt"
        # Save the text to a text file
        textname = textname.strip()
        with open("static/text/"+textname, 'w') as f:
            f.write(text0)
        filename = filename.strip()  # remove the newline character
        # Create a gTTS object and save the audio file
        tts = gTTS(text)
        filename = filename.strip() 
        tts.save(filename)
        shutil.copy(filename, 'static/TEMP.mp3')
        # Play the mp3 file
        pygame.mixer.init()
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        # Wait for the audio to finish playing
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        # Stop pygame and exit the program
        pygame.mixer.quit()
        pygame.quit()
        # Return the text and filename to the template
        return render_template('text_mp3.html', text=text, filename=filename)
    else:
        # Render the home page template
        return render_template('text_mp3.html')
@app.route('/mp3_upload', methods=['POST'])
def mp3_upload():
    if 'file' not in request.files:
        return 'No file uploaded', 400

    file = request.files['file']
    if file.filename == '':
        return 'No file selected', 400

    if file:
        audio_file = 'static/TEMP.mp3'
        file.save(audio_file)
        return render_template('player.html', audio_file=audio_file)
    
@app.route('/generate_video', methods=['GET', 'POST'])
def generate_video():
    if request.method == 'POST':
        # Set the input and output filenames
        eyes_filename = 'static/TEMP.png'
        input_filename = 'static/TEMP2.mp4'
        output_filename = 'static/TEMP2.mp4'
        
        # Set the paths for the video and audio files
        audio_file = 'static/TEMP.mp3'
        output_filenames = 'static/TEMP.mp4'
        
        # Extract eyes from the uploaded image and save as eyes_test.png
        image_path = "static/TEMP.jpg"
        shape_predictor_path = "/home/jack/hidden/shape_predictor_68_face_landmarks.dat"
        extract_eyes(image_path, eyes_filename, shape_predictor_path)
        
        # Load the image clip
        image_clip = ImageClip(image_path, duration=30)
        
        # Set the final clip properties
        final_clip = image_clip.set_audio(None)
        final_clip = final_clip.set_position('center')
        
        # Write the final video
        final_clip.write_videofile(output_filename, codec='libx264', fps=30, audio=False)
        
        # Load the input video without audio
        input_clip = VideoFileClip(input_filename, audio=False)
        
        # Load the eye image clip
        eyes_clip = ImageClip(eyes_filename)
        
        # Create multiple looping clips
        clips = []
        for i in range(8):
            loop_clip = mkloop(input_clip, eyes_clip)
            clips.append(loop_clip)
        
        # Concatenate all the clips
        final_clips = concatenate_videoclips(clips)
        
        # Write the final video
        final_clips.write_videofile(output_filenames, codec='libx264', fps=input_clip.fps, audio=False)
        
        # Load the video and audio files
        video_clip = VideoFileClip(output_filenames)
        audio_clip = AudioFileClip(audio_file)
        
        # Set the duration of the final video to match the audio clip's duration
        final_duration = audio_clip.duration+.5
        
        # Set the video clip's duration to match the final duration
        video_clip = video_clip.set_duration(final_duration)
        
        # Set the audio of the video clip to be the same as the loaded audio clip
        video_clip = video_clip.set_audio(audio_clip)
        
        # Write the final video file
        output_path = "static/final_video_blinking.mp4"
        video_clip.write_videofile(output_path, codec='libx264', audio_codec='aac', fps=24)
        shutil.copy(output_path, 'results/final_video_blinking.mp4')
        return render_template('generate_video.html', video_path=output_path)
    
    return render_template('generate_video.html')

# Function to extract eyes from an image using dlib
def extract_eyes(image_path, eyes_filename, shape_predictor_path):
    # Load the image and shape predictor model
    image = cv2.imread(image_path)
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(shape_predictor_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = detector(gray)

    # Iterate over the detected faces and extract the eye regions
    for face in faces:
        landmarks = predictor(gray, face)

        # Extract the coordinates of the left eye
        left_eye_pts = [(landmarks.part(i).x, landmarks.part(i).y) for i in range(36, 42)]

        # Extract the coordinates of the right eye
        right_eye_pts = [(landmarks.part(i).x, landmarks.part(i).y) for i in range(42, 48)]

        # Create a transparent image with an alpha channel
        transparent_image = np.zeros((image.shape[0], image.shape[1], 4), dtype=np.uint8)

        # Define the skin color (e.g., light brown or tan) in BGR format
        #skin_color_bgr = (210, 180, 140)
        skin_color_bgr = (80, 80, 40)

        # Convert BGR to RGB
        skin_color_rgb = (skin_color_bgr[2], skin_color_bgr[1], skin_color_bgr[0])

        # Draw the eye regions on the transparent image with the skin color and alpha channel
        cv2.fillPoly(transparent_image, [np.array(left_eye_pts)], skin_color_rgb + (200,))
        cv2.fillPoly(transparent_image, [np.array(right_eye_pts)], skin_color_rgb + (200,))
        blurred_image = cv2.GaussianBlur(transparent_image, (5, 5), 0)
        # Save the transparent image with only the eyes as a PNG file
        cv2.imwrite(eyes_filename, blurred_image)


# Function to create a looping clip with blinking eyes
def mkloop(input_clip, eyes_clip):
    # Set the duration of the eye image clip
    eyes_duration = 0.1  # seconds

    # Set the position of the eye image clip
    eyes_position = 'center'

    # Set the start time of the eye image clip
    blink_start_time = randint(2, 4)

    # Create a CompositeVideoClip with the input video and the eye image clip
    final_clip = CompositeVideoClip([input_clip, eyes_clip.set_duration(eyes_duration)
                                                      .set_position(eyes_position)
                                                      .set_start(blink_start_time)])

    # Calculate the duration of the final clip
    final_duration = blink_start_time + eyes_duration + randint(2, 4)  # 5 to 8 seconds after the blink

    # Set the duration of the final clip
    final_clip = final_clip.set_duration(final_duration)
    return final_clip

def apply_text(mp4_path, text, x, y):
    video = moviepy.editor.VideoFileClip(mp4_path)
    font = "/home/jack/fonts/OpenSansBold.ttf"
    text_clip = moviepy.editor.TextClip(text, font=font, fontsize=24, color="white")

    try:
        x = int(x)
        y = int(y)
    except ValueError:
        raise ValueError("Invalid position values. Please provide integer values for x and y.")

    if not (0 <= x <= video.w):
        raise ValueError("Invalid x position. Must be within the width of the video.")
    
    if not (0 <= y <= video.h):
        raise ValueError("Invalid y position. Must be within the height of the video.")

    text_clip = text_clip.set_position((x, y))

    # Check if duration is None and set a default value if necessary
    video_duration = video.duration if video.duration is not None else 0
    text_clip_duration = text_clip.duration if text_clip.duration is not None else 0

    # Set the duration of the video and text clips
    duration = max(video_duration, text_clip_duration)
    video = video.set_duration(duration)
    text_clip = text_clip.set_duration(duration)

    # Create the composite video by overlaying the text clip onto the video clip
    new_video = moviepy.editor.CompositeVideoClip([video, text_clip])

    # Save the new video with the applied text
    new_mp4_path = 'static/TTMP.mp4'
    new_video.write_videofile(new_mp4_path, codec='libx264', audio_codec='aac', remove_temp=False)

    return new_mp4_path




@app.route("/apply_text_to_video", methods=["POST", "GET"])
def apply_text_to_video():
    if request.method == "POST":
        file = request.files["mp4_file"]
        if file.filename == '':
            return redirect(request.url)
        file.save('static/TTMP.mp4')

        mp4_path = 'static/TTMP.mp4'
        text = request.form["text"]
        x = request.form["x"]
        y = request.form["y"]
        new_mp4_path = apply_text(mp4_path, text, x, y)
        return render_template("apply_text_to_video.html", new_mp4_path=new_mp4_path)
    else:
        return render_template("apply_text_to_video.html")

# Get a list of existing subdirectories in the video resources directory
existing_subdirectories = [subdir for subdir in os.listdir("/home/jack/Desktop/Project/StoryMaker/static/current_project") if os.path.isdir(os.path.join("/home/jack/Desktop/Project/StoryMaker/static/current_project", subdir))]

@app.route('/uploads', methods=['GET', 'POST'])
def upload_files():
    video_resources_dir="static/current_project"
    if request.method == 'POST':
        # Get the selected subdirectory from the form
        selected_subdirectory = request.form.get('subdirectory')

        # Check if the selected subdirectory exists
        if selected_subdirectory in existing_subdirectories:
            # Handle the uploaded file
            file = request.files['file']
            if file:
                # Save the file to the selected subdirectory
                file.save(os.path.join(video_resources_dir, selected_subdirectory, file.filename))
                # Get the URL for the uploaded image
                image_path = url_for('static', filename=os.path.join('current_project', selected_subdirectory, file.filename))
                return render_template('upload_files.html', image_path=image_path)
            else:
                return 'No file selected.'
        else:
            return 'Invalid subdirectory selected.'
    # Render the upload form with the list of existing subdirectories
    return render_template('upload_files.html', subdirectories=existing_subdirectories)

@app.route('/get_files', methods=['POST'])
def get_files():
    subdirectory = request.form.get('subdirectory')
    file_options = []
    if subdirectory and subdirectory in existing_subdirectories:
        subdirectory_path = os.path.join("static/current_project", subdirectory)
        files = os.listdir(subdirectory_path)
        file_options = [
            f'<option value="{file}">{file}</option>'
            for file in files
            if os.path.isfile(os.path.join(subdirectory_path, file))
        ]
    return ''.join(file_options)

@app.route('/image_list')
def image_list():
    image_directory = 'static/current_project/Narrators'
    image_list = [
        filename
        for filename in os.listdir(image_directory)
        if filename.endswith('.jpg')
    ]
    return render_template('image_list.html', image_list=image_list)

@app.route('/upload', methods=['POST','GET'])
def upload():
    filename = request.form['filename']
    if filename:
        src_path = 'static/current_project/Narrators/' + filename
        dest_path = 'static/TEMP.jpg'
        shutil.copyfile(src_path, dest_path)
        return redirect('/')
    else:
        return 'No file selected.'


@app.route("/mkblend_videos")
def mkblend_videos():
    # Directory for image files
    DIR = "static/current_project/junk/"
    filelist = glob.glob('animate/*.jpg')  # Get a list of all *.jpg files in the animate/ directory

    for file_path in filelist:
        os.remove(file_path)  # Delete each fil
    # Get a list of image files
    image_list = glob.glob(DIR + "*.jpg")
    
    # Shuffle and select a subset of images
    random.shuffle(image_list)
    image_list = random.sample(image_list, 40)
    
    # Print the number of selected images
    print(len(image_list))
    
    def changeImageSize(maxWidth, maxHeight, image):
        widthRatio = maxWidth / image.size[0]
        heightRatio = maxHeight / image.size[1]
        newWidth = int(widthRatio * image.size[0])
        newHeight = int(heightRatio * image.size[1])
        newImage = image.resize((newWidth, newHeight))
        return newImage
    
    # Get the size of the first image
    imagesize = Image.open(image_list[0]).size
    
    for i in range(len(image_list) - 1):
        imag1 = image_list[i]
        imag2 = image_list[i + 1]
        image1 = Image.open(imag1)
        image2 = Image.open(imag2)

        image3 = changeImageSize(imagesize[0], imagesize[1], image1)
        image4 = changeImageSize(imagesize[0], imagesize[1], image2)

        image5 = image3.convert("RGBA")
        image6 = image4.convert("RGBA")
        
        text = "animate/"
        for ic in range(0,125):
           inc = ic*.008
           sleep(.1)
           #gradually increase opacity
           alphaBlended = Image.blend(image5, image6, alpha=inc)
           alphaBlended = alphaBlended.convert("RGB")
           current_datetime = str(int(time.time())) 
           filename = current_datetime[:-3] + '.jpg'
           alphaBlended.save(f'{text}{filename}')
           if ic %25 ==0:print(i,":",ic, end = " . ")

    from moviepy.video.io.ImageSequenceClip import ImageSequenceClip
    # Get the list of files sorted by creation time
    imagelist = sorted(glob.glob('animate/*.jpg'), key=os.path.getmtime)

    # Create a clip from the images
    clip = ImageSequenceClip(imagelist, fps=30)

    # Write the clip to a video file using ffmpeg
    current_datetime = str(int(time.time())) 
    filename = "static/animate/TEMP3a.mp4"
    clip.write_videofile(filename, fps=24, codec='libx265', preset='medium')
    store = "animate/"+current_datetime[:-3] + 'june25.mp4'
    output_file = "static/animate/TEMP5.mp4"  # Replace with the desired path for the converted video file
    webm_file = "static/animate/TEMP5.webm"  # Replace with the desired path for the converted video file
    ffmpeg_cmd = ['ffmpeg', '-i', filename, '-c:v', 'libx264', '-crf', '23', '-preset', 'medium', '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart','-y', output_file]
    subprocess.run(ffmpeg_cmd) 
    ffmpeg_cmd2 = ['ffmpeg', '-i', filename, '-c:v', 'libx264', '-crf', '23', '-preset', 'medium', '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart', '-y', webm_file]
    subprocess.run(ffmpeg_cmd2)   
    shutil.copy(filename, store)
    return render_template('mkblend_videos.html', video=filename)

@app.route('/generate_vid', methods=['GET', 'POST'])
def generate_vid():
    current_datetime = str(int(time.time())) 
    str_current_datetime = str(current_datetime)
    logger.debug('Generating video', str_current_datetime)
    if request.method == 'POST':
        # Load the audio file
        audio_file = request.files['audio']
        filename = os.path.join(app.config['AUDIO_PATH'])#, 'input_audio.mp3')
        logger.info(f'Audio path: {filename}')
        audio_file.save(filename)
        print("FILENAME:",filename)

        # Get the duration of the audio using ffprobe
        command = f"ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 {filename}"
        duration = subprocess.check_output(command.split())
        duration = float(duration.strip().decode())
        logger.info(f'Duration: {duration}')
        # Load the image file
        image_file = request.files['image']
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(image_file.filename))
        logger.info(f'Image path: {image_path}')
        image_file.save(image_path)

        # Create the video
        #video_path = os.path.join(app.config['VIDEO_PATH'])#, 'sample_data/input_video.mp4')
        video_path = 'sample_data/input_video.mp4'
        logger.info(f'Video path: {video_path}')
        ffmpeg_command = f"ffmpeg -loop 1 -i {image_path} -c:v libx264 -t {duration+ 0.5} -pix_fmt yuv420p -y {video_path}"
        subprocess.run(ffmpeg_command, shell=True)

        return f'Video created: {video_path}'

    return render_template('generate_vid.html')

# Define route to display upload form
@app.route('/upload_file', methods=['POST', 'GET'])
def upload_file():
    if request.method == 'POST':
        # Check if file was uploaded
        if 'file' not in request.files:
            app.logger.error('No file was uploaded')
            flash('Error: No file was uploaded')
            return redirect(request.url)

        app.logger.error('request.files[\'file\']')
        file = request.files['file']

        # Check if file was selected
        if file.filename == '':
            app.logger.error('No file was selected')
            flash('Error: No file was selected')
            return redirect(request.url)

        # Define allowed file extensions
        ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

        # Define function to check file extension
        def allowed_file(filename):
            return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

        # Check if file is allowed
        if not allowed_file(file.filename):
             #app.logger.error(f"File '{file.filename}' is not allowed")
             app.logger.error("File '" + file.filename + "' is not allowed")
             flash("Error: File '" + file.filename + "'close is not allowed")
             return redirect(request.url)

        # Save the file
        try:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            app.logger.info(f'File {filename} saved')
            app.logger.info('FILENAME:',os.path.join(app.config['UPLOAD_FOLDER'], filename))
        except Exception as e:
            app.logger.error(f'Error saving file: {e}')
            flash('Error: Unable to save file')
            return redirect(request.url)

        # Redirect to the result page
        app.logger.info(f'File-Result {filename} SAVED')
        return redirect(url_for('result', filename=filename))

    # Return the upload form for GET requests
    return render_template('upload_file.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/make_text', methods=['GET', 'POST'])
def make_text():
    DIR = 'static/text/'
    if request.method == 'POST':
        # Get the text entered in the textarea
        text = request.form.get('text')

        # Generate a filename using the first 25 letters of the text
        text = text.replace(' ', '_')
        filename = text[:25]

        # Save the text to a file
        with open(f'{DIR}{filename}.txt', 'w') as file:
            file.write(text)

        return 'Text saved successfully!'
    else:
        return render_template('make_text.html')
directories = ['static/images','static/images/squares', 'static/final_videos', 'static/Dreamlike_art', 'static/squares', 'static/images/uploads', 'static/Final_Fantasy', 'static/final_images', 'static/thumbnails']
# Route for the home page
@app.route('/')
def home():
    return render_template('choose_dir.html', directories=directories)

# Route for choosing a directory
@app.route('/choose_dir', methods=['GET', 'POST'])
def choose_dir():
    if request.method == 'POST':
        selected_directory = request.form.get('directory', directories)
        TExt = "TEXT TEST"
        logger.error('No file was selected: %s', TExt)
        logger.debug('Debug was selected: %s', TExt)
        if selected_directory is None:
            # Handle the case where no directory is selected
            logger.error('No directory selected')
            return 'No directory selected!'
        # Rest of the code...
        # Use the selected_directory variable in your logic to generate the video
        # Make sure to update the paths according to the selected directory
        logger.debug('Selected directory: %s', selected_directory)
        # Get the list of image files in the selected directory
        image_filenames = random.sample(glob.glob(selected_directory + '/*.jpg'), 10)
        logger.debug('Selected image filenames: %s', image_filenames)
        
        image_clips = []
        for filename in image_filenames:
            # Open the image file and resize it to 512x768
            logger.debug('Processing image: %s', filename)
            image = Image.open(filename)
            #image = image.resize((512, 768), Image.ANTIALIAS)
            # Convert the PIL Image object to a NumPy array
            image_array = np.array(image)
            # Create an ImageClip object from the resized image and set its duration to 1 second
            image_clip = ImageClip(image_array).set_duration(1)
            # Append the image clip to the list
            image_clips.append(image_clip)

        logger.debug('Number of image clips: %d', len(image_clips))

        # Concatenate all the image clips into a single video clip
        video_clip = concatenate_videoclips(image_clips, method='compose')
        timestr = time.strftime("%Y%m%d-%H%M%S")
        # Set the fps value for the video clip
        video_clip.fps = 24
        # Write the video clip to a file
        video_file = f'static/videos/random_images_{timestr}_video.mp4'
        output_p = 'static/videos/random_images_video.mp4'
        logger.debug('Output video file path: %s', video_file)
        logger.debug('Final video file path: %s', output_p)
        
        video_clip.write_videofile(video_file, fps=24)
        
        try:
            shutil.copy(video_file, output_p)
        except Exception as e:
            logger.error('Error occurred while copying file: %s', str(e))
            return f"Error occurred while copying file: {str(e)}"

        # Return the rendered template with the list of directories and output path
        return render_template('choose_dir.html', directories=directories, output_path=output_p)

    # If the request method is GET, render the form template with the list of directories
    output_p = 'static/videos/random_images_video.mp4'
    return render_template('choose_dir.html', directories=directories, output_path=output_p)


  
@app.route('/convert', methods=['GET', 'POST'])
def convert():
    if request.method == 'POST':
        try:
            audio_file = request.files['audio_file']
            audio_file_path = f'static/audio_mp3/{audio_file.filename}'  # Path for audio file
            audio_file.save(audio_file_path)  # Save the audio file to the specified location

            formatted_text_file = request.files['formatted_text_file']
            formatted_text_file_path = f'static/formatted_text/{formatted_text_file.filename}'  # Path for formatted text file
            formatted_text_file.save(formatted_text_file_path)  # Save the formatted text file to the specified location

            output_filename = datetime.datetime.now().strftime('%Y-%m-%d') + '.mp4'
            output_path = 'static/videos/' + output_filename
            # Define the ffmpeg command
            # Create the blank video
            #ffmpeg -f lavfi -i color='#470000'@0x0:s=1280x720:rate=60,format=rgba -t 280 -y blank.mp4
            command = [
    'ffmpeg',
    '-i', audio_file_path,
    '-f', 'lavfi',
    '-i', f"color='#470000'@0.0:s=1280x720:rate=60,format=rgba",
    '-vf', f"drawtext=textfile='{os.path.abspath(formatted_text_file_path)}':y=(h-220)-12*t:x=580:fontcolor=orange:fontfile=/home/jack/Arimo-Regular.ttf:fontsize=26",
    '-t', '280',
    '-y', output_path
]

            logger.debug(f"Command: {' '.join(command)}")

            subprocess.run([str(arg) for arg in command], check=True)
            video = f'{output_filename}'
            return render_template('convert.html', video=output_path)
        except Exception as e:
            logger.exception("An error occurred during video conversion:")
            return render_template('error.html', message="An error occurred during video conversion.")
    else:
        return render_template('convert_form.html')

@app.route('/convert512', methods=['GET', 'POST'])
def convert512():
    if request.method == 'POST':
        try:
            audio_file = request.files['audio_file']
            audio_file_path = f'static/audio_mp3/{audio_file.filename}'  # Path for audio file
            audio_file.save(audio_file_path)  # Save the audio file to the specified location
            # Get the duration of the audio using ffprobe
            command = f"ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 {audio_file_path}"
            duration = subprocess.check_output(command.split())
            duration = float(duration.strip().decode())
            length = int(duration + 5)
            logger.info(f'Duration-512: {length}')
            formatted_text_file = request.files['formatted_text_file']
            formatted_text_file_path = f'static/formatted_text/{formatted_text_file.filename}'  # Path for formatted text file
            formatted_text_file.save(formatted_text_file_path)  # Save the formatted text file to the specified location

            output_filename = datetime.datetime.now().strftime('%Y-%m-%d') + '.mp4'
            output_path = 'static/videos/' + output_filename
            # Define the ffmpeg command
            # Create the blank video
            #ffmpeg -f lavfi -i color='#470000'@0x0:s=1280x720:rate=60,format=rgba -t 280 -y blank.mp4
            #y=(h-120)-12*t:x=24:
            command = [
    'ffmpeg',
    '-i', audio_file_path,
    '-f', 'lavfi',
    '-i', f"color='#470000'@0.0:s=512x1024:rate=60,format=rgba",
    '-vf', f"drawtext=textfile='{os.path.abspath(formatted_text_file_path)}':y=(h-120)-10*t:x=24:fontcolor=orange:fontfile=/home/jack/Arimo-Regular.ttf:fontsize=20",
    '-t', f'{length}',
    '-y', output_path
]

            logger.debug(f"Command: {' '.join(command)}")

            subprocess.run([str(arg) for arg in command], check=True)
            video = f'{output_filename}'
            return render_template('convert512.html', video=output_path)
        except Exception as e:
            logger.exception("An error occurred during video conversion:")
            return render_template('error.html', message="An error occurred during video conversion.")
    else:
        return render_template('convert_form512.html')  
  

@app.route('/mk_text', methods=['GET', 'POST'])
def mk_text():
    DIR = "static/text/"
    if request.method == 'POST':
        text = request.form.get('text')
        tex = text.replace(" ", "_")
        filename = tex[:25]
        with open(f'{DIR}{filename}.txt', 'w') as file:
            file.write(text)
        return render_template('mk_text.html', text=text, filename=f'{filename}.txt')
    else:
        return render_template('mk_text.html')

@app.route('/list_files')
def list_files():
    static_text_dir = 'static/text/'
    files = os.listdir(static_text_dir)
    files = [file for file in files if os.path.isfile(os.path.join(static_text_dir, file))]
    return str(files)

@app.route('/format_file', methods=['POST', 'GET'])
def format_file():
    static_text_dir = 'static/text/'
    static_format_dir = 'static/formatted_text/'    
    if request.method == 'POST':
        filename = request.form.get('filename')
        file_path = os.path.join(static_text_dir, filename)
        if not os.path.isfile(file_path):
            return render_template('error.html', message=f'File "{filename}" does not exist')
        with open(file_path, 'r') as file:
            content = file.read()
        words = content.split()
        formatted_content = '\n'.join([' '.join(words[i:i+5]) for i in range(0, len(words), 5)])
        modified_filename = filename.replace('.txt', '') + 'FORMATTED.txt'
        modified_file_path = os.path.join(static_format_dir, modified_filename)
        with open(modified_file_path, 'w') as modified_file:
            modified_file.write(formatted_content)
            logger.debug('This is Formated Content: %s', formatted_content)
            logger.debug('This is Formated file: %s', modified_file_path)
        return render_template('success.html', original_file=filename, modified_file=modified_filename)
    
    file_options = []
    for file_name in os.listdir(static_text_dir):
        if file_name.endswith('.txt'):
            file_options.append(file_name)
    
    return render_template('form.html', file_options=file_options)

@app.route('/view_text')
def view_text():
    text_files_dir = 'static/text/'
    text_files = []
    for filename in os.listdir(text_files_dir):
        if filename.endswith('.txt'):
            text_files.append(filename)
    return render_template('select_file.html', text_files=text_files)

@app.route('/view_text/<filename>')
def display_text(filename):
    text_file_path = f'static/text/{filename}'
    try:
        with open(text_file_path, 'r') as file:
            file_contents = file.read()
        return render_template('view_text.html', file_contents=file_contents, filename=filename)
    except FileNotFoundError:
        return f'Text file {filename} not found.'

@app.route('/edit_file', methods=['GET', 'POST'])
def edit_file():
    if request.method == 'POST':
        filename = request.form.get('filename')
        text = request.form.get('text')
        with open(f'static/text/{filename}', 'w') as file:
            file.write(text)
    text_files_dir = 'static/text/'
    text_files = []
    for filename in os.listdir(text_files_dir):
        if filename.endswith('.txt'):
            text_files.append(filename)
    return render_template('edit_file.html', text_files=text_files)

@app.route('/edit_formatted', methods=['GET', 'POST'])
def edit_formatted():
    if request.method == 'POST':
        filename = request.form.get('filename')
        text = request.form.get('text')
        with open(f'static/formatted_text/{filename}', 'w') as file:
            file.write(text)
    text_files_dir = 'static/formatted_text/'
    text_files = []
    for filename in os.listdir(text_files_dir):
        if filename.endswith('.txt'):
            text_files.append(filename)
    return render_template('edit_formatted.html', text_files=text_files)

@app.route('/get_formatted_content/<filename>')
def get_formatted_content(filename):
    file_path = os.path.join('static/formatted_text', filename)
    with open(file_path, 'r') as file:
        content = file.read()
    return content

@app.route('/get_file_content/<filename>')
def get_file_content(filename):
    file_path = os.path.join('static/text', filename)
    with open(file_path, 'r') as file:
        content = file.read()
    return content


@app.route("/mkblend_video", methods=['GET', 'POST'])
def mkblend_video():
    #directory = request.files.get('directory')
    #print("XXXXXXdirectory", directory)
    #logger.debug('Selected directory: %s', directory)

    # Save the uploaded directory to a temporary location
    temp_dir = tempfile.mkdtemp()
    #directory_path = os.path.join(temp_dir, directory.filename)
    #directory.save(directory_path)
    logger.debug('Directory saved to: %s', directory_path)
    # Process the directory path as needed
    #image_list = glob.glob(directory_path + "/*.jpg")
    directory = "leonardo_files/"
    print(directory)
    if directory:
            image_list = glob.glob(directory + "*.jpg")
            # Shuffle and select a subset of images
            random.shuffle(image_list)
            image_list = random.sample(image_list, 50)
            logger.debug('Selected image filenames: %s', image_list)
            # Print the number of selected images
            print(len(image_list))

            def changeImageSize(maxWidth, maxHeight, image):
                widthRatio = maxWidth / image.size[0]
                heightRatio = maxHeight / image.size[1]
                newWidth = int(widthRatio * image.size[0])
                newHeight = int(heightRatio * image.size[1])
                newImage = image.resize((newWidth, newHeight))
                return newImage

            # Get the size of the first image
            if image_list:
                imagesize = Image.open(image_list[0]).size

                for i in range(len(image_list) - 1):
                    imag1 = image_list[i]
                    imag2 = image_list[i + 1]
                    image1 = Image.open(imag1)
                    image2 = Image.open(imag2)

                    image3 = changeImageSize(imagesize[0], imagesize[1], image1)
                    image4 = changeImageSize(imagesize[0], imagesize[1], image2)

                    image5 = image3.convert("RGBA")
                    image6 = image4.convert("RGBA")

                    text = "animate/"
                    for ic in range(0, 125):
                        inc = ic * 0.008
                        sleep(0.1)
                        # Gradually increase opacity
                        alphaBlended = Image.blend(image5, image6, alpha=inc)
                        alphaBlended = alphaBlended.convert("RGB")
                        current_time = datetime.datetime.now()
                        filename = current_time.strftime('%Y%m%d_%H%M%S%f')[:-3] + '.jpg'
                        alphaBlended.save(f'{text}{filename}')
                        if ic % 25 == 0:
                            print(i, ":", ic, end=" . ")

                from moviepy.video.io.ImageSequenceClip import ImageSequenceClip
                # Get the list of files sorted by creation time
                imagelist = sorted(glob.glob('animate/*.jpg'), key=os.path.getmtime)

                # Create a clip from the images
                clip = ImageSequenceClip(imagelist, fps=30)

                # Write the clip to a video file using ffmpeg
                current_time = datetime.datetime.now()
                filename = "static/animate/TEMP3a.mp4"
                clip.write_videofile(filename, fps=24, codec='libx265', preset='medium')
                store = "animate/" + current_time.strftime('%Y%m%d_%H%M%S%f')[:-3] + 'june25.mp4'
                output_file = "static/animate/TEMP5.mp4"  # Replace with the desired path for the converted video file
                webm_file = "static/animate/TEMP5.webm"  # Replace with the desired path for the converted video file
                ffmpeg_cmd = [
                    'ffmpeg', '-i', filename, '-c:v', 'libx264', '-crf', '23', '-preset', 'medium', '-c:a', 'aac',
                    '-b:a', '128k', '-movflags', '+faststart', '-y', output_file
                ]
                subprocess.run(ffmpeg_cmd)
                ffmpeg_cmd2 = [
                    'ffmpeg', '-i', filename, '-c:v', 'libx264', '-crf', '23', '-preset', 'medium', '-c:a', 'aac',
                    '-b:a', '128k', '-movflags', '+faststart', '-y', webm_file
                ]
                subprocess.run(ffmpeg_cmd2)
                shutil.copy(filename, store)
                return render_template('mkblend_video.html', video=filename)

    return render_template('choose_directory.html')




@app.route('/indeX')
def indeX():
    return render_template('indeX.html')

    

@app.route('/resize_and_overlay_videos')
def resize_and_overlay_videos():
    # Path to the videos
    static_video_path = 'static/videos/2023-07-07.mp4'
    input_video_path = 'static/animate/topvideo.mp4'
    output_video_path = 'static/output/resulta.mp4'

    # Resize the input video using FFmpeg
    resize_command = f'ffmpeg -i {input_video_path} -vf "scale=410:820" -y resized.mp4'
    subprocess.call(resize_command, shell=True)

    # Overlay the resized video on the background video using FFmpeg
    overlay_command = f'ffmpeg -i {static_video_path} -i resized.mp4 -filter_complex "overlay=25:25" -y {output_video_path}'
    subprocess.call(overlay_command, shell=True)

    # Remove the temporary resized video
    subprocess.call('rm resized.mp4', shell=True)

    # Return the final video as a response
    return send_file(output_video_path, mimetype='video/mp4')


@app.route('/resize_and_overlay_videos_page')
def resize_and_overlay_videos_page():
    output_video_path = 'static/output/resulta.mp4'
    return render_template('resize_and_overlay_videos.html',video = output_video_path)

@app.route('/build_stackedvids')
def build_stackedvids():
    # Get a random video and image from the static folder
    video_filename = random.choice(glob.glob('static/square_vids/*.mp4'))
    image_filename = random.choice(glob.glob('static/squares/*.jpg'))
    
    # Load the video and image files as clips
    video_clip = VideoFileClip(video_filename)
    image_clip = ImageClip(image_filename)
    
    # Set the duration of the image clip to match the duration of the video clip
    image_clip = image_clip.set_duration(video_clip.duration)
    
    # Resize the clips to 640x640 and 640x640 respectively
    video_clip = video_clip.resize((640, 640))
    image_clip = image_clip.resize((640, 640))
    
    # Create a black clip to fill the remaining space below the image
    black_clip = ColorClip(size=(640, 640), color=(0, 0, 0)).set_duration(video_clip.duration)
    
    # Combine the clips vertically using CompositeVideoClip
    final_clip = CompositeVideoClip([
        video_clip.set_position(('center', 'top')),
        image_clip.set_position(('center', 640)),
        black_clip.set_position(('center', 640 + 640))
    ], size=(640, 1280))
    
    # Export the final clip as a video file
    timestr = time.strftime("%Y%m%d-%H%M%S")
    video_filename = 'static/stacked_vids/stacked_vids'+timestr+'video.mp4'
    final_clip_path = 'static/stacked_vids/stacked_videos.mp4'
    final_clip.write_videofile(final_clip_path)
    final_clip.write_videofile(video_filename)
    
    return render_template('/build_stackedvids.html', stackedvid_url=final_clip_path)

from moviepy.editor import *
@app.route('/build_stackedvid')
def build_stackedvid():
    # Get a random video and image from the static folder
    video_filename = random.choice(glob.glob('static/square_vids/*.mp4'))
    videofilename = random.choice(glob.glob('static/square_vids/*.mp4'))
    
    
    # Load the video and image files as clips
    video_clip = VideoFileClip(video_filename)
    videoclip = VideoFileClip(videofilename)
    
    # Set the duration of the image clip to match the duration of the video clip
    videoclip = videoclip.set_duration(video_clip.duration)
    
    # Resize the clips to 640x640 and 640x640 respectively
    video_clip = video_clip.resize((640, 640))
    videoclip = videoclip.resize((640, 640))
    
    # Create a black clip to fill the remaining space below the image
    black_clip = ColorClip(size=(640, 640), color=(0, 0, 0)).set_duration(video_clip.duration)
    
    # Combine the clips vertically using CompositeVideoClip
    final_clip = CompositeVideoClip([
        video_clip.set_position(('center', 'top')),
        videoclip.set_position(('center', 640)),
        black_clip.set_position(('center', 640 + 640))
    ], size=(640, 1280))
    
    # Export the final clip as a video file
    timestr = time.strftime("%Y%m%d-%H%M%S")
    video_filename = 'static/stacked_vids/stacked_vids'+timestr+'video.mp4'
    final_clip_path = 'static/stacked_vids/stacked_videos.mp4'
    final_clip.write_videofile(final_clip_path)
    final_clip.write_videofile(video_filename)
    
    return render_template('/build_stackedvid.html', stackedvid_url=final_clip_path)

@app.route('/clean_images', methods=['POST'])
def clean_images_route():
    clean_images()
    app.logger.error('line 210 clean_images_route')
    return redirect(url_for('index'))

@app.route('/get_gallery')
def get_gallery():
    image_dir = '/mnt/HDD500/flask/FLASK/static/images/uploads'
    image_names = os.listdir(image_dir)
    return render_template('get_gallery.html', image_names=image_names)

@app.route('/uploads/<filename>')
def send_image(filename):
    return send_from_directory('static/images/uploads', filename)

@app.route('/uploads/thumbnails/<filename>')
def send_image_thumb(filename):
    return send_from_directory('static/images/uploads/thumbnails', filename)
@app.route('/flask_info')
def flask_info():
    return render_template('flask_info.html')
@app.route('/add_effects')
def add_effects():
    return '''
        <form method="post" action="/video" enctype="multipart/form-data">
            <label for="input_video">Select input video file:</label><br>
            <input type="file" id="input_video" name="input_video"><br><br>
            <input type="submit" value="Submit">
        </form>
    '''

@app.route('/video', methods=['GET', 'POST'])
def process_video():
    DIR = "static/"
    input_video = request.files['input_video']
    
    # Save the uploaded video to a file
    input_video.save(f"{DIR}input_video.mp4")
    
    # Run FFmpeg commands
    command1 = f"ffmpeg -nostdin -i {DIR}input_video.mp4 -filter:v \"minterpolate='mi_mode=mci:mc_mode=aobmc:vsbmc=1:fps=10'\" -c:v libx264 -r 20 -pix_fmt yuv420p -c:a copy -y {DIR}output.mp4"    
    
    subprocess.run(command1, shell=True, stderr=subprocess.PIPE, universal_newlines=True)
    
    command2 = f"ffmpeg -nostdin -i {DIR}output.mp4 -vf mpdecimate,setpts=N/FRAME_RATE/TB -c:v libx264 -r 30 -pix_fmt yuv420p -c:a copy -y {DIR}mpdecimate.mp4"
    
    subprocess.run(command2, shell=True, stderr=subprocess.PIPE, universal_newlines=True)
    
    #DIR = "/home/jack/Desktop/ffmpeg_flask/"
    command3 = f"ffmpeg -i static/mpdecimate.mp4 -filter_complex \"[0:v]trim=duration=14,loop=500:1:0[v];[1:a]afade=t=in:st=0:d=1,afade=t=out:st=0.9:d=2[a1];[v][0:a][a1]concat=n=1:v=1:a=1\" -c:v libx264 -r 30 -pix_fmt yuv420p -c:a aac -b:a 192k -shortest -y static/output.mp4"
    subprocess.run(command3, shell=True, stderr=subprocess.PIPE, universal_newlines=True)
    
    now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    shutil.copy(f"{DIR}output.mp4", f"{DIR}{now}_output.mp4")
    logging.info(f'my_video: f"{DIR}mpdecimate.mp4"') 
    video_file="static/outputALL.mp4"     
    command4 = f'ffmpeg -i "{DIR}mpdecimate.mp4" -i "{DIR}mpdecimate.mp4" -i "{DIR}mpdecimate.mp4" -i "{DIR}mpdecimate.mp4" -i "{DIR}mpdecimate.mp4" -filter_complex "[0:v]trim=duration=15[v0];[1:v]trim=duration=15[v1];[2:v]trim=duration=15[v2];[3:v]trim=duration=15[v3];[4:v]trim=duration=15[v4];[v0][v1][v2][v3][v4]concat=n=5:v=1:a=0" -c:v libx264 -pix_fmt yuv420p -shortest -y {video_file}'
    subprocess.run(command4, shell=True, stderr=subprocess.PIPE, universal_newlines=True)
    now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    diR = f"{DIR}/square_videos/"
    logging.info(f'diR: f"{diR}mpdecimate.mp4"')
    shutil.copy(f"{video_file}", f"{diR}{now}_outputALL.mp4")
    logging.info(f'diR: {diR}mpdecimate.mp4')
    return render_template('final.html', video_file=video_file)

def get_all_mp4_videos():
    mp4_videos = []
    for root, dirs, files in os.walk('static'):
        for file in files:
            if file.endswith('.mp4'):
                mp4_videos.append(os.path.join(root, file))
    return mp4_videos

@app.route('/play/<path:video_path>')
def play(video_path):
    return send_file(video_path)

@app.route('/select_order', methods=['GET', 'POST'])
def select_order():
    output_path = 'static/videos/concatenated_video.mp4'  # Set a default value for output_path
    if request.method == 'POST':
        # Get the order of the videos from the form data
        order = request.form.getlist('order')
        # Join the videos in the specified order
        join_videos(order, output_path)
        # Set the timestamped output path
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        new_output_path = f'static/videos/concatenated_{timestamp}XX.mp4'
        shutil.copy(output_path, new_output_path)
        # Redirect to the download page
        return redirect(url_for('download'))
    else:
        # Get the paths to the video files in the directory
        video_dir = 'static/videos'
        video_files = [os.path.join(video_dir, filename) for filename in os.listdir(video_dir) if filename.endswith('.mp4')]
        # Render the template with the list of video files and the output path
        return render_template('select_order.html', video_files=video_files, output_path=output_path)
         
def join_videos(video_paths, output_path):
    # Generate a list of input arguments for FFmpeg
    input_args = []
    for path in video_paths:
        input_args.extend(['-i', path])
    # Join the videos using FFmpeg
    subprocess.run(['ffmpeg', *input_args, '-filter_complex', 'concat=n={}:v=1:a=0'.format(len(video_paths)), '-c:v', 'libx264', '-crf', '23', '-preset', 'veryfast', '-y', output_path])
    #output_path = 'static/videos/concatenated_video.mp4'
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    new_output_path = f'static/videos/concatenated_{timestamp}XX.mp4'
    shutil.copy(output_path, new_output_path)    
@app.route('/videos', methods=['POST'])
def process_videos():
    DIR = "static/"
    input_video = request.files['input_video']
    ""
    # Save the uploaded video to a file
    input_video.save(f"{DIR}input_video2.mp4")
    
    command1 = f"ffmpeg -nostdin -i {DIR}input_video2.mp4 -filter:v \"minterpolate='mi_mode=mci:mc_mode=aobmc:vsbmc=1:fps=10'\" -c:v libx264 -r 20 -pix_fmt yuv420p -c:a copy -y {DIR}alice/output2.mp4"    
    subprocess.run(command1, shell=True, stderr=subprocess.PIPE, universal_newlines=True)
    
    command2 = f"ffmpeg -hide_banner -i {DIR}alice/output2.mp4 -filter:v \"setpts=5*PTS,minterpolate='fps=25:scd=none:me_mode=bidir:vsbmc=1:search_param=200'\" -t 58 -y {DIR}alice/final2.mp4"
    subprocess.run(command2, shell=True, stderr=subprocess.PIPE, universal_newlines=True)
    
    command3 = f"ffmpeg -hide_banner -i {DIR}alice/final2.mp4 -filter:v \"setpts=5*PTS,minterpolate='fps=25:scd=none:me_mode=bidir:vsbmc=1:search_param=200'\" -t 58 -y {DIR}alice/final5.mp4"
    subprocess.run(command3, shell=True, stderr=subprocess.PIPE, universal_newlines=True)

    # Add music to the video
    init = randint(10,50)
    MUSIC=["static/music/Born_a_Rockstar-Instrumental-NEFFEX.mp3","static/music/Cattle-Telecasted.mp3","static/music/Bite_Me-Clean-NEFFEX.mp3","static/music/El_Secreto-Yung_Logos.mp3","static/music/Blue_Mood-Robert_Munzinger.mp3","static/music/Escapism-Yung_Logos.mp3","static/music/Enough-NEFFEX.mp3","static/music/As_You_Fade_Away-NEFFEX.mp3","static/music/Culture-Anno_Domini_Beats.mp3","static/music/Contrast-Anno_Domini_Beats.mp3","static/music/Diving_in_Backwards-Nathan_Moore.mp3","static/music/Aztec_Empire-Jimena_Contreras.mp3","static/music/Devil_s_Organ-Jimena_Contreras.mp3","static/music/Alpha_Mission-Jimena_Contreras.mp3","static/music/Changing-NEFFEX.mp3","static/music/Anxiety-NEFFEX.mp3","static/music/6-Shots-NEFFEX.mp3","static/music/DimishedReturns.mp3","static/music/Drum_Meditation.mp3","static/music/ChrisHaugen.mp3","static/music/DoveLove-Moreira.mp3","static/music/DesertPlanet.mp3","static/music/David_Fesliyan.mp3"]
    
    music = random.choice(MUSIC)
    command3 = f"ffmpeg -i {DIR}alice/final5.mp4 -ss {init} -i {music} -af 'afade=in:st=0:d=4,afade=out:st=55:d=3' -map 0:0 -map 1:0 -shortest -y {DIR}alice/Final_End.mp4"
    subprocess.run(command3, shell=True)
    
    # Save the output video to a file   
    now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    shutil.copy(f"{DIR}alice/output2.mp4", f"{DIR}alice/{now}_output.mp4")
    shutil.copy(f"{DIR}alice/Final_End.mp4", f"{DIR}alice/{now}_Final.mp4")
    shutil.copy(f"{DIR}alice/Final_End.mp4", f"{DIR}alice/Final_End_mix.mp4")
    return render_template('final.html', video_file="alice/Final_End.mp4")
@app.route('/large_video')
def large_video():
    return render_template('large_video.html')
@app.route('/add_border')
def add_border():
    images = [f for f in os.listdir('static/images/uploads/') if os.path.isfile(os.path.join('static/images/uploads/', f))]
    thumbnails = []
    for image in images:
        with Image.open('static/images/uploads/'+image) as img:
            img.thumbnail((200, 200))
            thumbnail_name = 'thumbnail_'+image
            img.save('static/thumbnails/'+thumbnail_name)
            thumbnails.append(thumbnail_name)
    return render_template('add_border.html', images=images, thumbnails=thumbnails)


@app.route('/select_border')
def select_border():
    borders = os.listdir('static/transparent_borders/')
    return render_template('select_border.html', borders=borders)

@app.route('/apply_border', methods=['POST', 'GET'])
def apply_border():
    selected_image = request.form['image']
    selected_border = request.form['border']
    try:
        with Image.open('static/images/uploads/'+selected_image) as img:
            with Image.open('static/transparent_borders/'+selected_border) as border:
                img = img.resize(border.size)
                img.paste(border, (0, 0), border)
                final_image_name = 'final_'+selected_image
                img.save('static/final_images/'+final_image_name)
        return render_template('final_image.html', final_image=final_image_name, message='Border applied successfully.')
    except Exception as e:
        error_message = f'An error occurred: {str(e)}. Please try again.'
        return render_template('apply_border.html', image=selected_image, border=selected_border, error_message=error_message)

@app.route('/select_border_image', methods=['GET'])
def select_border_image():
    try:
        image = request.args.get('image')
        if not image:
            raise ValueError('No image selected.')
        return render_template('select_border.html', image=image, borders=os.listdir('static/transparent_borders/'))
    except Exception as e:
        error_message = f'An error occurred: {str(e)}. Please try again.'
        return render_template('add_border.html', error_message=error_message)
@app.route('/overlay_text', methods=['GET'])
def overlay_text():
    # Load the blank image
    blank_image_path = 'static/new_video/Border-plain.png'
    blank_image = Image.open(blank_image_path)

    # Load the text file and format its contents
    text_file_path = 'static/new_video/text_file.txt'
    with open(text_file_path, 'r') as file:
        text_contents = file.read()

    formatted_text = f"{text_contents}"  # Format the contents as desired

    # Set the font properties
    font_size = 21
    font_color = (255, 255, 255)  # White color
    font_path = '/home/jack/fonts/source-sans-pro-semibold.ttf'

    font = ImageFont.truetype(font_path, font_size)

    # Create a new image with the same size as the blank image and transparent background
    text_overlay = Image.new('RGBA', blank_image.size, (0, 0, 0, 0))

    # Draw the formatted text onto the overlay image
    draw = ImageDraw.Draw(text_overlay)
    text_position = (50, 600)  # Adjust the position as needed
    draw.text(text_position, formatted_text, font=font, fill=font_color)

    # Merge the overlay image with the blank image
    final_image = Image.alpha_composite(blank_image.convert('RGBA'), text_overlay)

    # Save the final image
    output_image_path = 'static/new_video/output_image.png'
    final_image.save(output_image_path)

    return render_template('overlay_text.html', output_image_path=output_image_path)
@app.route('/create_text_file', methods=['GET', 'POST'])
def create_text_file():
    if request.method == 'POST':
        # Get the text content from the textarea
        text_content = request.form.get('textarea_content')

        # Create the file path
        text_file_path = os.path.join('static/new_video', 'text_file.txt')

        # Write the text content to the file
        with open(text_file_path, 'w') as file:
            file.write(text_content)

        return render_template('text_file_created.html', text_file_path=text_file_path)
    
    return render_template('create_text_file.html')    
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'jpg'

@app.route('/generate_video3', methods=['GET', 'POST'])
def generate_video3():
    if request.method == 'POST':
        # Check if any files were uploaded
        if 'file' not in request.files:
            error_message = "No files uploaded."
            logging.error(error_message)
            return render_template('generate_video3.html', error_message=error_message)

        files = request.files.getlist('file')

        # Check if files were selected
        if len(files) == 0:
            error_message = "No files selected."
            logging.error(error_message)
            return render_template('generate_video3.html', error_message=error_message)

        # Check if the files have supported extensions
        for file in files:
            if not allowed_file(file.filename):
                error_message = f"Invalid file extension for {file.filename}. Only JPG files are allowed."
                logging.error(error_message)
                return render_template('generate_video3.html', error_message=error_message)

        # Create a temporary directory to save the uploaded files
        temp_dir = os.path.join('static', 'temp')
        os.makedirs(temp_dir, exist_ok=True)

        # Save the uploaded files to the temporary directory
        saved_files = []
        for file in files:
            filename = secure_filename(file.filename)
            file_path = os.path.join(temp_dir, filename)
            file.save(file_path)
            saved_files.append(file_path)

        # Randomly select 30 image files
        selected_images = random.sample(saved_files, min(30, len(saved_files)))

        # Create a list of image clips from the selected images
        image_clips = []
        for image_file in selected_images:
            image_clip = mp.ImageClip(image_file, duration=1)
            image_clips.append(image_clip)

        # Concatenate the image clips into a video clip
        video_clip = mp.concatenate_videoclips(image_clips)

        # Set the output video path
        output_path = os.path.join('static', 'videos', 'generated_video.mp4')

        # Write the video clip to the output file
        video_clip.write_videofile(output_path, fps=24)

        # Delete the uploaded files after processing
        for file_path in saved_files:
            os.remove(file_path)

        # Return the generated video URL to the client
        video_url = url_for('static', filename='videos/generated_video.mp4')
        return render_template('generate_video3.html', video_url=video_url)

    # Render the initial form
    return render_template('generate_video3.html')

@app.route('/generate_video2')
def generate_video2():
    # Get the pythonlist of image files in the static/final_images/ directory  
    #image_filenames = random.sample(glob.glob('static/final_images/*.jpg'),25)
    #image_filenames = random.sample(glob.glob('static/images/uploads/*.jpg'),30)
    #image_filenames = random.sample(glob.glob('static/alien_files/*.jpg'),30)
    image_filenames= random.sample(glob.glob('/mnt/HDD500/collections/absrtact/*.jpg'),30)
    print(image_filenames,end="-")
   
    image_clips = []
    for filename in image_filenames:
        # Open the image file and resize it to 512x768
        image = Image.open(filename)
        image = image.resize((512, 768), Image.ANTIALIAS)
        print(image)
        # Convert the PIL Image object to a NumPy array
        image_array = np.array(image)
        # Create an ImageClip object from the resized image and set its duration to 1 second
        image_clip = ImageClip(image_array).set_duration(1)
        
        # Append the image clip to the list
        image_clips.append(image_clip)
    
    # Concatenate all the image clips into a single video clip
    video_clip = concatenate_videoclips(image_clips, method='compose')
    timestr = time.strftime("%Y%m%d-%H%M%S")
    # Set the fps value for the video clip
    video_clip.fps = 24
    # Write the video clip to a file
    video_path = 'static/videos/random_images'+timestr+'video.mp4'
    video_clip.write_videofile(video_path, fps=24)
    video_clip.write_videofile('static/videos/TEMPvideo.mp4', fps=24)
    
    # Return a message to the client
    return render_template('generate_video2.html', video_url='static/videos/TEMPvideo.mp4')
    #return render_template('generate_video2.html' ,video_url='/static/videos/TEMPvideo.mp4', video_path=video_path)


@app.route('/ffmpeg_ctl', methods=['GET', 'POST'])
def ffmpeg_ctl():
    if request.method == 'POST':
        # Access the numeric input value from the form data
        number = request.form.get('number')
        # Process the value as needed
        # ...

    return render_template('ffmpeg_ctl.html')

@app.route('/mkmoz', methods=['GET', 'POST'])
def mkmoz():
    im = Image.new("RGB", (2048,2048), (250,250,250))
    for i in range(0,2500):
        if i< 500:DIR = "/home/jack/.cache/thumbnails/large/*.png"
        if i> 500:DIR = "/home/jack/.cache/thumbnails/normal/*.png"
        #if i> 2495:DIR = "/home/jack/.cache/thumbnails/large/*.png"
        thumb = random.choice(glob.glob(DIR))
        print("THUMB:",thumb)
        Thum = Image.open(thumb)            
        im.paste(Thum,((randint(0,im.size[0])),randint(0,im.size[1])-50))
        filename = "static/images/ThumbNails.png"
        im.save(filename)
        Filename="images/ThumbNails.png"
    return render_template("mkmoz.html", filename=Filename)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config['DATABASE'])
    return db
# Define the route for the form
@app.route('/select_by_id_form', methods=['POST','GET'])
def select_by_id_form():
    return render_template('select_by_id_form.html')

# Handle the form submission
@app.route('/select_by_id', methods=['POST','GET'])
def handle_select_by_id():
    row_id = request.form['row_id']

    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM snippets WHERE rowid = ?", (row_id,))
    data = cursor.fetchone()

    if data is not None:
        # Retrieve the individual data values
        id_value = data[0]
        description = data[1]
        code = data[2]
        keywords = data[3]
    else:
        # Set default values if no data found
        id_value = row_id
        description = ""
        code = ""
        keywords = ""

    return render_template('display_data.html', id_value=id_value, description=description, code=code, keywords=keywords)

@app.route('/search_by_rowid')
def search_by_rowid():
    return render_template('search_by_rowid.html')

@app.route('/edit_data/<int:rowid>', methods=['GET', 'POST'])
def edit_data(rowid):
    db = get_db()
    cursor = db.cursor()

    if request.method == 'POST':
        description = request.form['description']
        code = request.form['code']
        keywords = request.form['keywords']

        cursor.execute("UPDATE snippets SET description = ?, code = ?, keywords = ? WHERE rowid = ?",
                       (description, code, keywords, rowid))
        db.commit()

        return redirect('/search_database')

    cursor.execute("SELECT * FROM snippets WHERE rowid = ?", (rowid,))
    data = cursor.fetchone()

    return render_template('edit_data.html', data=data)




@app.route('/search_database', methods=['POST','GET'])
def search_database():
    search_term = request.form['search_term']
    search_area = request.form['search_area']

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
        return redirect('/search_database')

    results = cursor.fetchall()
    return render_template('db_results.html', results=results)

#@app.route('/edit_data/<int:rowid>', methods=['GET', 'POST'])
#def edit_data(rowid):

@app.route('/insert_data', methods=['POST', 'GET'])
def insert_data():
    if request.method == 'POST':
        description = request.form['description']
        code = request.form['code']
        keywords = request.form['keywords']

        db = get_db()
        cursor = db.cursor()

        cursor.execute("INSERT INTO snippets (description, code, keywords) VALUES (?, ?, ?)",
                       (description, code, keywords))
        db.commit()

        # Get the rowid of the newly inserted row
        rowid = cursor.lastrowid

        return redirect(url_for('edit_data', rowid=rowid))

    return render_template('insert_data.html')


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/view_thumbs')
def view_thumbs():
    # Define the directory where the images are located
    image_directory = 'static/images/uploads'
    # Get a list of all the image files in the directory
    image_files = [f for f in os.listdir(image_directory) if f.endswith('.jpg') or f.endswith('.png')]
    # Create a list of dictionaries containing the image file name and URL
    image_list = [{'name': f, 'url': f'/images/uploads/{f}'} for f in image_files]
    # Render the template with the list of images
    return render_template('view_thumbs.html', image_list=image_list)

@app.route('/add_text', methods=['GET', 'POST'])
def add_text():
    if request.method == 'POST':
        text = request.form['text']
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        text = f'Text Entry: {timestamp} {text}'
        with open('chat.txt', 'a') as file:
            file.write(f'\n{text}')
        return render_template('add_text.html', message='Text added successfully')
    else:
        return render_template('add_text.html')

@app.route('/search_txt', methods=['GET', 'POST'])
def search_txt():
    if request.method == 'POST' and 'phrase' in request.form:
        phrase = request.form['phrase']
        with open('chat.txt', 'r') as file:
            lines = file.readlines()
        results = []
        for i, line in enumerate(lines):
            if phrase in line:
                start = max(0, i-5)
                end = min(len(lines), i+6)
                context = lines[start:end]
                for j, context_line in enumerate(context):
                    if phrase in context_line:
                        results.append(f'Line {start+j}: {context_line}')
                    else:
                        results.append(f'Line {start+j}: {context_line}')
        return render_template('results.html', results=results)
    return render_template('search_txt.html')

@app.route('/blend_pil', methods=['POST', 'GET'])
def blend_pil():
    if request.method == 'POST':
        # Get the uploaded images
        img1 = request.files['img1']
        img2 = request.files['img2']
        img3 = request.files['img3']

        # Open the images using PIL
        img1_pil = Image.open(img1)
        img2_pil = Image.open(img2)
        img3_pil = Image.open(img3)

        # Blend the images
        blended_pil = Image.blend(img1_pil, img2_pil, 1/3)
        blended_pil = Image.blend(blended_pil, img3_pil, 1/3)

        # Return the blended image as a response
        # Since we are not saving it to the server, we can use a BytesIO object to avoid creating a temporary file
        img_io = BytesIO()
        blended_pil.save(img_io, 'JPEG', quality=70)
        current_datetime = datetime.now()
        str_current_datetime = str(current_datetime)
        file_name = "static/images/uploads/blended_pil"+str_current_datetime+"XXXX.jpg"
        blended_pil.save(file_name, format='JPEG')
        img_io.seek(0)
        
        # Generate the HTML for displaying the blended image in the template
        blended_image_data = base64.b64encode(img_io.getvalue()).decode('utf-8')
        blended_image_url = f"data:image/jpeg;base64,{blended_image_data}"
        #blended_image_url = blended_image_url.resize(( blended_image_url.size[0]//2, blended_image_url.size[1]//2), Image.ANTIALIAS) 
        # Pass the URL of the blended image to the template
        return render_template('show_blend_pil.html', blended_image_url=blended_image_url)      
    return render_template('blend_pil.html')

@app.route('/process_images', methods=['POST', 'GET'])
def process_images():
    if request.method == 'POST':
        # read the images from the request
        img1 = Image.open(request.files['image1'].stream).convert('RGB')
        img2 = Image.open(request.files['image2'].stream).convert('L')
        img3 = Image.open(request.files['image3'].stream).convert('RGB')
    
        # resize the images to have the same shape
        img1 = img1.resize((img2.width, img2.height))
        img3 = img3.resize((img2.width, img2.height))
    
        # convert the mask to binary
        threshold = 127
        mask = Image.eval(img2, lambda px: 255 if px > threshold else 0)
    
        # apply the mask
        img = Image.composite(img1, img3, mask)
    
        # save the image to a file
        output = BytesIO()
        current_datetime = datetime.now()
        str_current_datetime = str(current_datetime)
        file_name = "static/images/"+str_current_datetime+"XXXX.jpg"
        img.save(file_name, format='JPEG')
        img.save(output, format='JPEG')
        output.seek(0)
    
        # encode the image to bytes
        img_bytes = output.getvalue()
    
        # return the image as a response
        return Response(img_bytes, mimetype='image/jpeg')
    return render_template('process_images.html')

@app.route('/image_directories', methods=['GET', 'POST'])
def image_directories():
    image_directories = ['static/Prodia_640x640', 'static/LineArt', 'static/Quantized', 'static/squares', 'static/BrightColors']
    if request.method == 'POST':
        # Rest of the code

        directory = request.form['directory']
        # Check that the directory parameter is not empty
        if directory:
            app.logger.info('Redirecting endpoint with directory: %s', directory)
            # Check that the directory is a valid directory path
            if os.path.isdir(directory):
                # Pass the directory value to the square_video endpoint
                app.logger.info('Redirecting to square_video endpoint with directory: %s', directory)
                return redirect(url_for('square_video', directory=directory))
            else:
                # Render an error template if the directory parameter is not a valid directory path
                app.logger.error('Invalid directory parameter: %s', directory)
                return render_template('error.html', message='Please enter a valid directory path.')
        else:
            # Render an error template if the directory parameter is empty
            app.logger.error('Directory parameter is empty')
            return render_template('error.html', message='Please enter a directory path.')
    else:
        # Pass the list of image directories to the template
        return render_template('image_directories.html', image_directories=image_directories)

@app.route('/select_playmp3', methods=['GET', 'POST'])
def select_playmp3():
    # Get the list of mp3 files in the static/audio_mp3/ directory
    mp3_files = [f for f in os.listdir('static/audio_mp3/') if f.endswith('.mp3')]
    if request.method == 'POST':
        # Get the selected MP3 file from the dropdown list
        mp3_file = request.form['mp3_file']
        # Play the selected mp3 file
        pygame.mixer.init()
        pygame.mixer.music.load('static/audio_mp3/' + mp3_file)
        pygame.mixer.music.play()
        # Wait for the audio to finish playing
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        # Stop pygame and exit the program
        pygame.mixer.quit()
        pygame.quit()
    # Render the template with the list of mp3 files
    return render_template('select_playmp3.html', mp3_files=mp3_files)


@app.route("/make_animation")
def make_animation():
    # Get a list of all files in the final_images directory
    #image_files = os.listdir("static/final_images/")
    #DIR = "/home/jack/Desktop/HDD500/collections/gypsy_files/"
    #DIR = "/home/jack/Desktop/HDD500/collections/hippy_files/"
    DIR = "/mnt/HDD500/collections/jungle/exotic_lithograph_prints-Playground_AI_files/512x768/"
    image_files = os.listdir(DIR)
    #image_files = os.listdir("/mnt/HDD500/collections/640x640-alien/")
    # Select 20 random files from the list
    selected_files = random.sample(image_files, 30)
    
    # Load each selected file, resize it to 400x600, and save it to a temporary directory
    resized_images = []
    for filename in selected_files:
        with Image.open(DIR + filename) as img:
            img = img.resize((400, 600))
            temp_filename = "static/tmp/" + filename
            img.save(temp_filename)
            resized_images.append(temp_filename)
    
    # Create an animated GIF from the resized images
 
    gif_filename = "static/animated_gifs/animated.gif"
    with imageio.get_writer(gif_filename, mode='I', duration=1) as writer:
        for filename in resized_images:
            image = imageio.imread(filename)
            writer.append_data(image)
    import shutil

    timestr = time.strftime("%Y%m%d-%H%M%S")

  
    src = 'static/animated_gifs/animated.gif'
    dst = 'static/animated_gifs/animated' + timestr + '.gif'
    # 2nd option
    shutil.copy(src, dst) 
    # Return a template that displays the GIF
    return render_template("make_animation.html", gif_filename=gif_filename)

@app.route('/title_page', methods=['GET', 'POST'])
def title_page():
    if request.method == 'POST':
        # Get the text input and image file from the form data
        text = request.form['text']
        image = request.files['image']
        
        # Save the image to a temporary location
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(image.filename))
        image.save(image_path)
        
        # Open the image file
        image = Image.open(image_path)
               
        # Create a drawing context on the image
        draw = ImageDraw.Draw(image)
        
        # Define the font and font size for the text
        font = ImageFont.truetype('static/fonts/OpenSansBold.ttf', 50)
        # Split the text by newline characters
        lines = text.split("  ")


        # Calculate the size of each line and get the maximum width
        line_sizes = [draw.textsize(line, font) for line in lines]
        max_line_width = max([size[0] for size in line_sizes])

        # Calculate the total size of the text
        text_width = max_line_width
        text_height = sum([size[1] for size in line_sizes])

        # Calculate the position of the text in the center of the image
        x = (640 - text_width) / 2
        y = (640 - text_height) / 2

        # Calculate the size of the text
        text_width, text_height = draw.textsize(text, font)
        
        # Calculate the position of the text in the center of the image
        x = (640 - text_width) / 2
        y = (640 - text_height) / 2
        
        # Add the text to the image
        draw.text((x, y), text, font=font, fill=(0, 0, 0, 255))
        
        # Save the image to the static folder with a unique filename
        inc = text.replace(" ","")
        filenamex = os.path.join(app.static_folder, 'title_pages', f'{inc}_{hash(text)}.png')
        image.save(filenamex)
        filename = 'static/title_pages/title_page.png'
        shutil.copy(filenamex , filename)
        logging.error('filename: %s', filename)
        
        #print(inc[:5])
        # Remove the temporary image file
        #os.remove(image_path)
        filenamev = 'title_pages/title_page.png'
        # Return the rendered template with the image filename
        return render_template('title_page.html', filename=filenamev)
    filenamev = 'title_pages/title_page.png'    
    return render_template('title_page.html', filename=filenamev)


@app.route('/add_title', methods=['GET', 'POST'])
def add_title():
    # Create the final_videos directory if it does not exist
    final_videos_dir = os.path.join(app.static_folder, 'final_videos')
    if not os.path.exists(final_videos_dir):
        os.makedirs(final_videos_dir)

    if request.method == 'POST':
        app.logger.debug('Entering POST request handler for /add_title')
        # Get the paths of the selected video and title page
        video_path = os.path.join(app.static_folder, 'videos', request.form['video'])
        title_page_path = os.path.join(app.static_folder, 'title_pages', request.form['title_page'])
        app.logger.debug(f'video_path: {video_path}')
        app.logger.debug(f'title_page_path: {title_page_path}')

        # Load the video and title page as clips
        video_clip = VideoFileClip(video_path)
        title_page_clip = ImageClip(title_page_path).set_duration(2)

        # Add the title page to the video for the first 2 seconds
        final_clip = concatenate_videoclips([title_page_clip, video_clip.subclip(2)])

        # Save the final video to the final_videos directory
        final_filename = f"{os.path.splitext(request.form['video'])[0]}_{os.path.splitext(request.form['title_page'])[0]}.mp4"
        final_path = os.path.join(final_videos_dir, final_filename)
        app.logger.debug(f'final_path: {final_path}')
        final_clip.write_videofile(final_path)

        # Return a response to the user indicating that the video with title page was created
        message = f"The video with title page was created and saved to {final_path}"
        return render_template('add_title.html', message=message)

    # If the request method is GET, render the add_title.html template
    app.logger.debug('Entering GET request handler for /add_title')
    videos = os.listdir(os.path.join(app.static_folder, 'square_vids'))
    title_pages = os.listdir(os.path.join(app.static_folder, 'title_pages'))
    app.logger.debug(f'videos: {videos}')
    app.logger.debug(f'title_pages: {title_pages}')
    return render_template('add_title.html', videos=videos, title_pages=title_pages)
def get_rowid():
    # Connect to the database
    db = sqlite3.connect('code.db')
    cursor = db.cursor()
    row_id = request.form['row_id']
    # Execute a query to retrieve the rowid
    cursor.execute("SELECT rowid FROM snippets WHERE rowid = ?", (rowid,))


    # Fetch the result
    result = cursor.fetchone()

    # Close the database connection
    db.close()

    # Check if a rowid was found
    if result:
        rowid = result[0]
    else:
        # Handle the case when no rowid is found
        rowid = None

    return rowid

@app.route('/indexdb')
def indexdb():
    return render_template('indexdb.html')

@app.route('/indexA')
def indexA():
    image_dir = 'static/images'
    image_files = [f for f in os.listdir(image_dir) if f.endswith('.jpg')]
    random_image_file = random.choice(image_files)
    app.logger.info(f"Random image file selected: {random_image_file}")
    return render_template('indexA.html', random_image_file=random_image_file)


@app.route('/index_FLASK')
def index_FLASK():
    image_dir = 'static/images'
    image_files = [f for f in os.listdir(image_dir) if f.endswith('.jpg')]
    random_image_file = random.choice(image_files)
    app.logger.info(f"Random image file selected: {random_image_file}")

    return render_template('index_FLASK.html')

@app.route('/edit_data_page', methods=['GET', 'POST'])
def edit_data_page():
    if request.method == 'POST':
        rowid = request.form['rowid']
        return redirect(url_for('edit_data', rowid=rowid))

    return render_template('edit_data_page.html')
# Configuration
app.config['DATABASE'] = 'code.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect("code.db")
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.before_first_request
def create_table():
    db = get_db()
    cursor = db.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            price REAL
        )
    ''')

    db.commit()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(app, '_database', None)
    if db is not None:
        db.close()


@app.route('/indexD')
def indexD():
    return redirect('/products')


@app.route('/products', methods=['GET', 'POST'])
def products():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']

        db = get_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO products (name, description, price) VALUES (?, ?, ?)",
                       (name, description, price))
        db.commit()

    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()

    return render_template('products.html', products=products)


@app.route('/edit/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']

        db = get_db()
        cursor = db.cursor()
        cursor.execute("UPDATE products SET name=?, description=?, price=? WHERE id=?",
                       (name, description, price, product_id))
        db.commit()

        return redirect('/products')

    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM products WHERE id=?", (product_id,))
    product = cursor.fetchone()

    return render_template('edit_product.html', product=product)


@app.route('/delete/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM products WHERE id=?", (product_id,))
    db.commit()

    return redirect('/products')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5100)

