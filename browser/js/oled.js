"use strict";

serial_setup_str = `\x03exec("""\r
from machine import Pin, Soft12C\r
import ssd1306\r
import framebuf\r
\r
i2c = SoftI2C(scl=Pin(15), sda=Pin(14))\r
oled = ssd1306.SSD1306_I2C(128, 64, i2c)\r
oled.fill(0)\r
oled.show()\r
""")\r`;

var State = {
  is_mousedown: false,
  is_mousedown_canvas: false,
  mousedown_pixel: [-1,-1],
  mouseup_pixel: [-1,-1],
  color: 1,
  tool: null,
  current_handles: {
    mousedown: () => {},
    mousemove: () => {},
    mouseup: () => {}
  }
};

// OLED class.
var OLED = {};
OLED.canvas = document.querySelector(".oled-canvas");
OLED.ctx = OLED.canvas.getContext("2d");
OLED.last_image = OLED.ctx;
OLED.bounds = OLED.canvas.getBoundingClientRect();

// FrameBuffer class, based on adafruit python implementation.
OLED.FBuf = {}
OLED.FBuf.width = 128; // FBuf width.
OLED.FBuf.height = 64; // FBuf height.
const __buf = new Uint8Array(1024); // Buffer, or bytearray. Created as const pointer.
OLED.FBuf.__buf = __buf;
OLED.FBuf.format = {}; // Format base functions.

// Setting up format base functions.
((f) => {
  f.pixel = function (fbuf, x, y, value) {
    if (!(inRange(0, fbuf.width - 1)(x) && inRange(0, fbuf.height - 1)(y)))
      return; // If coordinates are out of bounds, return. Avoids looping figures.
    let index = (y >> 3) + x*(fbuf.height >> 3); // Get byte index. Uses VLSB.
    let bit = y & 0b00000111; // Get desired bit number.
    if (typeof value !== 'undefined') {// If value is defined, modify buffer.
      fbuf.__buf[index] = (fbuf.__buf[index] & ~(0x01 << bit)) | ((value != 0) << bit);
      // console.log(`[OLED.FBuf.format] Modified pixel (${x}, ${y}) to value ${value}.`)
    }
    return (fbuf.__buf[index] >> bit) & 0x01;
  }

  f.fillRect = function (fbuf, x, y, width, height, value) {
    let h = height, _y = y; // h makes backward count from height to 0. _y is current y being drawn.
    while (h > 0) { // Line by line.
      let index = (_y >> 3) + x*(fbuf.height >> 3);
      let bit = _y & 0b00000111;
      for (let w_ = 0; w_ < width; ++w_) { // For each pixel in horizontal line.
        let w = w_*(fbuf.height >> 3);
        fbuf.__buf[index + w] = (fbuf.__buf[index + w] & ~(0x01 << bit)) | ((value != 0) << bit);
      }
      ++_y; --h;
    }
  }

  f.hLine = function (fbuf, x, y, width, value) {
    this.fillRect(fbuf, x, y, width, 1, value);
  }

  f.vLine = function (fbuf, x, y, height, value) {
    this.fillRect(fbuf, x, y, 1, height, value);
  }

  f.rect = function (fbuf, x, y, width, height, value) {
    f.hLine(fbuf, x, y, width, value);
    f.hLine(fbuf, x, y + height - 1, width, value);
    f.vLine(fbuf, x, y, height, value);
    f.vLine(fbuf, x + width - 1, y, height, value);
  }

  f.line = function(fbuf, x0, y0, x1, y1, value) {
    // Bresenham's line algorithm.
    const dx = Math.abs(x1 - x0), dy = Math.abs(y1 - y0);
    const stepx = (x0 < x1)?(1):(-1), stepy = (y0 < y1)?(1):(-1);
    let x = x0, y = y0;
    let err;
    if (dx > dy) {
      err = dx/2;
      while (x != x1) {
        this.pixel(fbuf, x, y, value);
        err -= dy;
        if (err < 0) {
          y += stepy;
          err += dx;
        }
        x += stepx;
      }
    } else {
      err = dy/2;
      while (y != y1) {
        this.pixel(fbuf, x, y, value);
        err -= dx;
        if (err < 0) {
          x += stepx;
          err += dy;
        }
        y += stepy;
      }
    }
    this.pixel(fbuf, x, y, value);
  }

  f.ellipse = function (fbuf, centerx, centery, radiusx, radiusy, value, fill) {
    const rx2 = radiusx ** 2, ry2 = radiusy ** 2, rxry = radiusx * radiusy;
    // let half_rxry = (rxry/2) >> 0;
    // console.log(`Threshold (half_rxry): `, half_rxry);
    const rx2ry2 = rxry ** 2;
    const ellipseParametric = (x, y) => {return (ry2*(x**2) + rx2*(y**2) - rx2ry2);}
    
    // let para_array = [];
    for (let y = 0; y <= radiusy; ++y) {
      // para_array.push([]);
      for (let x = 0; x <= radiusx; ++x) {
        const result = ellipseParametric(x, y);
        // para_array[y].push(result);
        if (result < rxry) {
          this.pixel(fbuf, centerx - x, centery - y, value);
          this.pixel(fbuf, centerx + x, centery - y, value);
          this.pixel(fbuf, centerx - x, centery + y, value);
          this.pixel(fbuf, centerx + x, centery + y, value);
        }
      }
    }
    // console.log(para_array);
    if (!fill) this.ellipse(fbuf, centerx, centery, radiusx - 1, radiusy - 1, 1 - value, true);
  }

  f.fill = function (fbuf, value) {
    const byte = 0xff * value;
    for (let i = 0; i < 1024; ++i)
      fbuf.__buf[i] = byte;
  }
})(OLED.FBuf.format);

OLED.renderPixel = function (x, y) {
  // Updates single pixel based on current FBuf state.
  const px = 4 * x, py = 4 * y;
  let pixel = this.FBuf.format.pixel(this.FBuf, x, y);
  this.ctx.fillStyle = RGBtoHEX(
    [240, 240, 240].map((value) => {return (pixel * value)})
  );
  this.ctx.fillRect(px, py, 4, 4);
}

OLED.renderRegion = function(left, top, right, bottom) {
  // Updates region of canvas based on current FBuf state.
  let xmin, xmax, ymin, ymax;
  
  if (left < right) 
    xmin = left, xmax = right;
  else
    xmin = right, xmax = left;

  if (top < bottom) 
    ymin = top, ymax = bottom;
  else
    ymin = bottom, ymax = top;

  for (let x = xmin; x < xmax; ++x)
    for (let y = xmin; y < ymax; ++y)
      this.renderPixel(x, y);
}

OLED.renderFBuf = function () {
  // Updates full canvas based on current FBuf state.
  this.renderRegion(0, 0, this.FBuf.width, this.FBuf.height);
}

var Controls = {
  Color: {
    element: document.querySelector("#color-button")
  },
  Pencil: {
    element: document.querySelector("#pencil-button"),
    handles: {
      mousedown: (event) => {
        console.log("Controls.Pencil mousedown handle called!")
        // Do nothing.
      },
      mousemove: (event) => {
        // 
        if (State.is_mousedown_canvas == false) return;
        let [x, y] = OLED.getMousePixel(event);
        OLED.FBuf.format.pixel(OLED.FBuf, x, y, State.color);
        OLED.renderPixel(x, y);
      },
      mouseup: (event) => {
        console.log("Controls.Pencil mouseup handle called!")
        // Do nothing.
      }
    }
  },
  Line: {
    element: document.querySelector("#line-button"),
    handles: {
      mousedown: (event) => {
        console.log("Controls.Line mousedown handle called!")
        State.mousedown_pixel = OLED.getMousePixel(event);
      },
      mousemove: (event) => {
        // Do nothing.
      },
      mouseup: (event) => {
        console.log("Controls.Line mouseup handle called!")
        State.mouseup_pixel = OLED.getMousePixel(event);
        OLED.FBuf.format.line(OLED.FBuf, State.mousedown_pixel[0], State.mousedown_pixel[1], State.mouseup_pixel[0], State.mouseup_pixel[1], State.color);
        // OLED.renderRegion(State.mousedown_pixel[0], State.mousedown_pixel[1], State.mouseup_pixel[0], State.mouseup_pixel[1]);
        OLED.renderFBuf();
      },
    }
  },
  Rect: {
    element: document.querySelector("#rect-button"),
    handles: {
      mousedown: (event) => {
        console.log("Controls.Rect mousedown handle called!")
        State.mousedown_pixel = OLED.getMousePixel(event);
      },
      mousemove: (event) => {},
      mouseup: (event) => {
        console.log("Controls.Rect mouseup handle called!")
        State.mouseup_pixel = OLED.getMousePixel(event);
        let x0, y0;
        let dx, dy;
        if (State.mousedown_pixel[0] < State.mouseup_pixel[0])
          x0 = State.mousedown_pixel[0], dx = State.mouseup_pixel[0] - State.mousedown_pixel[0];
        else
          x0 = State.mouseup_pixel[0], dx = State.mousedown_pixel[0] - State.mouseup_pixel[0];

        if (State.mousedown_pixel[1] < State.mouseup_pixel[1])
          y0 = State.mousedown_pixel[1], dy = State.mouseup_pixel[1] - State.mousedown_pixel[1];
        else
          y0 = State.mouseup_pixel[1], dy = State.mousedown_pixel[1] - State.mouseup_pixel[1];

        OLED.FBuf.format.rect(OLED.FBuf, x0, y0, dx, dy, State.color, false);
        // OLED.renderRegion(State.mousedown_pixel[0], State.mousedown_pixel[1], State.mouseup_pixel[0], State.mouseup_pixel[1]);
        OLED.renderFBuf();
      },
    }
  },
  FillRect: {
    element: document.querySelector("#fillrect-button"),
    handles: {
      mousedown: (event) => {
        console.log("Controls.FillRect mousedown handle called!")
        State.mousedown_pixel = OLED.getMousePixel(event);
      },
      mousemove: (event) => {},
      mouseup: (event) => {
        console.log("Controls.FillRect mouseup handle called!")
        State.mouseup_pixel = OLED.getMousePixel(event);
        let x0, y0;
        let dx, dy;
        if (State.mousedown_pixel[0] < State.mouseup_pixel[0])
          x0 = State.mousedown_pixel[0], dx = State.mouseup_pixel[0] - State.mousedown_pixel[0];
        else
          x0 = State.mouseup_pixel[0], dx = State.mousedown_pixel[0] - State.mouseup_pixel[0];

        if (State.mousedown_pixel[1] < State.mouseup_pixel[1])
          y0 = State.mousedown_pixel[1], dy = State.mouseup_pixel[1] - State.mousedown_pixel[1];
        else
          y0 = State.mouseup_pixel[1], dy = State.mousedown_pixel[1] - State.mouseup_pixel[1];

        OLED.FBuf.format.fillRect(OLED.FBuf, x0, y0, dx, dy, State.color);
        // OLED.renderRegion(State.mousedown_pixel[0], State.mousedown_pixel[1], State.mouseup_pixel[0], State.mouseup_pixel[1]);
        OLED.renderFBuf();
      },
    }
  },
  Ellipse: {
    element: document.querySelector("#ellipse-button"),
    handles: {
      mousedown: (event) => {
        console.log("Controls.Ellipse mousedown handle called!")
        State.mousedown_pixel = OLED.getMousePixel(event);
      },
      mousemove: (event) => {},
      mouseup: (event) => {
        console.log("Controls.Ellipse mouseup handle called!")
        State.mouseup_pixel = OLED.getMousePixel(event);
        let [x0, y0] = State.mousedown_pixel;
        let [rx, ry] = [Math.abs(x0 - State.mouseup_pixel[0]), Math.abs(y0 - State.mouseup_pixel[1])];
        OLED.FBuf.format.ellipse(OLED.FBuf, x0, y0, rx, ry, State.color, false);
        OLED.renderFBuf();
      },
    }
  },
  FillEllipse: {
    element: document.querySelector("#fillellipse-button"),
    handles: {
      mousedown: (event) => {
        console.log("Controls.FillEllipse mousedown handle called!")
        State.mousedown_pixel = OLED.getMousePixel(event);
      },
      mousemove: (event) => {},
      mouseup: (event) => {
        console.log("Controls.FillEllipse mouseup handle called!")
        State.mouseup_pixel = OLED.getMousePixel(event);
        let [x0, y0] = State.mousedown_pixel;
        let [rx, ry] = [Math.abs(x0 - State.mouseup_pixel[0]), Math.abs(y0 - State.mouseup_pixel[1])];
        OLED.FBuf.format.ellipse(OLED.FBuf, x0, y0, rx, ry, State.color, true);
        OLED.renderFBuf();
      },
    }
  },
  Fill: {
    element: document.querySelector("#fill-button")
  },
  Send: {
    element: document.querySelector("#send-button")
  }
};

OLED.getMousePixel = function (event) {
  let rect = this.canvas.getBoundingClientRect();
  let x = ((event.clientX - rect.left - 8)/4) >> 0;
  let y = ((event.clientY - rect.top - 8)/4) >> 0;
  return [x, y];
};

(() => {
  Controls.Color.element.addEventListener("click", () => {
    Controls.Color.element.style.backgroundColor = (State.color == 1)?("black"):("white");
    State.color = 1 - State.color;
  });

  Controls.Pencil.element.addEventListener("click", (e) => {
    State.tool = Controls.Pencil;
    State.current_handles.mousedown = Controls.Pencil.handles.mousedown;
    State.current_handles.mousemove = Controls.Pencil.handles.mousemove;
    State.current_handles.mouseup = Controls.Pencil.handles.mouseup;
  });
  
  Controls.Line.element.addEventListener("click", (e) => {
    State.tool = Controls.Line;
    State.current_handles.mousedown = Controls.Line.handles.mousedown;
    State.current_handles.mousemove = Controls.Line.handles.mousemove;
    State.current_handles.mouseup = Controls.Line.handles.mouseup;
  });
  
  Controls.Rect.element.addEventListener("click", (e) => {
    State.tool = Controls.Rect;
    State.current_handles.mousedown = Controls.Rect.handles.mousedown;
    State.current_handles.mousemove = Controls.Rect.handles.mousemove;
    State.current_handles.mouseup = Controls.Rect.handles.mouseup;
  });
  
  Controls.FillRect.element.addEventListener("click", (e) => {
    State.tool = Controls.FillRect;
    State.current_handles.mousedown = Controls.FillRect.handles.mousedown;
    State.current_handles.mousemove = Controls.FillRect.handles.mousemove;
    State.current_handles.mouseup = Controls.FillRect.handles.mouseup;
  });
  
  Controls.Ellipse.element.addEventListener("click", (e) => {
    State.tool = Controls.Ellipse;
    State.current_handles.mousedown = Controls.Ellipse.handles.mousedown;
    State.current_handles.mousemove = Controls.Ellipse.handles.mousemove;
    State.current_handles.mouseup = Controls.Ellipse.handles.mouseup;
  });
  
  Controls.FillEllipse.element.addEventListener("click", (e) => {
    State.tool = Controls.FillEllipse;
    State.current_handles.mousedown = Controls.FillEllipse.handles.mousedown;
    State.current_handles.mousemove = Controls.FillEllipse.handles.mousemove;
    State.current_handles.mouseup = Controls.FillEllipse.handles.mouseup;
  });

  Controls.Fill.element.addEventListener("click", (e) => {
    OLED.FBuf.format.fill(OLED.FBuf, State.color);
    OLED.renderFBuf();
  });
})();

document.addEventListener("mousedown", (e) => {
  State.is_mousedown = true;
});

document.addEventListener("mouseup", (e) => {
  State.is_mousedown = false;
});

OLED.canvas.addEventListener("mousedown", (e) => {
  State.is_mousedown_canvas = true;
  State.current_handles.mousedown(e);
  // let [x, y] = OLED.getMousePixel(e);
  // console.log([x, y], OLED.FBuf.format.pixel(OLED.FBuf, x, y));
});

OLED.canvas.addEventListener("mousemove", (e) => {
  State.current_handles.mousemove(e);
});

OLED.canvas.addEventListener("mouseup", (e) => {
  State.is_mousedown_canvas = false;
  State.current_handles.mouseup(e);
});

OLED.renderFBuf();
