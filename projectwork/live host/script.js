let flag=0;
const zero = document.getElementsByClassName("zero-float");
for(const element of zero)
{

  element.addEventListener("click",()=>{
    document.getElementById("layer").style.display="block";
    document.getElementById("zero-float").style.visibility="visible";
  
  })

}
const one = document.getElementsByClassName("one-float");
for(const element of one)
{
  
  element.addEventListener("click",()=>{
  
    document.getElementById("layer").style.display="block";
    document.getElementById("one-float").style.visibility="visible";
    
  })

}
const entry_zero = document.getElementsByClassName("flat-adder");
for(const element of entry_zero)
{
  
  element.addEventListener("click",()=>{
    document.getElementById("zero-float").style.visibility="hidden";
    document.getElementById("layer").style.display="none";
    document.getElementById("one-float").style.visibility="hidden";
  })
}

/* const zeroFloatClickHandler = () => {
  zeroFloatDiv.style.visibility = "visible";
};

const zeroFloatDivs = document.querySelectorAll(".zero-float");

zeroFloatDivs.forEach(d => {
    console.log("Print");
  d.addEventListener("click", zeroFloatClickHandler);
}); */