"use strict";

var oled_canvas = document.querySelector(".oled-canvas");
var oled_ctx = oled_canvas.getContext("2d");

oled_ctx.fillStyle = "#000";
oled_ctx.fillRect(0, 0, 512, 256);

var isMouseDown = false;
var isMouseStartedOnBlack = false;

function drawPixel(event) {
  const bounding = oled_canvas.getBoundingClientRect();
  const x = 4 * (((event.clientX - bounding.left - 8)/4) >> 0);
  const y = 4 * (((event.clientY - bounding.top - 8)/4) >> 0);
  let color;
  if (isMouseStartedOnBlack) {
    color = "#fff";
  } else {
    color = "#000";
  }
  oled_ctx.fillStyle = color;
  oled_ctx.fillRect(x, y, 4, 4);
}

oled_canvas.addEventListener("mousedown", (event) => {
  // Get color on mousedown event.
  const bounding = oled_canvas.getBoundingClientRect();
  const x = event.clientX - bounding.left;
  const y = event.clientY - bounding.top;
  const colorOnMouse = ((color) => {
    console.log(color);
    return "#" + ("000000" + (((color[0] << 16) + (color[1] << 8) + color[2]).toString(16))).slice(-6);
  })(oled_canvas.getContext("2d").getImageData(x, y, 1, 1).data);
  console.log(colorOnMouse);

  isMouseStartedOnBlack = (colorOnMouse === "#000000");
  console.log(isMouseStartedOnBlack);
  isMouseDown = true;
  drawPixel(event);
});
oled_canvas.addEventListener("mousemove", (event) => {
  if (isMouseDown) 
    drawPixel(event);
});
oled_canvas.addEventListener("mouseup", (event) => {
  isMouseDown = false;
});