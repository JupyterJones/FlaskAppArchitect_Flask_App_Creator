var counter = 0;

function updateFishPosition() {
    var windowWidth = window.innerWidth;
    var windowHeight = window.innerHeight;
    var fish = document.getElementById('fish');
    var fishWidth = fish.offsetWidth;
    var fishHeight = fish.offsetHeight;

    // Generate random coordinates within the window bounds
    var posX = Math.random() * (windowWidth - fishWidth);
    var posY = Math.random() * (windowHeight - fishHeight);

    // Update the fish's position every 10 frames
    if (counter % 10 === 0) {
        // Set the new position
        fish.style.top = posY + 'px';
        fish.style.left = posX + 'px';
    }

    // Increment the counter
    counter++;

    // Continue the animation
    requestAnimationFrame(updateFishPosition);
}

// Start the animation
updateFishPosition();
