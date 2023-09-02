import json
from flask import Flask, render_template, request, Response
import logging
from PIL import Image, ImageDraw

import io
app = Flask(__name__)

# Configure logging
logging.basicConfig(filename='search_log.txt', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
@app.route('/favicon.ico')
def favicon():
    # Set the size of the favicon
    size = (16, 16)

    # Create a new image with a transparent background
    favicon = Image.new('RGBA', size, (0, 0, 0, 0))

    # Create a drawing object
    draw = ImageDraw.Draw(favicon)

    # Draw a yellow square
    square_color = (255, 0, 255)
    draw.rectangle([(0, 0), size], fill=square_color)

    # Draw a red circle
    circle_center = (size[0] // 2, size[1] // 2)
    circle_radius = size[0] // 3
    app.logger.info(f'circle_center, circle_radius:,{circle_center} {circle_radius}')
    circle_color = (255, 255, 0)
    draw.ellipse(
        [(circle_center[0] - circle_radius, circle_center[1] - circle_radius),
         (circle_center[0] + circle_radius, circle_center[1] + circle_radius)],
        fill=circle_color
    )

    # Save the image to a memory buffer
    image_buffer = io.BytesIO()
    favicon.save(image_buffer, format='ICO')
    image_buffer.seek(0)

    return Response(image_buffer.getvalue(), content_type='image/x-icon')

@app.route('/search_chat')
def search_chat():
    print("ONE")
    try:
        # Load the conversations JSON file
        with open('static/chat/conversations.json', 'r') as f:
            conversations = json.load(f)

        # Get the search query from the request parameters
        query = request.args.get('q')

        # Search the conversations for the query and collect results
        results = []
        for conversation in conversations:
            if 'messages' in conversation:
                for message in conversation['messages']:
                    if 'content' in message and query.lower() in message['content'].lower():
                        results.append(message)

        # Log the search results
        logging.info(f'Search query: {query}')
        logging.info(f'Search results: {results}')

        # Render the search results in the template
        return render_template('search_chat.html', query=query, results=results)
    except Exception as e:
        # Log any exceptions
        logging.error(f'Error occurred: {str(e)}')
        return render_template('search_chat.html')
if __name__ == '__main__':
    print("running on port 5300")
    app.run(debug=True, port=5300)

