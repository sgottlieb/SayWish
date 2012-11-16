// this let's you click, mouse over and collect div ids and sends to get_wish/ on third click

var jQueryLib = document.createElement("script");
jQueryLib.src = "http://code.jquery.com/jquery-1.6.1.min.js";
document.body.appendChild(jQueryLib);
var items = [];
var click_listener;
var capturing = false;
var click_time = 1;

click_listener = addEventListener('click', function(){
	capturing = !capturing;
	click_time = click_time + 1;
	if (click_time===3){
		$.ajax({
  			type: 'POST',
  			url: 'http://127.0.0.1:5000/get_wishes/?items='+encodeURIComponent(items)+'&weburl='+encodeURIComponent(document.URL),
  			success: alert('success'),
  			dataType: 'jsonp'
		});
		window.open('http://127.0.0.1:5000/get_wishes/?items='+encodeURIComponent(items)+'&weburl='+encodeURIComponent(document.URL), 
						"myWindow", 
						"status = 1, height = 300, width = 300, resizable = 0");
	};
});
var mouse_listener = document.addEventListener('mouseover', function(evt) {
	if (capturing) {
		saywish_item = evt.target;
		items.push(saywish_item.getAttribute('class'));
		console.log('adding item')
	}
});

//issue with searching children of div with classes that it's searching for
// var jQueryLib = document.createElement("script");
// jQueryLib.src = "http://code.jquery.com/jquery-1.6.1.min.js";
// document.body.appendChild(jQueryLib);
// var items = [];
// var click_listener;
// var capturing = false;
// var click_time = 1;

// click_listener = addEventListener('click', function(){
// 	capturing = !capturing;
// 	click_time = click_time + 1;
// 	if (click_time===3){
// 		$.ajax({
//   			type: 'POST',
//   			url: 'http://127.0.0.1:5000/get_wishes/?items='+encodeURIComponent(items)+'&weburl='+encodeURIComponent(document.URL),
//   			success: alert('success'),
//   			dataType: 'jsonp'
// 		});
// 	};
// });
// var mouse_listener = document.addEventListener('mouseover', function(evt) {
// 	if (capturing) {
// 		saywish_item = evt.target;
// 		items.push(saywish_item.getAttribute('class'));
// 		console.log('adding item')
// 	}
// });



// $.ajax({
//   type: 'POST',
//   url: 'http://127.0.0.1:5000/get_wishes?items='+encodeURIComponent(items)+'?url='+encodeURIComponent(document.URL),
//   dataType: 'jsonp'
// });

// $.post('http://127.0.0.1:5000/get_wishes?items='+encodeURIComponent(items)+'?url='+encodeURIComponent(document.URL))




// $.ajax({
//   type: 'POST',
//   url: 'http://127.0.0.1:5000/get_wishes?items='+encodeURIComponent(items)+'?url='+encodeURIComponent(document.URL)),
//   dataType: 'jsonp'
// });

// dataType: 'jsonp'

// function send_info(entry) {
//   $.post(Parse.ApplicationUrl,
//     JSON.stringify({objectId: entry.objectId, number: entry.number}),
//     function(data) {
//       App.phoneNumberIds[data.objectId] = data ;
//     }
//   );
// }
// var move_things = location.href='get_wish.html'
// 								+encodeURIComponent(document.URL)
// 								+'&items=''file:///Users/saragottlieb/Desktop/SayWish/templates/get_wish.html'
// 								+encodeURIComponent(document.URL)
// 								+'&items='+encodeURIComponent(items)
// $.post(string)


// var post_action = '/post_items?items=' + encodeURIComponent(items) + '&url='+
// 								+'?weburl='+document.URL

// //maybe add numbers to help with push
// 		// console.log(saywish_item);
// 			// console.log(evt);
// 				console.log(saywish_item.getAttribute('id'));