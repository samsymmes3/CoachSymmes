can = document.getElementById("screen");
ctx = can.getContext("2d");

var PIXEL_RATIO = (function () {
    var ctx = document.getElementById("screen").getContext("2d"),
        dpr = window.devicePixelRatio || 1,
        bsr = ctx.webkitBackingStorePixelRatio ||
              ctx.mozBackingStorePixelRatio ||
              ctx.msBackingStorePixelRatio ||
              ctx.oBackingStorePixelRatio ||
              ctx.backingStorePixelRatio || 1;

    return dpr / bsr;
})();

createHiDPICanvas = function(w, h, ratio) {
    if (!ratio) { ratio = PIXEL_RATIO; }
    var can = document.getElementById("screen");
    can.width = w * ratio;
    can.height = h * ratio;
    can.style.width = w + "px";
    can.style.height = h + "px";
    can.getContext("2d").setTransform(ratio, 0, 0, ratio, 0, 0);
    return can;
}

var can = createHiDPICanvas(document.body.clientWidth, window.innerHeight);
ctx = can.getContext("2d");

backgroundColor = rgbToHex({
  r: 240,
  g: 240,
  b: 240
});

document.body.style.background = backgroundColor;
