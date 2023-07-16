#!/home/jack/Desktop/FLASK/flask_venv/bin/python
import subprocess
import logging
from flask import Flask, render_template, send_file, request, redirect, url_for, flash
from flask import jsonify, send_from_directory
import os
from logging.handlers import RotatingFileHandler
import datetime
from werkzeug.utils import secure_filename
import time
from clean_images import clean_images
from flask import Response
import matplotlib.pyplot as plt
from io import BytesIO
import imageio
from PIL import Image
import pygame
import glob 
import moviepy.editor as mp
import shutil
import numpy as np
import random
from pydub import AudioSegment
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from gtts import gTTS
from moviepy.editor import ImageClip, AudioFileClip, CompositeVideoClip, concatenate_videoclips
from io import BytesIO
import base64
# Define the Flask application
app = Flask(__name__)
import logging

# Create a formatter for the log messages
formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')

# Create a file handler to write log messages to a file
handler = RotatingFileHandler('Logs/app.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)
# Create a logger object
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# Add the file handler to the Flask app logger
app.logger.addHandler(handler)
# Set up logging
logging.basicConfig(level=logging.DEBUG)
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'jpg'
directories = ['static/images', 'static/final_videos', 'static/tmp', 'static/BrightColors', 'static/final_images', 'static/thumbnails']
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
# Mp3 page with file upload and textarea to enter text
@app.route('/')
def index():
    image_dir = 'static/images'
    image_files = [f for f in os.listdir(image_dir) if f.endswith('.jpg')]
    random_image_file = random.choice(image_files)
    return render_template('index.html', random_image_file=random_image_file)


app.secret_key = os.urandom(24)

app.config['UPLOAD_FOLDER'] = 'static/images/uploads'
app.config['RESULTS_FOLDER'] = 'static/videos/results'
app.config['THUMBNAILS_FOLDER'] = 'static/images/thumbnails'
#app.config['CHECKPOINT_PATH'] = '/home/jack/Desktop/FlaskApp/Wav2Lip/checkpoints/wav2lip_gan.pth'
#app.config['AUDIO_PATH'] = '/home/jack/Desktop/FlaskApp/Wav2Lip/content/sample_data/input_audio.wav'

# Set the maximum file size to 16MB
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Configure the logger
formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.INFO)
handler.setFormatter(formatter)
app.logger.addHandler(handler)

@app.route('/indexA')
def indexA():
    image_dir = 'static/images'
    image_files = [f for f in os.listdir(image_dir) if f.endswith('.jpg')]
    random_image_file = random.choice(image_files)
    app.logger.info(f"Random image file selected: {random_image_file}")
    return render_template('indexA.html', random_image_file=random_image_file)
@app.route('/', methods=['GET', 'POST'])
def text_mp3():
    if request.method == 'POST':
        # Get the text from the textarea
        text = request.form['text']
        # Remove whitespace from the text
        text = text.replace(" ", "")
        # Create a filename based on the first 20 characters of the text
        filename = "static/milestones_resources/comments/TEMP.mp3"
        filename = filename.strip()  # remove the newline character
        # Create a gTTS object and save the audio file
        tts = gTTS(text)
        filename = filename.strip()
        tts.save(filename)
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
        return render_template('text_mp3.html')
        
@app.route('/large_video')
def large_video():
    return render_template('large_video.html')        
        
        
@app.route('/choose_dir', methods=['GET', 'POST'])
def choose_dir():
    if request.method == 'POST':
        selected_directory = request.form.get('directory', 'static/images')
        if selected_directory is None:
            # Handle the case where no directory is selected
            return 'No directory selected!'
        
        # rest of the code...
        logging.debug("Selected directory: %s", selected_directory)
     
        # Get the list of image files in the selected directory
        image_filenames = random.sample(glob.glob(selected_directory + '/*.jpg'),30)
        image_clips = []
        for filename in image_filenames:
            # Open the image file and resize it to 512x768
            image = Image.open(filename)
            image = image.resize((512, 768), Image.ANTIALIAS)
            logging.debug("Opened image: %s", filename)
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
        video_file = 'static/videos/random_images'+timestr+'Xvideo.mp4'
        output_p = 'static/videos/random_images_video.mp4'
        video_clip.write_videofile(video_file, fps=24)
        try:
            shutil.copy(video_file, output_p)
        except Exception as e:
            logging.error("Error occurred while copying file: %s", str(e))

        # Return a message to the client
        return render_template('choose_dir.html', directories=directories, output_path=output_p)

    output_p = 'static/videos/random_images_video.mp4'
    # If the request method is GET, render the form template with the list of directories
    return render_template('choose_dir.html', directories=directories, output_path=output_p)


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
            app.logger.error(f'File {file.filename} is not allowed')
            flash(f'Error: File {file.filename} is not allowed')
            return redirect(request.url)

        # Save the file
        try:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            app.logger.info(f'File {filename} saved')
        except Exception as e:
            app.logger.error(f'Error saving file: {e}')
            flash('Error: Unable to save file')
            return redirect(request.url)

        # Redirect to the result page
        return redirect(url_for('result', filename=filename))

    # Return the upload form for GET requests
    return render_template('upload_file.html')

@app.route('/result/<filename>')
def result(filename):
    return render_template('result.html', filename=filename)


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
def get_audio_duration(audio_file):
    audio = AudioSegment.from_file(audio_file)
    duration = audio.duration_seconds
    return duration  
@app.route('/generate_vid', methods=['GET', 'POST'])
def generate_vid():
    current_datetime = datetime.now()
    str_current_datetime = str(current_datetime)
    logger.debug('Generating video', str_current_datetime)
    if request.method == 'POST':
        # Load the audio file
        audio_file = request.files['audio']
        filename = os.path.join(app.config['AUDIO_PATH'], 'input_audio.mp3')
        logger.info(f'Audio path: {filename}')
        audio_file.save(filename)

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
        video_path = os.path.join(app.config['VIDEO_PATH'], 'input_video.mp4')
        logger.info(f'Video path: {video_path}')
        ffmpeg_command = f"ffmpeg -loop 1 -i {image_path} -c:v libx264 -t {duration+ 0.5} -pix_fmt yuv420p -y {video_path}"
        subprocess.run(ffmpeg_command, shell=True)

        return f'Video created: {video_path}'

    return render_template('generate_vid.html')

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
@app.route('/view_thumbs')
def view_thumbs():
    # Define the directory where the images are located
    image_directory = '/home/jack/Desktop/FLASK/static/images/uploads'
    # Get a list of all the image files in the directory
    image_files = [f for f in os.listdir(image_directory) if f.endswith('.jpg') or f.endswith('.png')]
    # Create a list of dictionaries containing the image file name and URL
    image_list = [{'name': f, 'url': f'/images/uploads/{f}'} for f in image_files]
    # Render the template with the list of images
    return render_template('view_thumbs.html', image_list=image_list)



@app.route('/images/uploads/<filename>')
def image(filename):
    # Define the directory where the images are located
    image_directory = '/home/jack/Desktop/FLASK/static/images/uploads'
    # Generate the full path to the requested image file
    image_path = os.path.join(image_directory, filename)
    # Determine the file type based on the file extension
    file_extension = os.path.splitext(filename)[1].lower()
    if file_extension == '.jpg':
        content_type = 'image/jpeg'
    elif file_extension == '.png':
        content_type = 'image/png'
    else:
        # If the file type is not recognized, return a 404 error
        print("abort(404)")
    # Return the image file as a response with the appropriate content type
    with open(image_path, 'rb') as f:
        image_data = f.read()
    return Response(image_data, content_type=content_type)
@app.route('/clean_images', methods=['POST'])
def clean_images_route():
    clean_images()
    app.logger.error('line 210 clean_images_route')
    return redirect(url_for('index'))
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
@app.route('/get_gallery')
def get_gallery():
    image_dir = 'static/images/uploads'
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
@app.route('/create_avatar', methods=['GET', 'POST'])
def create_avatar():
    if request.method == 'POST':
        #check_point = os.path.join(app.config['CHECKPOINT_PATH'], 'checkpoints/wav2lip_gan.pth')
        check_point = 'checkpoints/wav2lip_gan.pth'
        wav_filename = os.path.join(app.config['AUDIO_PATH'], 'input_audio.wav')
        video_path = os.path.join(app.config['VIDEO_PATH'], 'input_video.mp4')
        logger.info(f'Video path: {video_path}')
        build_avatar = f"python inference.py --checkpoint_path {check_point} --face {video_path} --audio {wav_filename}"

        def generate_output():
            process = subprocess.Popen(build_avatar, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

            for line in iter(process.stdout.readline, b''):
                yield line

        return Response(generate_output(), mimetype='text/plain')
    else:
        return render_template('create_avatar.html')
    
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
@app.route('/generate_video')
def generate_video():
    # Get the pythonlist of image files in the static/final_images/ directory  
    #image_filenames = random.sample(glob.glob('static/final_images/*.jpg'),20)
    #image_filenames = random.sample(glob.glob('static/video_resources/*.jpg'),30)
    image_filenames = random.sample(glob.glob('static/images/uploadd/*.jpg'),30)
    print(image_filenames,end="-")
   
    image_clips = []
    for filename in image_filenames:
        # Open the image file and resize it to 512x768
        image = Image.open(filename)
        image = image.resize((512, 666), Image.ANTIALIAS)
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
    video_clip.write_videofile('static/videos/random_images'+timestr+'video.mp4', fps=24)
    
    # Return a message to the client
    return 'Video generated successfully!'
# List of directories to choose from   
@app.route('/generate_video2')
def generate_video2():
    # Get the pythonlist of image files in the static/final_images/ directory  
    #image_filenames = random.sample(glob.glob('static/final_images/*.jpg'),25)
    image_filenames = random.sample(glob.glob('static/images/uploads/*.jpg'),30)
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
    return render_template('generate_video2.html', video_url='/static/videos/TEMPvideo.mp4')
    #return render_template('generate_video2.html' ,video_url='/static/videos/TEMPvideo.mp4', video_path=video_path)
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
    final_clip_path = 'static/stacked_vids/stacked_video.mp4'
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
 
@app.route('/add_effects')
def add_effects():
    return '''
        <form method="post" action="/video" enctype="multipart/form-data">
            <label for="input_video">Select input video file:</label><br>
            <input type="file" id="input_video" name="input_video"><br><br>
            <input type="submit" value="Submit">
        </form>
    ''' 
 
 
    
if __name__ == '__main__':
    app.run(debug=True)


