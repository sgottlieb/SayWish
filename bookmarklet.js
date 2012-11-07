// this let's you click, mouse over and collect div ids


var items = [];
var click_listener;
var capturing = false;
click_listener = addEventListener('click', function(){
	capturing = !capturing;
});
var mouse_listener = document.addEventListener('mouseover', function(evt) {
	if (capturing) {
		// console.log(evt);
		saywish_item = evt.target;
		console.log(saywish_item);
		console.log(saywish_item.getAttribute('id'));
		items.push(saywish_item.getAttribute('id'));
	}
});
