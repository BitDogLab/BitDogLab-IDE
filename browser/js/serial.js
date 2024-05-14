var serial = {};

(
  function() {
    'use strict';

    serial.getPorts = function() {
      return navigator.usb.getDevices()
        .then(devices => {
          return devices.map(device => new serial.Port(device));
        });
    }

    serial.requestPort = function() {
      const filters = [
        { 'vendorId': 0xCAFE }, // TinyUSB
        { 'vendorId': 0x239A }, // Adafruit
        { 'vendorId': 0x2E8A }, // Raspberry Pi
        { 'vendorId': 0x303A }, // Espressif
        { 'vendorId': 0x2341 }, // Arduino
      ];
      return navigator.usb.requestDevice({ 'filters': filters })
        .then(
          device => new serial.Port(device)
        );
    };

    serial.Port = function(device) {
      this.device_ = device;
      this.interfaceNumber = 0;
      this.endpointIn = 0;
      this.endpointOut = 0;
    };

    serial.Port.prototype.connect = function() {
      let readLoop = () => {
        this.device_.transferIn(this.endpointIn, 64)
          .then(result => {
            this.onRecieve(result.data);
            readLoop();
          }, error => {
            this.onRecieveError(error);
          });
      };
      return this.device_.open()
        .then(() => {
          if (this.device_.configuration === null) {
            return this.device_.selectConfiguration(1);
          };
        }).then(() => {
          var interfaces = this.device_.configuration.interfaces;
          interfaces.forEach(element => {
            element.alternates.forEach(elementalt => {
              if (elementalt.interfaceClass == 0xFF) {
                this.interfaceNumber = element.interfaceNumber;
                elementalt.endpoints.forEach(elementendpoint => {
                  if (elementendpoint.direction == "out") {
                    this.endpointOut = elementendpoint.endpointNumber;
                  }
                  if (elementendpoint.direction == "in") {
                    this.endpointIn = elementendpoint.endpointNumber;
                  }
                })
              }
            })
          })
        }).then(() => {
          readLoop();
        });
    };

    serial.Port.prototype.disconnect = function() {
      return this.device_.controlTransferOut({
        'requestType': 'class',
        'recipient': 'interface',
        'request': 0x22,
        'value': 0x00,
        'index': this.interfaceNumber
      }).then(() => this.device_.close());
    };
  }
)();

let port;

function connect() {
  port.connect().then(() => {
    port.onRecieve = data => {
      let decoder = new TextDecoder();
      console.log(textDecoder.decode(data));
    };
    port.onRecieveError = error => {
      console.error(error);
    };
  });
}

function startup() {
  serial.getPorts().then(ports => {
    if (ports.length === 0) {
      console.error("No device found.");
    } else {
      console.log("Device found!");
      port = ports[0];
      connect();
    }
  });
}

window.addEventListener("load", startup);