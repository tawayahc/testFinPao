document.getElementById("custom-slider-length").addEventListener("input", function(event){
    let valueLength = event.target.value;
    document.getElementById("current-value-length").innerText = valueLength;
})

document.getElementById("custom-slider-num").addEventListener("input", function(event){
    let valueNum = event.target.value;
    document.getElementById("current-value-num").innerText = valueNum;
    ;
})

document.getElementById("custom-slider-temp").addEventListener("input", function(event){
    let valueTemp = event.target.value;
    document.getElementById("current-value-temp").innerText = valueTemp;
})