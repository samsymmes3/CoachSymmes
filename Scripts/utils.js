function hexToRGB(initHex){
  var numbers = []
  for(var i = 0; i < 6; i++){
    if(initHex[i + 1] == "f" || initHex[i + 1] == "F"){numbers.push(15);}
    else if(initHex[i + 1] == "e" || initHex[i + 1] == "E"){numbers.push(14);}
    else if(initHex[i + 1] == "d" || initHex[i + 1] == "D"){numbers.push(13);}
    else if(initHex[i + 1] == "c" || initHex[i + 1] == "C"){numbers.push(12);}
    else if(initHex[i + 1] == "b" || initHex[i + 1] == "B"){numbers.push(11);}
    else if(initHex[i + 1] == "a" || initHex[i + 1] == "A"){numbers.push(10);}
    else{numbers.push(Number(initHex[i + 1]));}
  }
  return {
    r: numbers[0] * 16 + numbers[1],
    g: numbers[2] * 16 + numbers[3],
    b: numbers[4] * 16 + numbers[5]
  }
}

function rgbToHex(initRGB){
  var toRet = "#"
  var letters = [
    Math.floor(initRGB.r / 16),
    Math.floor(initRGB.r % 16),
    Math.floor(initRGB.g / 16),
    Math.floor(initRGB.g % 16),
    Math.floor(initRGB.b / 16),
    Math.floor(initRGB.b % 16)
  ];
  for(var i = 0; i < 6; i++){
    if(letters[i] == 15){toRet = toRet + "f";}
    else if(letters[i] == 14){toRet = toRet + "e";}
    else if(letters[i] == 13){toRet = toRet + "d";}
    else if(letters[i] == 12){toRet = toRet + "c";}
    else if(letters[i] == 11){toRet = toRet + "b";}
    else if(letters[i] == 10){toRet = toRet + "a";}
    else{toRet = toRet + letters[i];}
  }
  return toRet;
}
