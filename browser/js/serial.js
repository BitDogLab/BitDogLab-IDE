'use strict';

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

var serialIsConnected = false;
var serial = {
  // Serial port variable.
  port: null,
  connected: false,
  isConnected: null,

  // Reader and writer. Built on connect.
  reader: null,
  writer: null,

  // Connect and disconnect functions.
  connect: null,
  disconnect: null,

  // On connect and on disconnect functions.
  onConnect: () => {},
  onDisconnect: () => {},

  // Read/Write functions.
  read: null,
  write: null
};

const serial_filters = [ // Doesn't work. When used, no ports are listed.
  {usbVendorId: 5, usbProductId: 11914}
];

// Connect and disconnect functions.
serial.connect = async () => {
  // Connect and open port. Log port info.
  this.port = await navigator.serial.requestPort();
  console.log(this.port.getInfo());
  await this.port.open({ baudRate: 115200 });

  // Reader setup.
  this.reader = {
    decoder: new TextDecoderStream(),
    readable_closed: null,
    reader: null,
    buffer: ''
  };
  this.reader.readable_closed = this.port.readable.pipeTo(
    this.reader.decoder.writable
  );
  this.reader.reader = this.reader.decoder.readable.getReader();

  // Writer setup.
  this.writer = {
    encoder: new TextEncoderStream(),
    writable_closed: null,
    writer: null
  };
  this.writer.writable_closed = this.writer.encoder.readable.pipeTo(
    this.port.writable
  );
  this.writer.writer = this.writer.encoder.writable.getWriter();

  this.connected = true;
  serialIsConnected = true;
}
serial.disconnect = async () => {
  this.reader.reader.releaseLock();
  this.port.readable.releaseLock();
  this.writer.writer.releaseLock();
  this.port.writable.releaseLock();
  await this.port.close();

  this.port = null;
  this.connected = false;
  serialIsConnected = false;

  await this.onDisconnect();
}

// Read/Write functions.
serial.read = async () => { // Reads into buffer string. Returns line.
  // let string = '';
  while (!this.reader.buffer.includes('\r')) {
    const { value, done } = await this.reader.reader.read();
    this.reader.buffer += value;
    if (done || value.length == 0) break;
  }
  let index = this.reader.buffer.indexOf('\r');
  let output = this.reader.buffer.slice(0, index);
  this.reader.buffer = this.reader.buffer.slice(index + 1);
  // console.log(string);
  return output;
}

serial.write = async (text) => {
  if (!this.connected) {
    console.error("Serial not connected! Can't write!");
    return;
  }
  let str = text.slice(0, 64), next = text.slice(64);
  while (str.length > 0) {
    await this.writer.writer.write(str);
    str = next.slice(0, 64);
    next = next.slice(64);
    // sleep(1);
  }
}

var status_display = document.getElementById("serialconnectstatus");
var connect_button = document.getElementById("serialconnectbutton");
var is_connected = false;
var serial_setup_str = "\r\n";

connect_button.addEventListener("click", async () => {
  if (!(serial.connected)) {
    try {
      await serial.connect();
    } catch (error) {
      console.error(error);
      return;
    }
    console.log("Success!");
    status_display.textContent = "Conectado";
    connect_button.textContent = "Desconectar";
    await serial.write(serial_setup_str);
    serial.onConnect();
  } else {
    await serial.disconnect();
    status_display.textContent = "Desconectado";
    connect_button.textContent = "Conectar";
  }
});

window.addEventListener('beforeunload', async () => {
  if (!serialIsConnected) return;
  await serial.write(`\x03\r
from machine import reset\r
reset()\r`);
});