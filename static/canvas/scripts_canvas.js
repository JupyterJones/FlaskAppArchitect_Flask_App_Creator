const canvas = document.querySelector("canvas");
const ctx = canvas.getContext("2d");

canvas.width = innerWidth;
canvas.height = innerHeight;

const mouse = {
  x: null,
  y: null,
  radius: 200,
};

addEventListener("mousemove", (e) => {
  mouse.x = e.x;
  mouse.y = e.y;
});

class Particle {
  constructor(x, y) {
    this.x = x;
    this.y = y;
    this.radius = 2;
    this.baseX = this.x;
    this.baseY = this.y;
  }
  draw() {
    ctx.beginPath();
    ctx.fillStyle = "orange";
    ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
    ctx.closePath();
    ctx.fill();
  }
  update() {
    let dx = mouse.x - this.x;
    let dy = mouse.y - this.y;
    let distance = Math.sqrt(dx * dx + dy * dy);
    let forceDirX = dx / distance;
    let forceDirY = dy / distance;
    let maxDistance = mouse.radius;
    let force = ((maxDistance - distance) / maxDistance) * 10;
    let dirX = forceDirX * force;
    let dirY = forceDirY * force;
    if (distance < maxDistance) {
      this.x -= dirX;
      this.y -= dirY;
    } else {
      if (this.x != this.baseX) {
        let dx = this.x - this.baseX;
        this.x -= dx / 15;
      }
      if (this.y != this.baseY) {
        let dy = this.y - this.baseY;
        this.y -= dy / 15;
      }
    }
  }
}

const particle = new Particle();
particle.draw();

const particlesArray = [];
const totalNumOfParticles = 1500;

for (let i = 0; i < totalNumOfParticles; i++) {
  let x = Math.random() * canvas.width;
  let y = Math.random() * canvas.height;
  particlesArray.push(new Particle(x, y));
}

function animate() {
  requestAnimationFrame(animate);
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  particlesArray.forEach((particle) => {
    particle.draw();
    particle.update();
  });
}

animate();

