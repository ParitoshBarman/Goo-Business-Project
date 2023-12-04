const divBGimg1 = document.querySelector(".sliderImg1");
const divBGimg2 = document.querySelector(".sliderImg2");
const divBGimg3 = document.querySelector(".sliderImg3");


setTimeout(() => {

    let progressElement = document.getElementById('pogressID');
    progressElement.style.display = "none"
    // console.log("Done...")
    
}, 1000);


setTimeout(() => {
    divBGimg2.classList.add("sliderImg2ExtraAni");
}, 1000);
setTimeout(() => {
    divBGimg2.classList.remove("sliderImg2ExtraAni");
}, 13000);


setInterval(sliding, 15000);
setInterval(slidingClear, 14990);

function sliding(){
    divBGimg1.classList.add("sliderImg1Ani");
    divBGimg2.classList.add("sliderImg2Ani");
    divBGimg3.classList.add("sliderImg3Ani");
    // divBGimg1.classList.add("zIndexHigh")3
    
    // divBGimg1.classList.remove("sliderImg1Ani");
    

}


function slidingClear(){
    divBGimg1.classList.remove("sliderImg1Ani");
    divBGimg2.classList.remove("sliderImg2Ani");
    divBGimg3.classList.remove("sliderImg3Ani");
    // divBGimg1.classList.add("zIndexHigh")3
    
    // divBGimg1.classList.remove("sliderImg1Ani");
}

function currentTime() {
    let date = new Date(); 
    let hh = date.getHours();
    let mm = date.getMinutes();
    let ss = date.getSeconds();
    let session = "AM";
  
    if(hh == 0){
        hh = 12;
    }
    if(hh > 12){
        hh = hh - 12;
        session = "PM";
     }
  
     hh = (hh < 10) ? "0" + hh : hh;
     mm = (mm < 10) ? "0" + mm : mm;
     ss = (ss < 10) ? "0" + ss : ss;
      
     let time = hh + ":" + mm + ":" + ss + " " + session;
  
    document.getElementById("clock").innerText = time; 
    let t = setTimeout(function(){ currentTime() }, 1000);
  }
  currentTime();