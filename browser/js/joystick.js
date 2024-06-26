serial_setup_str = `\x03\r
from machine import Pin, ADC\r
import time\r
joystick_x = ADC(Pin(27))\r
joystick_y = ADC(Pin(26))\r
joystick_sw = Pin(22, Pin.IN, Pin.PULL_UP)\r
\r
def mainloop():\r
while True:\r
print(f'{joystick_x.read_u16()} {joystick_y.read_u16()} {joystick_sw.value()}')\r
time.sleep(0.05)\r
\b\b\r
mainloop()\r`;

jsCanvas = document.querySelector('#joystickcanvas');
jsCtx = jsCanvas.getContext('2d');
jsCtx.fillStyle = '#000000';
jsCtx.fillRect(0,0,255,255);

Labels = {
  xpos: document.querySelector('#joystick-xpos'),
  ypos: document.querySelector('#joystick-ypos'),
  pressed: document.querySelector('#joystick-pressed'),
}

function drawArrow(ctx, fromx, fromy, tox, toy, arrowWidth, color){
    //variables to be used when creating the arrow
    var headlen = 10;
    var angle = Math.atan2(toy-fromy,tox-fromx);
 
    ctx.save();
    ctx.strokeStyle = color;
 
    //starting path of the arrow from the start square to the end square
    //and drawing the stroke
    ctx.beginPath();
    ctx.moveTo(fromx, fromy);
    ctx.lineTo(tox, toy);
    ctx.lineWidth = arrowWidth;
    ctx.stroke();
 
    //starting a new path from the head of the arrow to one of the sides of
    //the point
    ctx.beginPath();
    ctx.moveTo(tox, toy);
    // ctx.lineTo(tox-headlen*Math.cos(angle-Math.PI/7),
    //            toy-headlen*Math.sin(angle-Math.PI/7));
 
    //path from the side point of the arrow, to the other side point
    ctx.lineTo(tox-headlen*Math.cos(angle+Math.PI/7),
               toy-headlen*Math.sin(angle+Math.PI/7));
 
    //path from the side point back to the tip of the arrow, and then
    //again to the opposite side point
    ctx.lineTo(tox, toy);
    ctx.lineTo(tox-headlen*Math.cos(angle-Math.PI/7),
               toy-headlen*Math.sin(angle-Math.PI/7));
 
    //draws the paths created above
    ctx.stroke();
    ctx.restore();
}

var long_buffer = '';
const token = '\r';
setInterval(async () => {
  if (!serialIsConnected) return;

  // Clear canvas.
  jsCtx.fillStyle = 'black';
  
  // Get data from serial port.
  long_buffer = await Terminal.readFromSerial(serial);
  // if (!long_buffer.includes('\r')) return;
  
  let values = long_buffer.split(' ').map((value) => {return parseInt(value);});
  let validValue = inRange(0, 65535);
  if (values.length != 3 || !validValue(values[0]) || !validValue(values[1])) return;
  values[1] = 65535 - values[1];
  console.log(values);
  
  // Draw arrow.
  jsCtx.fillRect(0, 0, 255, 255);
  drawArrow(jsCtx, 128, 128, values[0] >> 8, values[1] >> 8, 2, 'red');

  // Update labels.
  Labels.xpos.textContent = `${values[0]}`;
  Labels.ypos.textContent = `${values[1]}`;
  Labels.pressed.textContent = `${values[2]}`;
}, 25);
