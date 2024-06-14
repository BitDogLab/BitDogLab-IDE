'use strict';

serial_setup_str = `\x03\r
from machine import Pin, ADC\r
import time\r
mic = ADC(Pin(28))\r
def mainloop():\r
while True:\r
print(mic.read_u16())\r
time.sleep(0.005)\r\r\r\r\r\r
mainloop()\r
`;

var Mic = {
  // Microphone control elements in document.
  Controls: {
    // play: document.querySelector("#play"),
    // stop: document.querySelector("#stop"),
    record: document.querySelector("#record")
  },
  Volume: {
    canvas: document.querySelector("#volume-meter"),
    ctx: null,
    bar_grad: null,
    set: null
  },
  is_recording: false
}

Mic.Volume.ctx = Mic.Volume.canvas.getContext('2d');
Mic.Volume.bar_grad = Mic.Volume.ctx.createLinearGradient(0, 0, 512, 0);
Mic.Volume.bar_grad.addColorStop(0, '#00ff00');
Mic.Volume.bar_grad.addColorStop(0.5, '#ffff00');
Mic.Volume.bar_grad.addColorStop(1, '#ff0000');

// Prepare volume meter.
Mic.Volume.ctx.fillStyle = 'black';
Mic.Volume.ctx.fillRect(0, 0, 528, 80);

Mic.Volume.set = (vol) => {
  Mic.Volume.ctx.fillStyle = 'black';
  Mic.Volume.ctx.fillRect(0, 0, 528, 80);
  Mic.Volume.ctx.fillStyle = Mic.Volume.bar_grad;
  
  const length = vol >> 7;
  Mic.Volume.ctx.fillRect(8, 8, length, 64);
};

Mic.Controls.record.addEventListener('click', (e) => {
  if (!serialIsConnected) return;
  if (Mic.is_recording) {
    Mic.Volume.set(0);
    e.target.textContent = 'Record';
    Mic.is_recording = false;
  } else {
    e.target.textContent = 'Stop recording'
    Mic.is_recording = true;
  }
});

let long_buffer = '';
const token = '\r';
setInterval(async () => {
  if (!serialIsConnected || !Mic.is_recording) return;
  
  // Get data from serial port.
  long_buffer = await serial.read();
  console.log(long_buffer);
  let volume = 2 * Math.abs(parseInt(long_buffer) - 32768);
  Mic.Volume.set(volume);
}, 5);

