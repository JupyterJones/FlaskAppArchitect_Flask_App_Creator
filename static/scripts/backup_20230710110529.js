var styleElement = document.createElement('style');
styleElement.textContent = `
    .floating-image {
        position: absolute;
    }
`;

var h1Element = document.createElement('h1');
h1Element.textContent = 'Floating Fish';

var imgElement = document.createElement('img');
imgElement.src = 'static/images/perfect_fish.png'; // Update the file extension to .png
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

    var posX = Math.random() * (windowWidth - fishWidth);
    var posY = Math.random() * (windowHeight - fishHeight);

    fish.style.top = posY + 'px';
    fish.style.left = posX + 'px';

    setTimeout(function() {
        requestAnimationFrame(updateFishPosition);
    }, 500); // Delay of 500 milliseconds
}

updateFishPosition();
