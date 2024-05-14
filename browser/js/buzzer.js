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

// Maybe canvas would be better for this. Rethink later.
var keys = document.querySelectorAll(".piano-key");
keys.forEach((key) => {
  key.addEventListener("mousedown", (event) => {
    const clicked_key = event.target.dataset.list;
    console.log("Key:", clicked_key, "| Frequency:", NOTES[clicked_key]);
    // After this, send instruction via serial.
  });
  key.addEventListener("mouseup", (event) => {
    console.log("Released key.");
    // Send release instruction via serial.
  })
});