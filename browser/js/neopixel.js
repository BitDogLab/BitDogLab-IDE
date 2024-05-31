"use strict";

serial_setup_str = `\x03\r
exec("""\r
from machine import Pin\r
import neopixel\r
\r
np = neopixel.NeoPixel(Pin(7), 25)\r
np_queue = []\r
\r
def resetLEDs():\r
global np, np_queue\r
for i in range(25):\r
np[i] = (0, 0, 0)\r
\bnp.write()\r
np_queue.clear()\r
\b\r
def setLED(pos: tuple[int, int], color: tuple[int, int, int]):\r
global np_queue\r
y = pos[1]\r
x = (4 - pos[0]) if y%2==0 else pos[0]\r
np_queue.append((5*y + x, color))\r
\b\r
def updateLEDs():\r
global np, np_queue\r
while len(np_queue) > 0:\r
i, color = np_queue.pop(0)\r
np[i] = color\r
\bnp.write()\r
\b\r""")\r\n`;

// NeoPixel color control elements.
var npCanvas = document.getElementById("npcanvas");
var npCtx = npCanvas.getContext("2d");
var npColor = document.getElementById("npcolorselect");
var npLuminosity = document.getElementById("npluminosityselect");
var npSend = document.getElementById("npsend");

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

    npColorList[4 - pixel_y][pixel_x] = colorList;
    console.log("Pixel of index [", pixel_x, 4 - pixel_y, "] has color ", colorList, ".");
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

npSend.addEventListener("click", async (event) => {
  // let colors_str = "[";
  // npColorList.forEach((row) => {
  //   colors_str += "[";
  //   row.forEach((color) => {
  //     colors_str += `[${color}],`;
  //   });
  //   colors_str = colors_str.slice(0, -1) + "],";
  // });
  // colors_str = colors_str.slice(0, -1) + "]";
  // console.log(colors_str);
  npColorList.forEach(async (row, y, array_y) => {
    row.forEach(async (color, x, array_x) => {
      console.log(x, y, `${color}`);
      await serial.write(`\rsetLED((${x}, ${y}), (${color}))\r`);
    });
  });
  await serial.write("\rupdateLEDs()\r");
//   await serial.write(`\r
// exec("""
// for y, row in enumerate(${colors_str}):\r
//   for x, rgb in enumerate(row):\r
//     setLED((x, y), rgb)\r 
// \r
// updateLEDs()\r
// """)\r
  // `);
});