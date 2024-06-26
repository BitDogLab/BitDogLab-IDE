"use strict";

const NOTES = {
  "B3": 247,
  "C4": 262,
  "Cs4": 277,
  "D4": 294,
  "Ds4": 311,
  "E4": 330,
  "F4": 349,
  "Fs4": 370,
  "G4": 392,
  "Gs4": 415,
  "A4": 440,
  "As4": 466,
  "B4": 494,
  "C5": 523
};
const KEYBOARD_NOTES = { // Unused.
  'z': 247,
  'x': 262,
  'd': 277,
  'c': 294,
  'f': 311,
  'v': 330,
  'b': 349,
  'h': 370,
  'n': 392,
  'j': 415,
  'm': 440,
  'k': 466,
  ',': 494,
  '.': 523
};

serial_setup_str = `\x03\r\n
exec("""\r\n
from machine import Pin, PWM\r\n
\r\n
buzzerA_pin = Pin(21, Pin.OUT)\r\n
buzzerA_pwm = PWM(buzzerA_pin)\r\n
buzzerA_pwm.duty_u16(0)\r\n
buzzerB_pin = Pin(4, Pin.OUT)\r\n
buzzerB_pwm = PWM(buzzerB_pin)\r\n
buzzerB_pwm.duty_u16(0)\r\n
""")\r\n`;

// Maybe canvas would be better for this. Rethink later.
var keys = document.querySelectorAll(".piano-key");
keys.forEach((key) => {
  key.addEventListener("mousedown", async (event) => {
    const clicked_key = event.target.dataset.list;
    console.log("Key:", clicked_key, "| Frequency:", NOTES[clicked_key]);
    // After this, send instruction via serial.
    await serial.write(`\r\n
buzzerA_pwm.freq(${NOTES[clicked_key]})\r\n
buzzerA_pwm.duty_u16(32767)\r\n
    `);
  });
  key.addEventListener("mouseup", async (event) => {
    console.log("Released key.");
    // Send release instruction via serial.
    await serial.write(`\r\n
buzzerA_pwm.duty_u16(0)\r\n
    `);
  });
});
document.addEventListener("keydown", async (event) => {
  if (event.key in KEYBOARD_NOTES) {
    await serial.write(`\r\n
buzzerA_pwm.freq(${KEYBOARD_NOTES[event.key]})\r\n
buzzerA_pwm.duty_u16(32767)\r\n
    `);
  }
});
document.addEventListener("keyup", async (event) => {
  // Send release instruction via serial.
  await serial.write(`\r\n
buzzerA_pwm.duty_u16(0)\r\n
  `);
});

setInterval(async () => {
  if (!serialIsConnected) return;
  console.log(await Terminal.readFromSerial(serial));
}, 10);