from moviepy.editor import *
import os

# Path to the directory containing images
image_dir = 'static/images/gothic_lolita'

# Get a list of image files in the directory
image_files = [f for f in os.listdir(image_dir) if f.endswith('.jpg')]

# Sort image files based on their filenames
image_files.sort()

# Duration for each image in seconds
image_duration = 2

# Initialize the final video with the first image
first_image_path = os.path.join(image_dir, image_files[0])
first_image = ImageClip(first_image_path).set_duration(image_duration)

# Get the dimensions of the first image
video_width, video_height = first_image.size

# Create an empty VideoClip to hold the final video
final_video = VideoClip()

# Iterate through the images to create zoom and pan transitions
for i, image_file in enumerate(image_files):
    image_path = os.path.join(image_dir, image_file)
    image = ImageClip(image_path).set_duration(image_duration)

    # Resize the image to match the video dimensions
    image = image.resize((video_width, video_height))

    # Calculate the scale factor for zooming
    scale_factor = 1.1  # Adjust as needed

    # Define the time intervals for the zoom and pan effect
    zoom_duration = 0.5  # Adjust as needed
    zoom_start_time = i * image_duration
    zoom_end_time = zoom_start_time + zoom_duration

    # Apply zoom in and out during the defined time interval
    zoomed_image = image.fx(vfx.crop, x_center=0.5, y_center=0.5, width=video_width * scale_factor, height=video_height * scale_factor)
    zoomed_image = zoomed_image.set_start(zoom_start_time).set_end(zoom_end_time)

    # Concatenate the zoomed image to the final video
    final_video = concatenate_videoclips([final_video, zoomed_image])

# Write the final video to an output file
final_video.write_videofile('static/output/video.mp4', codec='libx264', fps=24)
