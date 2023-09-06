import os
from flask import Flask, render_template, request, redirect, url_for
import glob
import logging
from logging.handlers import RotatingFileHandler
from werkzeug.utils import secure_filename
import shutil
import uuid
import random
import cv2
from PIL import Image
from moviepy.editor import VideoFileClip, AudioFileClip, clips_array, concatenate_videoclips, CompositeVideoClip, ImageClip

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

# Define a route for your Flask app

SDIR = "static/"
# Define the file path to store the script content
script_file = os.path.join(os.getcwd(),SDIR, 'scripts', 'scripts.js')
app.secret_key = os.urandom(24)

app = Flask(__name__)

def get_an_image():
    #image_dir =random.choice(glob.glob("/home/jack/Desktop/StoryMaker/static/images/*"))
    image_dir =glob.glob("/home/jack/Desktop/StoryMaker/static/images/*")
    #images = glob.glob(image_dir)
    image_dir = sorted(image_dir)
    return image_dir

def list_image_directories():
    image_directories = get_an_image()
    return image_directories


@app.route('/')
def fade_index():
    # List available image directories
    image_directories = list_image_directories()
    logger.debug("LINE 56: ",image_directories)
    video='assets/framed_final_output.mp4'
    video2='assets/final_output.mp4'
    return render_template('fade_index.html', image_directories=image_directories, video=video, video2=video2)

def get_an_mp3():
    mp3s = random.choice(glob.glob("static/free_no_attribute_music/*"))
    return mp3s 



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

        # Shuffle the image files to mix them randomly
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

        # Keep track of video duration
        video_duration = 0

        # Create the video with fading transitions
        for i in range(len(resized_images)):
            if video_duration >= 58:  # Limit video to 58 seconds
                break

            img1 = resized_images[i]
            img2 = resized_images[(i + 1) % len(resized_images)]  # Wrap around to the first image
            # changing the alpha step size will change the duration of the fade effect
            step_size = 5
            for alpha in range(0, 150):  # Gradually change alpha from 0 to 100 for fade effect
                alpha /= 150.0
                blended = cv2.addWeighted(img1, 1 - alpha, img2, alpha, 0)
                out.write(blended)
                video_duration += 1 / 30  # Assuming 30 FPS

        out.release()

        # Prepare an audio clip of the same duration (58 seconds)
        audio_clip = AudioFileClip(get_an_mp3())  # Replace with your audio file path
        audio_clip = audio_clip.subclip(0, 58)  # Limit audio to 58 seconds






        # Load the video clip
        video_clip = VideoFileClip(out_path)

        # Set the audio of the video clip
        video_clip = video_clip.set_audio(audio_clip)

        # Save the final video with music
        final_output_path = 'static/assets/final_output.mp4'
        uid = str(uuid.uuid4())  # Generate a unique ID using uuid
        mp4_file = os.path.join("static", "assets", f"{uid}.mp4")
      
        
        video_clip.write_videofile(final_output_path, codec='libx264')
        shutil.copyfile(final_output_path, mp4_file) 
        #return render_template('fade_index.html', video='assets/final_output.mp4',video2='assets/framed_final_output.mp4')
        return redirect(url_for('frame_final_output'))

    except Exception as e:
        # Handle any exceptions
        return "An error occurred. Please check the logs for details."
    
@app.route('/frame_final_output')
def frame_final_output():
    logger.debug("WE MADE IT HERE !")
    try:
        # Load the final output video
        final_output_path = 'static/assets/final_output.mp4'
        final_video_clip = VideoFileClip(final_output_path)
        logger.debug(final_video_clip.size)

        # Load the PNG overlay frame
        overlay_frame_path = 'static/overlay/frame.png'  # Replace with the actual path to your overlay frame
        overlay_frame = ImageClip(overlay_frame_path)  # Load the overlay frame as an image

        # Resize the overlay frame to match the video's dimensions
        overlay_frame = overlay_frame.resize(final_video_clip.size)
        logger.debug("FRAME SIZE: ", overlay_frame.size)

        # Create a list of overlay frames with the desired duration
        overlay_frames = [overlay_frame.set_duration(58)]

        # Concatenate the overlay frames to match the final video's duration
        overlay = concatenate_videoclips(overlay_frames, method="compose")

        # Composite the overlay onto the final video
        final_video_with_overlay = CompositeVideoClip([final_video_clip.set_duration(58), overlay])
        uid = str(uuid.uuid4())  # Generate a unique ID using uuid
        frame_file = os.path.join("static", "assets", f"{uid}framed.mp4")
        # Write the video with the overlay to a new file
        framed_final_output_path = 'static/assets/framed_final_output.mp4'
        final_video_with_overlay.write_videofile(framed_final_output_path, codec='libx264')
        shutil.copyfile(framed_final_output_path, frame_file) 
        return render_template('fade_index.html', video='assets/final_output.mp4',video2='assets/framed_final_output.mp4')

    except Exception as e:
        # Handle any exceptions
        logger.debug("Exception: ", e)
        return "An error occurred. Please check the logs for details."
@app.route('/large')
def large():
    return render_template('large.html')
if __name__ == '__main__':
    print("Served on port 5500")
    app.run(debug=True, host='0.0.0.0' ,port=5500)
