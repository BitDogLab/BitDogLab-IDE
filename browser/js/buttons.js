'use strict';

let ButtonA_Options = document.querySelector('#button-a-select');
let buttona_last_value = ButtonA_Options.value;
let ButtonA_Pages = {
  neopixel: {
    element: document.querySelector('span#button-a-neopixel'),
    options: {
      heart: document.querySelector('button#button-a-neopixel-heart'),
      smallheart: document.querySelector('button#button-a-neopixel-smallheart'),
      smile: document.querySelector('button#button-a-neopixel-smile'),
      sad: document.querySelector('button#button-a-neopixel-sad'),
      xbig: document.querySelector('button#button-a-neopixel-xbig'),
      xsmall: document.querySelector('button#button-a-neopixel-xsmall'),
      giraffe: document.querySelector('button#button-a-neopixel-giraffe'),
    },
    color: document.querySelector('input#button-a-neopixel-color'),
  },
  rgbled: {
    element: document.querySelector('#button-a-rgbled'),
    picker: document.querySelector('#button-a-rgbled-picker'),
    send: document.querySelector('#button-a-rgbled-send')
  },
  buzzer_a: {
    element: document.querySelector('span#button-a-buzzer-a'),
    freq: {
      value: 0,
      number_input: document.querySelector('#button-a-buzzer-a-freq'),
      slider_input: document.querySelector('#button-a-buzzer-a-freq-slide')
    },
    volume: {
      slider_input: document.querySelector('#button-a-buzzer-a-volume'),
      text: document.querySelector('#button-a-buzzer-a-volume-text')
    }
  },
  buzzer_b: {
    element: document.querySelector('span#button-a-buzzer-b'),
    freq: {
      value: 0,
      number_input: document.querySelector('#button-a-buzzer-b-freq'),
      slider_input: document.querySelector('#button-a-buzzer-b-freq-slide')
    },
    volume: {
      slider_input: document.querySelector('#button-a-buzzer-b-volume'),
      text: document.querySelector('#button-a-buzzer-b-volume-text')
    }
  }
};

async function changeButtonA (event) {
  let current_value = ButtonA_Options.value;
  ButtonA_Pages[buttona_last_value].element.style.display = "none";
  ButtonA_Pages[current_value].element.style.display = "block";
  
  switch (current_value) {
    case 'neopixel':
      await serial.write('\r' + 
        `ButtonHandler.BUTTONS_RISING_IRQ[0] = NeoPixelDesenhos.apaga\r`
      );
      break;
    case 'rgbled':
      await serial.write('\r' +
        `LedRGB.COLOR = ${HEXtoRGB(ButtonA_Pages.rgbled.picker.value).map((value) => {return value + (value << 8);})}\r` +
        `ButtonHandler.BUTTONS_FALLING_IRQ[0] = LedRGB.ligar\r` +
        `ButtonHandler.BUTTONS_RISING_IRQ[0] = LedRGB.desligar\r`
      );
      break;
    case 'buzzer_a':
      await serial.write('\r' +
        `ButtonHandler.BUTTONS_FALLING_IRQ[0] = lambda: Buzzer.ligar(0)\r` +
        `ButtonHandler.BUTTONS_RISING_IRQ[0] = lambda: Buzzer.desligar(0)\r`
      );
      break;
    case 'buzzer_b':
      await serial.write('\r' +
        `ButtonHandler.BUTTONS_FALLING_IRQ[0] = lambda: Buzzer.ligar(1)\r` +
        `ButtonHandler.BUTTONS_RISING_IRQ[0] = lambda: Buzzer.desligar(1)\r`
      );
      break;
  }

  if (current_value == buttonb_last_value) {
    ButtonB_Options.value = buttona_last_value;
  }
  buttona_last_value = current_value;
}

// Setting up button A select element.
ButtonA_Options.addEventListener('change', changeButtonA);

let ButtonB_Options = document.querySelector('#button-b-select');
let buttonb_last_value = ButtonB_Options.value;
let ButtonB_Pages = {
  neopixel: {
    element: document.querySelector('span#button-b-neopixel'),
    options: {
      heart: document.querySelector('button#button-b-neopixel-heart'),
      smallheart: document.querySelector('button#button-b-neopixel-smallheart'),
      smile: document.querySelector('button#button-b-neopixel-smile'),
      sad: document.querySelector('button#button-b-neopixel-sad'),
      xbig: document.querySelector('button#button-b-neopixel-xbig'),
      xsmall: document.querySelector('button#button-b-neopixel-xsmall'),
      giraffe: document.querySelector('button#button-b-neopixel-giraffe'),
    },
    color: document.querySelector('input#button-b-neopixel-color'),
  },
  rgbled: {
    element: document.querySelector('#button-b-rgbled'),
    picker: document.querySelector('#button-b-rgbled-picker'),
    send: document.querySelector('#button-b-rgbled-send')
  },
  buzzer_a: {
    element: document.querySelector('span#button-b-buzzer-a'),
    freq: {
      value: 0,
      number_input: document.querySelector('#button-b-buzzer-a-freq'),
      slider_input: document.querySelector('#button-b-buzzer-a-freq-slide')
    },
    volume: {
      slider_input: document.querySelector('#button-b-buzzer-a-volume'),
      text: document.querySelector('#button-b-buzzer-a-volume-text')
    }
  },
  buzzer_b: {
    element: document.querySelector('span#button-b-buzzer-b'),
    freq: {
      value: 0,
      number_input: document.querySelector('#button-b-buzzer-b-freq'),
      slider_input: document.querySelector('#button-b-buzzer-b-freq-slide')
    },
    volume: {
      slider_input: document.querySelector('#button-b-buzzer-b-volume'),
      text: document.querySelector('#button-b-buzzer-b-volume-text')
    }
  }
};

async function changeButtonB (event) {
  let current_value = ButtonB_Options.value;
  ButtonB_Pages[buttona_last_value].element.style.display = "none";
  ButtonB_Pages[current_value].element.style.display = "block";
  buttonb_last_value = current_value;

  switch (current_value) {
    case 'neopixel':
      await serial.write('\r' + 
        `ButtonHandler.BUTTONS_RISING_IRQ[1] = NeoPixelDesenhos.apaga\r`
      );
      break;
    case 'rgbled':
      await serial.write('\r' +
        `LedRGB.COLOR = ${HEXtoRGB(ButtonB_Pages.rgbled.picker.value).map((value) => {return value + (value << 8);})}\r` +
        `ButtonHandler.BUTTONS_FALLING_IRQ[1] = LedRGB.ligar\r` +
        `ButtonHandler.BUTTONS_RISING_IRQ[1] = LedRGB.desligar\r`
      );
      break;
    case 'buzzer_a':
      await serial.write('\r' +
        `ButtonHandler.BUTTONS_FALLING_IRQ[1] = lambda: Buzzer.ligar(0)\r` +
        `ButtonHandler.BUTTONS_RISING_IRQ[1] = lambda: Buzzer.desligar(0)\r`
      );
      break;
    case 'buzzer_b':
      await serial.write('\r' +
        `ButtonHandler.BUTTONS_FALLING_IRQ[1] = lambda: Buzzer.ligar(1)\r` +
        `ButtonHandler.BUTTONS_RISING_IRQ[1] = lambda: Buzzer.desligar(1)\r`
      );
      break;
  }
  
  if (current_value == buttona_last_value) {
    ButtonA_Options.value = buttonb_last_value;
  }
  buttonb_last_value = current_value;
}

// Setting up button A select element.
ButtonB_Options.addEventListener('change', changeButtonB);


// Setup function for both buttons.
((buttona, buttonb) => { // Button B not implemented yet.
  // Setting up NeoPixel.
  let setupNeoPixel = (np, id_) => {
    const id = id_;
    np.options.heart.addEventListener('click', async () => {
      let color = HEXtoRGB(np.color.value);
      await serial.write(`\r` +
      `NeoPixelDesenhos.COLOR = (${color})\r` +
      `ButtonHandler.BUTTONS_FALLING_IRQ[${id}] = NeoPixelDesenhos.coracao\r` + 
      `ButtonHandler.BUTTONS_RISING_IRQ[${id}] = NeoPixelDesenhos.apaga\r` + 
      `NeoPixelDesenhos.apaga()\r`
      );
    })

    np.options.smallheart.addEventListener('click', async () => {
      let color = HEXtoRGB(np.color.value);
      await serial.write(`\r` +
      `NeoPixelDesenhos.COLOR = (${color})\r` +
      `ButtonHandler.BUTTONS_FALLING_IRQ[${id}] = NeoPixelDesenhos.coracao_pequeno\r` + 
      `ButtonHandler.BUTTONS_RISING_IRQ[${id}] = NeoPixelDesenhos.apaga\r` + 
      `NeoPixelDesenhos.apaga()\r`
      );
    })

    np.options.smile.addEventListener('click', async () => {
      let color = HEXtoRGB(np.color.value);
      await serial.write(`\r` +
      `NeoPixelDesenhos.COLOR = (${color})\r` +
      `ButtonHandler.BUTTONS_FALLING_IRQ[${id}] = NeoPixelDesenhos.sorriso\r` + 
      `ButtonHandler.BUTTONS_RISING_IRQ[${id}] = NeoPixelDesenhos.apaga\r` + 
      `NeoPixelDesenhos.apaga()\r`
      );
    })

    np.options.sad.addEventListener('click', async () => {
      let color = HEXtoRGB(np.color.value);
      await serial.write(`\r` +
      `NeoPixelDesenhos.COLOR = (${color})\r` +
      `ButtonHandler.BUTTONS_FALLING_IRQ[${id}] = NeoPixelDesenhos.triste\r` + 
      `ButtonHandler.BUTTONS_RISING_IRQ[${id}] = NeoPixelDesenhos.apaga\r` + 
      `NeoPixelDesenhos.apaga()\r`
      );
    })
    
    np.options.xbig.addEventListener('click', async () => {
      let color = HEXtoRGB(np.color.value);
      await serial.write(`\r` +
      `NeoPixelDesenhos.COLOR = (${color})\r` +
      `ButtonHandler.BUTTONS_FALLING_IRQ[${id}] = NeoPixelDesenhos.X\r` + 
      `ButtonHandler.BUTTONS_RISING_IRQ[${id}] = NeoPixelDesenhos.apaga\r` + 
      `NeoPixelDesenhos.apaga()\r`
      );
    })

    np.options.xsmall.addEventListener('click', async () => {
      let color = HEXtoRGB(np.color.value);
      await serial.write(`\r` +
      `NeoPixelDesenhos.COLOR = (${color})\r` +
      `ButtonHandler.BUTTONS_FALLING_IRQ[${id}] = NeoPixelDesenhos.x\r` + 
      `ButtonHandler.BUTTONS_RISING_IRQ[${id}] = NeoPixelDesenhos.apaga\r` + 
      `NeoPixelDesenhos.apaga()\r`
      );
    })

    np.options.giraffe.addEventListener('click', async () => {
      let color = HEXtoRGB(np.color.value);
      await serial.write(`\r` +
      `NeoPixelDesenhos.COLOR = (${color})\r` +
      `ButtonHandler.BUTTONS_FALLING_IRQ[${id}] = NeoPixelDesenhos.girafa\r` + 
      `ButtonHandler.BUTTONS_RISING_IRQ[${id}] = NeoPixelDesenhos.apaga\r` + 
      `NeoPixelDesenhos.apaga()\r`
      );
    })
  };
  setupNeoPixel(buttona.neopixel, 0);
  setupNeoPixel(buttonb.neopixel, 1);

  // Setting up RGB LED control.
  let setupLED = (led) => {
    led.picker.addEventListener('change', async () => {
      let color = HEXtoRGB(led.picker.value).map((value) => {return value + (value << 8);});
      await serial.write('\r' +
        `LedRGB.COLOR = (${color})\r` + 
        `LedRGB.atualizar()\r`
      );
    });
  }
  setupLED(buttona.rgbled);
  setupLED(buttonb.rgbled);

  // Setting up buzzer A control.
  let setupBuzzer = (buzzer, id) => {
    buzzer.freq.number_input.addEventListener('change', async (e) => {
      buzzer.freq.value = e.target.value;
      buzzer.freq.slider_input.value = e.target.value;
      await serial.write('\r' +
        `Buzzer.BUZZERS[${id}].freq(${e.target.value})\r`
      );
    });
    
    buzzer.freq.slider_input.addEventListener('change', async (e) => {
      buzzer.freq.value = e.target.value;
      buzzer.freq.number_input.value = e.target.value;
      await serial.write('\r' +
        `Buzzer.BUZZERS[${id}].freq(${e.target.value})\r`
      );
    });
    
    buzzer.volume.slider_input.addEventListener('change', async (e) => {
      let value = e.target.value;
      // console.log(value);
      buzzer.volume.text.textContent = ((100*value / 32767) >> 0).toString();
      await serial.write('\r'+
        `Buzzer.VOLUMES[${id}] = ${value}\r` +
        `Buzzer.atualizar(${id})\r`
      );
    });
  };
  setupBuzzer(buttona.buzzer_a, 0);
  setupBuzzer(buttona.buzzer_b, 1);
  setupBuzzer(buttonb.buzzer_a, 0);
  setupBuzzer(buttonb.buzzer_b, 1);

})(ButtonA_Pages, ButtonB_Pages);

setInterval(async () => {
  if (!serialIsConnected) return;
  console.log(await serial.read());
}, 1000);
