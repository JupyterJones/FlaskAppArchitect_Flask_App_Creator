# create_comic.py

from flask import Blueprint, render_template, request, redirect, url_for, send_file
from PIL import Image, ImageDraw
import os

create_comic_bp = Blueprint('create_comic', __name__)

@create_comic_bp.route('/create_comic_index', methods=['GET', 'POST'])
def create_comic_index():
    if request.method == 'POST':
        # Handle form submission and generate the border image here
        border_name = request.form.get('border_name') # type: ignore
        border_shape = request.form.get('border_shape') # type: ignore
        border_thickness = int(request.form.get('border_thickness')) # type: ignore
        border_color = request.form.get('border_color') # type: ignore
        width_input = request.form.get('border_width') # type: ignore
        height_input = request.form.get('border_height') # type: ignore
        
        # Ensure that both inputs are valid integers
        try:
            width = int(width_input)
            height = int(height_input)
        except ValueError:
            return "Invalid size input, please enter valid numbers for width and height."

        border_image = generate_border(border_name, border_shape, (width, height), border_thickness, border_color)

        #border_image = generate_border(border_shape, (width,height), border_thickness, border_color)

        # Save the generated image to the 'static/borders' directory
        save_path = os.path.join('static', 'borders', f'{border_name}.png')
        border_image.save(save_path)

        # Redirect to the '/show_generated_image' route to display the image

        return redirect(url_for('create_comic.show_generated_image', save_path=save_path))

    return render_template('create_comic_index.html')



def generate_border(border_name, shape, size, thickness, color):
    # Create a transparent image
    border_image = Image.new('RGBA', size, (0, 0, 0, 0))

    draw = ImageDraw.Draw(border_image)

    # Define the border shape based on user input
    if shape == 'square':
        draw.rectangle((0, 0, size[0] - 1, size[1] - 1), outline=color, width=thickness)
    elif shape == 'rectangle':
        draw.rectangle((0, 0, size[0] - 1, size[1] // 2), outline=color, width=thickness)
    elif shape == 'triangle':
        # Define the vertices of the triangle
        vertices = [(0, size[1]), (size[0] // 2, 0), (size[0], size[1])]

        # Draw the triangle
        draw.polygon(vertices, outline=color, width=thickness)

    # Save the generated image with the specified name
    save_path = os.path.join('static', 'borders', f'{border_name}.png')
    border_image.save(save_path)

    return save_path  # Return the path to the saved image

@create_comic_bp.route('/show_generated_image/<border_name>')
def show_generated_image(border_name):
    # Implement logic to display the generated image here
    # You can create an HTML page to display the image

    return render_template('show_generated_image.html', border_name=border_name)


