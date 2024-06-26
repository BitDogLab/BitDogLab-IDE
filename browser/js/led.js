'use strict';

var ledColorPicker = document.querySelector("input");

document.addEventListener("DOMContentLoaded", () => {

  document.querySelector("#ledcolorsend").addEventListener("click", async () => {
    console.log();
    const color_str = ledColorPicker.value
    let color = [
      parseInt(color_str.substring(1, 3), 16) << 8,
      parseInt(color_str.substring(3, 5), 16) << 8,
      parseInt(color_str.substring(5), 16) << 8
    ];
    await serial.write(`\r\nsetColor(${color[0]}, ${color[1]}, ${color[2]})\r\n`);
  });

  serial_setup_str = `\x03exec("""\r\n
from machine import Pin, PWM\r\n
\r\n
pinR = Pin(12)\r\n
pinG = Pin(11)\r\n
pinB = Pin(13)\r\n
\r\n
pwmR = PWM(pinR)\r\n
pwmG = PWM(pinG)\r\n
pwmB = PWM(pinB)\r\n
\r\n
pwmR.freq(500)\r\n
pwmG.freq(500)\r\n
pwmB.freq(500)\r\n
pwmR.duty_u16(0)\r\n
pwmG.duty_u16(0)\r\n
pwmB.duty_u16(0)\r\n
\r\n
def setColor(r: int, g: int, b: int):\r\n
  global pwmR, pwmG, pwmB\r\n
  pwmR.duty_u16(r)\r\n
  pwmG.duty_u16(g)\r\n
  pwmB.duty_u16(b)\r\n
\r\n""")\r\n`;

  ledColorPicker.value = "#ff0000";
  ledColorPicker.select();
});



setInterval(async () => {
  if (!serialIsConnected) return;
  console.log(await Terminal.readFromSerial(serial));
}, 10);