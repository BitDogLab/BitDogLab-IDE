'use strict';
// import { serial } from "./serial.js";

document.addEventListener("DOMContentLoaded", () => {

  var ledColorPicker = document.querySelector("input");

  ledColorPicker.addEventListener("change", (event) => {
    if (serial.port)
  })

  ledColorPicker.value = "#ff0000";
  ledColorPicker.select();
});