'use strict';

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

var serial = {
  // Serial port variable.
  port: null,
  connected: false,

  // Reader and writer. Built on connect.
  reader: null,
  encoder: null,
  writer: null,

  // Connect and disconnect functions.
  connect: null,
  disconnect: null,

  // Read/Write functions.
  read: null,
  write: null
};

const serial_filters = [
  {usbVendorId: 5, usbProductId: 11914}
];

// Connect and disconnect functions.
serial.connect = async () => {
  // Connect and open port. Log port info.
  this.port = await navigator.serial.requestPort({ serial_filters });
  console.log(this.port.getInfo());
  await this.port.open({ baudRate: 115200 });

  // Reader setup.
  this.reader = this.port.readable.getReader({ mode: "byob" });

  // Writer setup.
  this.writer = {
    encoder: new TextEncoderStream(),
    writable_closer: null,
    writer: null
  };
  this.writer.writable_closed = this.writer.encoder.readable.pipeTo(
    this.port.writable
  );
  this.writer.writer = this.writer.encoder.writable.getWriter();
  this.connected = true;
}
serial.disconnect = async () => {
  this.reader.reader.releaseLock();
  this.port.readable.releaseLock();
  this.writer.writer.releaseLock();
  this.port.writable.releaseLock();
  await this.port.close();

  this.port = null;
  this.connected = false;
}

// Read/Write functions.
serial.read = async (buffer) => { // Reads into buffer.
  let offset = 0;
  while (offset < buffer.byteLength) {
    const { value, done } = await this.reader.read(
      new Uint8Array(buffer, offset)
    );
    if (done) {
      break;
    }
    buffer = value.buffer;
    offset += value.byteLength;
  }
  return buffer;
}
serial.write = async (text) => {
  let str = text.slice(0, 64), next = text.slice(64);
  while (str.length > 0) {
    await this.writer.writer.write(str);
    str = next.slice(0, 64);
    next = next.slice(64);
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
  } else {
    await serial.disconnect();
    status_display.textContent = "Desconectado";
    connect_button.textContent = "Conectar";
  }
});