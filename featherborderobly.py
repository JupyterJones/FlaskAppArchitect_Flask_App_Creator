import os
import logging
from flask import Flask, request, render_template, send_from_directory
from PIL import Image, ImageDraw

app = Flask(__name__)

# Configure logging
log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'feather.log')
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configure upload and download folders
UPLOAD_FOLDER = 'uploadz'
DOWNLOAD_FOLDER = 'downloadz'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def feather_image(input_path, output_path, feather_amount):
    try:
        logging.info("Opening image: %s", input_path)
        image = Image.open(input_path).convert("RGBA")

        width, height = image.size
        logging.info("Image dimensions: %dx%d", width, height)

        # Create a gradient mask for feathering
        mask = Image.new("L", (width, height))
        draw = ImageDraw.Draw(mask)
        for x in range(feather_amount):
            alpha = int((255 / feather_amount) * x)
            draw.line((width - x, 0, width - x, height), fill=alpha)

        # Apply the gradient mask to the image
        feathered_image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        feathered_image.paste(image, (0, 0))
        feathered_image.putalpha(mask)

        # Save the feathered image
        feathered_image.save(output_path)

        logging.info("Feathering completed successfully!")

    except Exception as e:
        logging.error("An error occurred: %s", str(e))

@app.route('/upload_files', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file part"

        file = request.files['file']

        if file.filename == '':
            return "No selected file"

        if file and allowed_file(file.filename):
            # Save uploaded file
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filename)

            # Paths for feathered image
            output_filename = os.path.join(app.config['DOWNLOAD_FOLDER'], 'feathered.png')
            feather_amount = 50

            # Call the function to feather the image
            feather_image(filename, output_filename, feather_amount)

            return send_from_directory(app.config['DOWNLOAD_FOLDER'], 'feathered.png', as_attachment=True)

    return render_template('upload_files.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5100)
