function draw(initCtx){
  can.width = document.body.clientWidth;
  can.height = window.innerHeight;
  width = can.width;
  height = can.height;

  drawSidebar(initCtx);
  drawHeader(initCtx);
}

function drawHeader(initCtx){
  initCtx.fillStyle = headerColor;
  initCtx.fillRect(190, 0, width - 190, 50);
}

function drawSidebar(initCtx){
  initCtx.fillStyle = sidebarColor;
  initCtx.fillRect(0, 0, 190, height);

  initCtx.fillStyle = "#000000";
  initCtx.font = "Bold 32px Times New Roman";
  console.log(initCtx.measureText("Home"))
  initCtx.fillText("Home", 10, 35);
}

var headerColor = rgbToHex({
  r: 8,
  g: 102,
  b: 156
});

var sidebarColor = rgbToHex({
  r: 10,
  g: 150,
  b: 240
});
