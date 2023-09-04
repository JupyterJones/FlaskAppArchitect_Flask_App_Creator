const canvas = document.querySelector("canvas");
const ctx = canvas.getContext("2d");

canvas.width = innerWidth;
canvas.height = innerHeight;

class Particle {
  constructor(x, y, speed, angle) {
    this.x = x;
    this.y = y;
    this.speed = speed;
    this.angle = angle;
    this.radius = Math.random() * 4 + 1;
    this.opacity = 1;
  }
  draw() {
    ctx.beginPath();
    ctx.fillStyle = `hsla(0, 100%, 0%, ${this.opacity})`;
    ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
    ctx.fill();
  }
  update() {
    this.x += this.speed * Math.cos(this.angle);
    this.y += this.speed * Math.sin(this.angle);
    this.opacity -= 0.01;
    if (this.opacity <= 0.01) this.opacity = 0;
    this.draw();
  }
}

const particle = new Particle(200, 100, 2, 1);
const numOfParticlesOnMouseMove = 5;
const particlesOnMouseMove = [];
const numOfParticlesOnMouseClick = 250;
const particlesOnMouseClick = [];
let mouseClicked = false;

function animate() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  requestAnimationFrame(animate);
  if (mouseClicked) {
    particlesOnMouseClick.forEach((particle, index) => {
      particle.update();
      if (particle.opacity == 0) {
        particlesOnMouseClick.splice(index, 1);
      }
    });
  }
  particlesOnMouseMove.forEach((particle, index) => {
    particle.update();
    if (particle.opacity == 0) {
      particlesOnMouseMove.splice(index, 1);
    }
  });
}

animate();

addEventListener("mousemove", (e) => {
  for (let i = 0; i < numOfParticlesOnMouseMove; i++) {
    let speed = Math.random() * 3 - 1.5;
    let angle = Math.random() * Math.PI * 2;
    particlesOnMouseMove.push(new Particle(e.x, e.y, speed, angle));
  }
});

addEventListener("click", (e) => {
  for (let i = 0; i < numOfParticlesOnMouseClick; i++) {
    let speed = Math.random() * 6 - 3;
    let angle = Math.random() * Math.PI * 2;
    particlesOnMouseClick.push(new Particle(e.x, e.y, speed, angle));
  }
  mouseClicked = true;
});
