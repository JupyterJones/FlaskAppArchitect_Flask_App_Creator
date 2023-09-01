import datetime

output_filename = datetime.datetime.now().strftime('%Y-%m-%d') + '.mp4'
print(output_filename)

ffmpeg -i static/videos/2023-07-09.mp4 -vf crop 460


@app.route('/convert512', methods=['GET', 'POST'])
def convert512():
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
    '-i', f"color='#470000'@0.0:s=512x1024:rate=60,format=rgba",
    '-vf', f"drawtext=textfile='{os.path.abspath(formatted_text_file_path)}':y=(h-120)-12*t:x=480:fontcolor=orange:fontfile=/home/jack/Arimo-Regular.ttf:fontsize=26",
    '-t', '280',
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
