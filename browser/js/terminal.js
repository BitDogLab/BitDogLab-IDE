'use strict';

serial_setup_str = `\x03`;

var Terminal = {
  input: document.querySelector('#cmd'),
  last_inputs: [],
  selected_input: 0,
  output: document.querySelector('.output'),
  lines: 0,
  MAX_LINES: 256,

  addLine: function (text_) {
    let text = text_;
    // while (text.includes('    \b')) {
    //   text = text.replaceAll('    \b', '');
    // }
    text = text.replaceAll(' ', '\xa0');
    let new_line = document.createElement('div');
    new_line.className = 'line';
    let text_node = document.createTextNode(text);
    new_line.appendChild(text_node);
    this.output.appendChild(new_line);
    this.output.scrollTop = this.output.scrollHeight;
    this.selected_input = this.last_inputs.length;
    if (++this.lines > this.MAX_LINES) {
      this.output.removeChild(this.output.firstChild);
      --this.lines;
    }
    return new_line;
  },

  addLines: function (lines) {
    lines.forEach(this.addLine);
  },

  readFromSerial: async function (ser) {
    let text = await ser.read();
    // console.log(text);
    this.addLine(text);
    return text;
  },

  addInput: function (line) {
    this.last_inputs.push(line);
    if (this.last_inputs.length > this.MAX_LINES)
      this.last_inputs.shift();
  },

  clear: function () {
    this.output.innerHTML = "";
  }
};

Terminal.input.addEventListener('keydown', async (event) => {
  switch (event.key) {
    case 'Enter':
      let line = event.target.value;
      // console.log(line);
      Terminal.addInput(line);
      await serial.write(line + '\r');
      event.target.value = '';
      break;
    case 'ArrowUp':
      if (--Terminal.selected_input < 0) {
        ++Terminal.selected_input;
        break;
      }
      event.target.value = Terminal.last_inputs[Terminal.selected_input];
      break;
    case 'ArrowDown':
      if (++Terminal.selected_input > Terminal.last_inputs.length) {
        --Terminal.selected_input;
        break;
      }
      event.target.value = (Terminal.selected_input >= Terminal.last_inputs.length)?(''):(Terminal.last_inputs[Terminal.selected_input]);
      break;
  }
});

document.getElementById("clear").addEventListener("click", () => {
  Terminal.clear();
});

setInterval(async () => {
  if (!serialIsConnected) return;
  let text;
  try {
    text = await Terminal.readFromSerial(serial);
  } catch (e) {
    if (e === DOMException)
      serial.disconnect();
  }
  if (text.length > 0)
    console.log(text);
}, 50);
