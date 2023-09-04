var styleElement = document.createElement('style');
styleElement.textContent = `
    .floating-image {
        position: absolute;
    }
`;

var h1Element = document.createElement('h1');
h1Element.textContent = 'Floating Fish';

var imgElement = document.createElement('img');
imgElement.src = 'static/images/fish.png';
imgElement.alt = 'Floating Fish';
imgElement.id = 'fish';
imgElement.classList.add('floating-image');
imgElement.setAttribute('width', '200');
imgElement.setAttribute('height', '200');

document.body.appendChild(styleElement);
document.body.appendChild(h1Element);
document.body.appendChild(imgElement);

function updateFishPosition() {
    var windowWidth = window.innerWidth;
    var windowHeight = window.innerHeight;
    var fish = document.getElementById('fish');
    var fishWidth = fish.offsetWidth;
    var fishHeight = fish.offsetHeight;

    var posX = parseFloat(fish.style.left) || windowWidth / 2 - fishWidth / 2; // Start position in the center horizontally
    var posY = parseFloat(fish.style.top) || windowHeight / 2 - fishHeight / 2; // Start position in the center vertically

    // Generate random floating directions (-1 or 1)
    var directionX = Math.random() > 0.5 ? 1 : -1;
    var directionY = Math.random() > 0.5 ? 1 : -1;

    // Calculate the new position
    posX += directionX * 1; // Move the fish horizontally by 1 pixel
    posY += directionY * 1; // Move the fish vertically by 1 pixel

    // Wrap the fish around the window bounds
    if (posX + fishWidth < 0) {
        posX = windowWidth;
    } else if (posX > windowWidth) {
        posX = -fishWidth;
    }
    if (posY + fishHeight < 0) {
        posY = windowHeight;
    } else if (posY > windowHeight) {
        posY = -fishHeight;
    }

    // Set the new position
    fish.style.top = posY + 'px';
    fish.style.left = posX + 'px';

    setTimeout(function() {
        requestAnimationFrame(updateFishPosition);
    }, 5); // Delay of 5 milliseconds (adjust as needed for the desired speed)
}

updateFishPosition();
