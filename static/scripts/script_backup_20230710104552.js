// Create the <style> element and set the CSS styles
var styleElement = document.createElement('style');
styleElement.textContent = `
    .floating-image {
        position: absolute;
    }
`;

// Create the <h1> element and set the text content
var h1Element = document.createElement('h1');
h1Element.textContent = 'Floating Fish';

// Create the <img> element and set the attributes
var imgElement = document.createElement('img');
imgElement.src = 'images/perfect_fish.png';
imgElement.alt = 'Floating Fish';
imgElement.id = 'fish';
imgElement.classList.add('floating-image');

// Append the elements to the <body> element
document.body.appendChild(styleElement);
document.body.appendChild(h1Element);
document.body.appendChild(imgElement);

// Define the updateFishPosition function
function updateFishPosition() {
    var windowWidth = window.innerWidth;
    var windowHeight = window.innerHeight;
    var fish = document.getElementById('fish');
    var fishWidth = fish.offsetWidth;
    var fishHeight = fish.offsetHeight;

    // Generate random coordinates within the window bounds
    var posX = Math.random() * (windowWidth - fishWidth);
    var posY = Math.random() * (windowHeight - fishHeight);

    // Set the new position
    fish.style.top = posY + 'px';
    fish.style.left = posX + 'px';

    // Continue the animation
    requestAnimationFrame(updateFishPosition);
}

// Start the animation
updateFishPosition();
