import os
import subprocess

# Path to the directory containing images
image_dir = '/home/jack/Desktop/StoryMaker/static/images/yoda'

# Get a list of image files in the directory
image_files = [f for f in os.listdir(image_dir) if f.endswith('.jpg')]

# Sort image files based on their filenames
image_files.sort()

# Output video file
output_video = 'static/output/yoda_video.mp4'

# Frame rate for the output video (adjust as needed)
frame_rate = 24

# Zoom and pan filter settings
zoom_factor = 1.1  # Adjust the zoom factor as needed
zoom_duration = 5  # Duration of the zoom effect (seconds)

# Initialize the FFmpeg command
ffmpeg_cmd = [
    'ffmpeg',
    '-framerate', str(frame_rate),
]

# Iterate through the images and apply zoom and pan effects
for i, image_file in enumerate(image_files):
    image_path = os.path.join(image_dir, image_file)

    # Define zoom and pan filter
    zoom_filter = f'zoompan=z=\'min(zoom+0.0015,{zoom_factor})\':d={zoom_duration}:s=512x768'

    ffmpeg_cmd += [
        '-i', image_path,
        '-vf', zoom_filter,
    ]

# Output video settings
ffmpeg_cmd += [
    '-c:v', 'libx264',
    '-pix_fmt', 'yuv420p',
    '-y',  # Overwrite output file if it exists
    output_video,
]

# Run the FFmpeg command
subprocess.run(ffmpeg_cmd)

print(f"Video created: {output_video}")
