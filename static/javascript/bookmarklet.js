// this let's you click, mouse over and collect div ids and sends to get_wish/ on third click

var jQueryLib = document.createElement("script");
jQueryLib.src = "http://code.jquery.com/jquery-1.6.1.min.js";
document.body.appendChild(jQueryLib);
var items = [];
var click_listener;
var capturing = false;
click_listener = addEventListener('click', function(){
	capturing = !capturing;
	if (!capturing){
		$.ajax({
  			type: 'POST',
  			url: window.open('http://127.0.0.1:5000/get_wishes/?items='+encodeURIComponent(items)+'&weburl='+encodeURIComponent(document.URL), 
						"myWindow", 
						"status = 1, height = 300, width = 300, resizable = 0"),
  			dataType: 'jsonp'
		});
	}
});
var mouse_listener = document.addEventListener('mouseover', function(evt) {
	if (capturing) {
		saywish_item = evt.target;
		items.push(saywish_item.getAttribute('class'));
		console.log('adding item')
	}
});