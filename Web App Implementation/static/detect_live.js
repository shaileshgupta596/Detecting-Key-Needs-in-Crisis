
var tweet_slider = document.getElementById("tweet_slider");
var tweet_slider_coords = tweet_slider.getBoundingClientRect();
var bottomBorder = tweet_slider_coords.bottom;

var redLables = ['affected_people', 'caution_and_advice','deaths_reports','disease_signs_or_symptoms', 'disease_transmission',
'displaced_people_and_evacuations','donation_needs_or_offers_or_volunteering_services','infrastructure_and_utilities_damage', 
'injured_or_dead_people','missing_trapped_or_found_people','not_related_or_irrelevant','other_useful_information','prevention',
'sympathy_and_emotional_support', 'treatment']

var intToLabel = {1:'missing_trapped_or_found_people',
       2:'affected_injured_dead_death',
       3:'donation_needs_or_offers_or_volunteering_services',
       4:'sympathy_and_emotional_support', 
       5:'not_related_or_irrelevant',
       6:'prevention_caution_and_advice',
       7:'infrastructure_and_utilities_damage',
       8:'disease_transmission_signs_or_symptoms',
       9:'treatment'}

var stop_btn = document.getElementById("stop_btn");
var download_btn = document.getElementById("download_btn");
var heading = document.getElementById("heading");

var socket = io.connect('http://' + document.domain + ':' + location.port);

heading.addEventListener("click", function()
{
    var loc ='http://' + document.domain + ':' + location.port
    window.open(loc, "_self");
});

stop_btn.addEventListener("click", function()
{
	socket.emit('stop_tweets');
	socket.emit('download_tweets');
    var buttonSpace = document.getElementById("control_btn_space");
    buttonSpace.innerHTML = "<span class='stopNotification'>Stopping tweet stream...</span>"
});

socket.on('stop_tweets', function(msg) {
    console.log('stop_tweets ',msg["tweet"]);
    var buttonSpace = document.getElementById("control_btn_space");
    buttonSpace.innerHTML = "<span class='stopNotification'>Tweet stream stopped!</span>"
});

download_btn.addEventListener("click", function()
{
	socket.emit('download_tweets');
});

socket.on('download_tweets', function(msg) {
    console.log('download_tweets ',msg["tweet"]);
    var loc ='http://' + document.domain + ':' + location.port+'/download'
    window.open(loc, "_blank"); 
        
});


function real_tweet_slider(t)
{
	var lastChild = tweet_slider.lastElementChild;	
	var lastChild_coords = lastChild.getBoundingClientRect();
	var tweet = document.createElement("div");
	tweet.className = "tweet";
	tweet.innerText = t;
	if((bottomBorder-40)<=lastChild_coords.bottom)
	{
		var firstChild = tweet_slider.firstChild;
		tweet_slider.removeChild(firstChild);
	}
	tweet_slider.insertBefore(tweet, lastChild.nextSibling);
}

function increment(label)
{
	console.log("TypeOF : "+typeof(label));
	console.log(intToLabel[label].concat("_label"));
    var e=document.getElementById(intToLabel[label]);
    var e_label = document.getElementById(intToLabel[label].concat("_label"))
	e.innerText = parseInt(e.innerText)+1;
	e.parentElement.parentElement.style.transition="transform 1.6s";
	e.parentElement.parentElement.style.transform = "rotateY(360deg)";
	e.parentElement.parentElement.style.backgroundColor="white";
    e.parentElement.parentElement.style.border="solid";
	e.parentElement.parentElement.style.borderColor="black";
	/*e.parentElement.parentElement.style.backgroundColor="#ffcb9a";*/
	/*e.parentElement.parentElement.style.color="black !important";*/
	e.style.color="black";
	e_label.style.color="black";
}
// verify our websocket connection is established
socket.on('CONNECTION', function(msg) {
    console.log('CONNECTION wala:  ',msg);
});

socket.emit('hashtag_recieved?');

socket.on('hashtag_recieved?', function(msg) {
    console.log('Hashtag Recieved ? ',msg);
    //tweet_slider_function();
});

socket.emit('send_tweets');
socket.on('send_tweets', function(msg) {
    //console.log('send_tweets ',msg["tweet"]);
    real_tweet_slider(msg["tweet"]);
    //tweet_slider_function();
});

socket.emit('send_prediction');
socket.on('send_prediction', function(msg) {
    //console.log('send_prediction ',msg["class"]);
   increment(msg["class"])
});

/*function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function tweet_slider_function()
{

	for(var i =0;i<=50;i++)
	{
		var lastChild = tweet_slider.lastElementChild;
		console.log(lastChild.className);
		var lastChild_coords = lastChild.getBoundingClientRect();
		var tweet = document.createElement("div");
		tweet.className = "tweet";
		tweet.innerText = i;
		if((bottomBorder-40)<=lastChild_coords.bottom)
		{
			
			var firstChild = tweet_slider.firstChild;
			tweet_slider.removeChild(firstChild);
		}
		tweet_slider.insertBefore(tweet, lastChild.nextSibling);
		await sleep(250);
	}
}
*/