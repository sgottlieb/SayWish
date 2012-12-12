function check_value(val, section){
  if(val===""){
    document.getElementById(section).style.display='block'
  }
  else{
    document.getElementById(section).style.display='none'
  }
}

function close_this_window(){
	alert("Wish Added!");
	window.close();
}