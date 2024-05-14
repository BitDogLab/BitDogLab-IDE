"use strict";

// NeoPixel color control elements.
var npCanvas = document.getElementById("npcanvas");
var npCtx = npCanvas.getContext("2d");
var npColor = document.getElementById("npcolorselect");
var npLuminosity = document.getElementById("npluminosityselect");

var isMouseDown = false;
var npColorList = [
  [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
  [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
  [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
  [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
  [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
]

npCtx.fillStyle = npColor.value;
npCtx.fillRect(0, 0, 200, 200);

function inRange(min, max) {
  return (value) => {
    return ((value - min) * (value - max)) <= 0;
  }
}

function drawPixel(event) {
  const bounding = npCanvas.getBoundingClientRect();
  const x = event.clientX - bounding.left;
  const y = event.clientY - bounding.top;
  const pixel_x = (x/40) | 0;
  const pixel_y = (y/40) | 0;
  
  if (inRange(0, 4)(pixel_x) && inRange(0, 4)(pixel_y)) {
    const color = npColor.value;
    const luminosityRatio = npLuminosity.value/255.0;
    npCtx.fillStyle = color;
    npCtx.fillRect(40 * pixel_x, 40 * pixel_y, 40, 40);

    var colorList = [
      Math.round(parseInt(color.substr(1, 2), 16) * luminosityRatio),
      Math.round(parseInt(color.substr(3, 2), 16) * luminosityRatio),
      Math.round(parseInt(color.substr(5, 2), 16) * luminosityRatio)
    ];

    npColorList[pixel_y][pixel_x] = colorList;
    console.log("Pixel of index [", pixel_x, pixel_y, "] has color ", colorList, ".");
  }
}


npCanvas.addEventListener("mousedown", (event) => {
  isMouseDown = true;
  drawPixel(event);
});
npCanvas.addEventListener("mousemove", (event) => {
  if (isMouseDown) 
    drawPixel(event);
});
npCanvas.addEventListener("mouseup", (event) => {
  isMouseDown = false;
});