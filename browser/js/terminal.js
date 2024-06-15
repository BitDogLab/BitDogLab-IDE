'use strict';

serial_setup_str = `\x03`;

var Terminal = {
  input: document.querySelector('#cmd'),
  output: document.querySelector('.output'),

  addLine: function (text) {
    let new_line = document.createElement('div');
    new_line.className = 'line';
    let text_node = document.createTextNode(text);
    new_line.appendChild(text_node);
    this.output.appendChild(new_line);
    return new_line;
  },

  addLines: function (lines) {
    lines.forEach(this.addLine);
  }
};

Terminal.input.addEventListener('keydown', async (event) => {
  if (event.key == 'Enter') {
    let line = event.target.value;
    // console.log(line);
    await serial.write(line + '\r');
    event.target.value = '';
  }
});

setInterval(async () => {
  if (!serialIsConnected) return;
  let line = await serial.read();
  // console.log(line);
  Terminal.addLine(line);
}, 50);
