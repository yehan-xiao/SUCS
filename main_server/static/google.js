//Written by Yichen Liu
var map, json, max_lat, min_lat, min_lng, max_lng, obj;
var box = [];
var markers = [];
var list = [];
var rectangle;
var address;
var Windows = []; // used for clear all inforwindows
var curCoor;// This variable store the coordinate object when user click on th map.
            // Using lat() and lng() to get latitude and lngitude from this object.
            // E.g.  curCoor.lat() => latitude
var server_url= "/UCS";


function change_mode(button) {
    jQuery("#rect").css("background-color", "#009FE3");
    jQuery("#point").css("background-color", "#009FE3");
    jQuery("#normal").css("background-color", "#009FE3");
    button.css("background-color", "#ccc");
}

// function used to initialize static map
function loadGoogleMap(){
//change_map_engine(0);
	locationCentre = new google.maps.LatLng(52.95478319999999,-1.1581085999999914);
	var mapOptions = {
		center: locationCentre,
		zoom: 17,
		mapTypeControl: false,
		mapTypeId: google.maps.MapTypeId.ROADMAP,
		streetViewControl: false
	}
	var gMap = document.getElementById("container");
	map = new google.maps.Map(gMap, mapOptions);
}

// function to do the geocoding; turn address string to proper coordinate
function loadAddress(){
    /*
        below codes needs to get user input for address
    */
    //////////////////////////////////////////////////////
    removeMarkers();
    address = document.getElementById("suggestId").value;
    if(address != ""){
        geocoder.geocode( { 'address': address}, function(results, status) {
            if (status == 'OK') {
                map.setCenter(results[0].geometry.location);
                addMarker(results[0].geometry.location);
            } else {
                alert('Geocode was not successful for the following reason: ' + status);
            }
        });
    }
}

// function to add a normal listener to map (with click function)
function addListener(){
    google.maps.event.clearListeners(map, 'click');
    change_mode(jQuery("#point"));
    map.addListener('click', function(event) {
        addMarker(event.latLng);
    });
}

function gNormal(){
    change_mode(jQuery("#normal"));
    google.maps.event.clearListeners(map, 'click');
}

// function to add a listener to map with box ability
function addListener_box(){
    change_mode(jQuery("#rect"));
    google.maps.event.clearListeners(map, 'click');
    var contentImg;
    box = [];
    map.addListener('click', function(event){
        /*if(box.length == 2){
            box[0].setMap(null);
            box[1].setMap(null);
            box.length = 0;
            rectangle.setMap(null);
            removeMarkers();
        }*/
        var marker = new google.maps.Marker({
            position: event.latLng,
            map: map
        })
        box.push(marker);
        markers.push(marker);
        if(box.length%2 == 0){
            addRectangle();
            $('#searching_window, #overlay-back').fadeIn(500);
        }
    })
}

// function to plot a single marker on the map
function addMarker(latLng){
    var marker = new google.maps.Marker({
        position: latLng,
        map: map
    });
    var singleImg = {"bounding_box": [], "lat": latLng.lat().toFixed(6), "long": latLng.lng().toFixed(6), "url": "https://maps.googleapis.com/maps/api/streetview?size=600x600&location="+latLng.lat().toFixed(6)+","+latLng.lng().toFixed(6)+"&key=AIzaSyAoaOH-XDMVKlm8KJoCXDLR8Twkz0rVkcY"};
    marker.addListener('click',function(){
	display_one_image(singleImg);	
    })
    markers.push(marker);
    curCoor = latLng;
    gNormal();
}

function display_one_image(image) {
    console.log(image);
    const draw = (ctx, x, y, w, h, score, c) => {
        ctx.beginPath();
        ctx.rect(x, y, w, h);
        ctx.strokeStyle = c;
        ctx.stroke();
        ctx.font = '15px serif';
        ctx.fillText(score, x, y - 5);
    };
    var canvas_ = jQuery('#image');
    canvas_.data("position", { lat: image.lat, long: image.long });
    var ctx = canvas_[0].getContext('2d');
    var img = new Image();
    img.crossOrigin = "Anonymous";
    bounding_boxes = image.bounding_box;
    img.onload = function () {
        ctx.drawImage(img, 0, 0);
        for (i = 0; i < bounding_boxes.length; i++) {
            [xmin, ymin, xmax, ymax, score] = bounding_boxes[i];
            draw(ctx, xmin, ymin, xmax - xmin, ymax - ymin, score, 'red');
        }
        $('#image_window, #overlay-back').fadeIn(500);
    }
    img.src = "/image/" + encodeURIComponent(image.url);
}

function display_images(images) {
    var coo;
    for (i = 0; i < images.length; i++) {
	coo = new google.maps.LatLng(images[i].lat,images[i].long)
        addMarker(coo);
    }
}

function close_searching_window(){
    $("#image_analysis").attr("disabled", true);
    $('#searching_window, #overlay-back').fadeOut(500);
    for(i = 0;i < box.length; i++){
	box[i].setMap(null);
    }
    rectangle.setMap(null);
    gNormal();
}

function close_image_window() {
    $('#image_window, #overlay-back').fadeOut(500);
    gNormal();
}

function reject(){
    markers[markers.length-1].setMap(null);
    close_image_window();
}

// function to remove all markers and rectangle from the map
function removeMarkers(){
    for(var i = 0;i < markers.length;i++){
        markers[i].setMap(null);
    }
    rectangle.setMap(null);
    markers.length = 0;
    google.maps.event.clearListeners(map, 'click');
    addListener();
}

// function to add proper rectangle to map
function addRectangle(){
    var l = box.length;
    var a = box[l-2].position.lat();
    var b = box[l-2].position.lng();
    var c = box[l-1].position.lat();
    var d = box[l-1].position.lng();
    var e = larger(a,c);
    var f = larger(b,d);
    var bounds = {
        north: e[0],
        south: e[1],
        east: f[0],
        west: f[1]
    }
    rectangle = new google.maps.Rectangle({
        bounds: bounds,
        editable: false,
    });
    rectangle.setMap(map);
    max_lat = bounds.north;
    min_lat = bounds.south;
    max_lng = bounds.east;
    min_lng = bounds.west;
}

function loadAddress_box(){
	var addr = document.getElementById('placename').value;
        var service = new google.maps.places.PlacesService(map);
        var southWest = new google.maps.LatLng(min_lat, min_lng);
        var northEast = new google.maps.LatLng(max_lat, max_lng);/////////////////////////////
        var Bounds = new google.maps.LatLngBounds(southWest, northEast);
        var request = {
            query: addr,
            bounds: Bounds
        }
        service.textSearch(request,callback);
}

function callback(results,status){
    if (status == google.maps.places.PlacesServiceStatus.OK) {
        //alert("found "+results.length+" points.");
        list = [];
        for (var i = 0; i < results.length; i++) {
            if(isInBounds(results[i].geometry.location)){
                list.push(results[i]);
                addMarker(results[i].geometry.location);
            }
	    close_searching_window();
        }
    }
}

function isInBounds(latLng){
    lat = latLng.lat();
    lng = latLng.lng();
    if(lat >= min_lat && lat <= max_lat){///////////////////
        if(lng >= min_lng && lng <= max_lng){
            return true;
        }else{
            return false;
        }
    }else{
        return false;
    }
}

// function to decode coordinates the user clicked to box's bounding coordinates
function larger(a,b){
    var numa = parseFloat(a);
    var numb = parseFloat(b);
    var result = [];
    if(numa>numb){
        result[0] = numa;
        result[1] = numb;
    }else{
        result[0] = numb;
        result[1] = numa;
    }
    return result;
}
