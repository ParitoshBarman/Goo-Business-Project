// let fetureLi = document.querySelector("header>nav>div>ul>li:nth-child(3)");
// let drpLi = document.querySelector("header>nav>div>ul>li:nth-child(3)>ul");

// fetureLi.addEventListener("mouseover", ()=>{
//     drpLi.style.display = "block";
//     drpLi.style.marginRight  = "-140px";
// });
// fetureLi.addEventListener("mouseout", ()=>{  
//     drpLi.style.display = "none";
//     drpLi.style.marginRight  = "0";
// });




let changealeImgDiv = document.querySelector("#changealeImgDiv>img")
let heddinTextP = document.querySelectorAll(".text>p")
let imageList = [
"/static/img/othersimg/comprehensive curriculam.png",
"/static/img/othersimg/expert instruction.jpg",
"/static/img/othersimg/hands-on project and portfolio buildind.jpg",
"/static/img/othersimg/flexible schedule.jpg",
"/static/img/othersimg/career readiness.jpg",
"/static/img/othersimg/course-features-real-world projects.png",
]
let i=0;
let j=0;
setInterval(function () {
    if(i==0){
        j=5;
    }else{
        j=i-1;
    }
    // changealeImgDiv.src = imageList[i]
    heddinTextP[i].style.display = "block"

    heddinTextP[j].style.display = "none"
    i++;
    
    if(i==6){
        i=0;
    }
}, 2000);

let navUl = document.querySelector("nav>div:nth-child(2)")
let hidden = true;
function myFunction(x) {
    x.classList.toggle("change");
    if(hidden==true){
        navUl.style.display = "block";
        hidden = false
    }else{
        navUl.style.display = "none";
        hidden = true;
    }
  }