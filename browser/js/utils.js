function inRange(min, max) {
  return (value) => {
    return ((value - min) * (value - max)) <= 0;
  }
}

function HEXtoRGB(hex) {
  if (hex[0] == "#") {
    hex = hex.substr(1,6);
  }
  return [
    Math.round(parseInt(hex.substr(0, 2), 16)),
    Math.round(parseInt(hex.substr(2, 2), 16)),
    Math.round(parseInt(hex.substr(4, 2), 16))
  ];
}

function RGBtoHEX(r, g, b) {
  if (typeof g !== "undefined" && typeof b !== "undefined") {
    let str = "#";
    if (r < 16) str += "0";
    str += r.toString(16);
    if (g < 16) str += "0";
    str += g.toString(16);
    if (b < 16) str += "0";
    str += b.toString(16);
    return str;
  } else if (Array.isArray(r)) {
    const r_ = r[0];
    const g_ = r[1];
    const b_ = r[2];
    return RGBtoHEX(r_, g_, b_);
  }
}