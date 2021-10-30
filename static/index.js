

function hide()
{

}
function check()
{

  if(this.checked){
    document.getElementById("otpbutton").disabled = false;
  }
  else{
    document.getElementById("otpbutton").disabled = true;
  }

}


document.getElementById("check").addEventListener("click",check);
