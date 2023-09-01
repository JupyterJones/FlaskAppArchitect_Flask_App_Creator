from flask import Flask, render_template, request
import os
import numpy as np
import cv2
import datetime
import matplotlib.pyplot as plt
from werkzeug.utils import secure_filename
import logging

app = Flask(__name__)

# Logging setup
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s [%(levelname)s] %(message)s',
                    handlers=[
                        logging.FileHandler('app.log'),
                        logging.StreamHandler()
                    ])
logger = logging.getLogger(__name__)

UPLOAD_FOLDER = os.path.join('static', 'uploads')
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/feather_files', methods=['GET', 'POST'])
def feather_files():
    if request.method == 'POST':
        selected_directories = request.form.getlist('directories')  # Use 'directories' instead of 'directory'
        selected_directories = sorted(selected_directories)
        if selected_directories:
            images = os.listdir(os.path.join('static', 'images', selected_directories[0]))
            return render_template('feather_files.html', directories=get_image_directories(), selected_directory=selected_directories[0], images=images)
        
        selected_image = request.form.get('image')
        if selected_image:
            selected_directory = request.form.get('selected_directory')  # Add this line to retrieve selected_directory
            image_path = os.path.join('static', 'images', selected_directory, selected_image)
            feathered_image_path = feather_image(image_path)
            return render_template('feather_files.html', directories=get_image_directories(), selected_directory=selected_directory, images=os.listdir(os.path.join('static', 'images', selected_directory)), feathered_image_path=feathered_image_path)
    
    return render_template('feather_files.html', directories=get_image_directories())

def get_image_directories():
    dirs = os.listdir(os.path.join('static', 'images'))
    DIR = sorted(dirs)
    return DIR

def feather_image(input_path):
    try:
        logger.info("Feathering image: %s", input_path)
        
        # Load the image
        giger = cv2.imread(input_path)
        l_row, l_col, nb_channel = giger.shape
        rows, cols = np.mgrid[:l_row, :l_col]
        radius = np.sqrt((rows - l_row/2)**2 + (cols - l_col/2)**2)
        alpha_channel = np.zeros((l_row, l_col))
        
        # Calculate alpha channel values
        r_min, r_max = 1./3 * radius.max(), 0.6 * radius.max()
        alpha_channel[radius < r_min] = 1
        alpha_channel[radius > r_max] = 0
        gradient_zone = np.logical_and(radius >= r_min, radius <= r_max)
        alpha_channel[gradient_zone] = (r_max - radius[gradient_zone]) / (r_max - r_min)
        alpha_channel *= 255
        
        # Create feathered image
        feathered = np.empty((l_row, l_col, nb_channel + 1), dtype=np.uint8)
        feathered[..., :3] = giger[:]
        feathered[..., -1] = alpha_channel[:]
        
        # Save the feathered image
        timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        output_path = os.path.join('static', 'images', 'feathers', f'{timestamp}.png')
        plt.imsave(output_path, feathered, format="png")
        logger.info("Feathered image saved at: %s", output_path)

        return output_path
    except Exception as e:
        logger.error("An error occurred during feathering: %s", str(e))
        return None


if __name__ == '__main__':
    app.run(debug=True)
