function check_value(val, section){
  if(val==="None, other"){
    document.getElementById(section).style.display='block'
  }
  else{
    document.getElementById(section).style.display='none'
  }
}