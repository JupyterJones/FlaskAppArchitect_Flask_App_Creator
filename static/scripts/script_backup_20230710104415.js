// Create the image element
        var image = document.createElement('img');
        image.src = 'static/images/perfect_fish.png';
        image.alt = 'Floating Fish';
        image.classList.add('floating-image');

        // Apply CSS styles to the image
        image.style.position = 'absolute';
        image.style.width = '100px';
        image.style.height = 'auto';
        image.style.top = '0';
        image.style.left = '0';
        image.style.transition = 'transform 0.5s ease-in-out';

        // Append the image element to the body
        document.body.appendChild(image);