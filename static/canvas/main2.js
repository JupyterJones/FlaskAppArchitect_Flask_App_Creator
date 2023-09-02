document.addEventListener("DOMContentLoaded", function () {
  // Get the canvas element
  var canvas = document.getElementById("myCanvas");
  var ctx = canvas.getContext("2d");

  // Define line properties
  var startX = 50;
  var startY = 50;
  var endX = 200;
  var endY = 50;
  var color = "blue";

  // Draw the line
  ctx.beginPath();
  ctx.moveTo(startX, startY);
  ctx.lineTo(endX, endY);
  ctx.strokeStyle = color;
  ctx.lineWidth = 5; // Line width
  ctx.stroke();
});
