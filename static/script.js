
var userposition=null;
var mymap=null;
var markerlist=new Object();
var previd=null;

var greenIcon=L.icon({iconUrl:'wastebin.png', iconSize:     [30, 50], // size of the icon
    // size of the shadow
    iconAnchor:   [15, 25], // point of the icon which will correspond to marker's location
   // the same for the shadow
    popupAnchor:  [-3, -10] // point from which the popup should open relative to the iconAnchor})
    });

var redIcon=L.icon({iconUrl:'wastebin1.png', iconSize:     [25, 42], // size of the icon
    // size of the shadow
    iconAnchor:   [15, 25], // point of the icon which will correspond to marker's location
   // the same for the shadow
    popupAnchor:  [-3, -10] // point from which the popup should open relative to the iconAnchor})
    });
// window load function
function myfunc(){
	mymap = L.map('mapid').fitWorld();
	L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
		maxZoom: 18,
		attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' +
			'<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
			'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
		id: 'mapbox.streets'
	}).addTo(mymap);

	 if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(getposition, errorPosition, {maximumAge:600000, timeout:5000, enableHighAccuracy: true});
    }
    else{
	 errorPosition();
	}
}


// get user cordinates
function getposition(position){
	userposition=position;
    console.log(position.coords.accuracy);
    var rad=position.coords.accuracy/2;
    var circle = L.circle([position.coords.latitude,position.coords.longitude], {
    color: 'red',
    fillColor: '#f03',
    fillOpacity: 0.2,
    radius: rad,
}).addTo(mymap).bindPopup("Current Location");


	getmap( position.coords.latitude, position.coords.longitude);
}

// get cordinates of first bin from database
function errorPosition(error){
	alert("location denied");
}

// display the map using cordinates
function getmap(lat, long){
	mymap.setView([lat, long], 12);
	getBin(mymap);
}

// get Bin locations from database
function getBin(mymap){
	var oReq = new XMLHttpRequest;
	XMLHttpRequest.responseType="json";
	oReq.onload = function(){
		//alert(this.response);
		var res=JSON.parse(this.response);
        if(res){
		  addMarker(mymap, res);
        }  
	};
	oReq.open("get", "get_garbage_bin_cordinates.php");
	oReq.send();
}

// add markers to bin locations
function addMarker(mymap, binArray){
	for(var obj in binArray){
		if(binArray.hasOwnProperty(obj)){
			let marker=L.marker([binArray[obj]["latitude"],binArray[obj]["longitude"]]).addTo(mymap);
			marker.setIcon(redIcon);
			markerlist[obj]=marker;
			marker.bindPopup("Level : "+ binArray[obj]["level"] + "  ID: " + binArray[obj]["id"]);
		}		

	}
}

function getLoc(){
	if(userposition){
		mymap.setView([userposition.coords.latitude, userposition.coords.longitude],12);
		var oReq = new XMLHttpRequest(); //New request object
	    XMLHttpRequest.responseType = "json";
   		oReq.onload = function() {
        //This is where you handle what to do with the response.
        //The actual data is found on this.responseText
        var res=JSON.parse(this.response);
        if(res){
        if(previd!=null){
        	markerlist[previd].setIcon(redIcon);
        }
        let curid=res["id"];
        previd=curid;
        var toggle=true;
        setInterval(function(){ 
        	if(toggle){
        		markerlist[curid].setIcon(greenIcon);
        	}
        	else{
        		markerlist[curid].setIcon(redIcon);
        	}
        	toggle=!toggle;
         }, 2000);
        }
        //markerlist[curid].setIcon(greenIcon);

        //alert(this.response);
    	};
    oReq.open("post", "getnearestbin.php", true);
    oReq.setRequestHeader("Content-Type", "application/json");
    var data = JSON.stringify({"lat": userposition.coords.latitude, "long": userposition.coords.longitude});
    oReq.send(data);
	}
	else{
		alert("geolocation not avaliable");
	}
}

var scanner;
function qrScanner(){
	 scanner = new Instascan.Scanner({ video: document.getElementById('preview'),refractoryPeriod:2000 });
      scanner.addListener('scan', function (content) {
        console.log(content);
        var qrReq=new XMLHttpRequest;
        XMLHttpRequest.responseType="json";
        qrReq.onload = function(){
        	var res=JSON.parse(this.response);
        	var pcode=res["promocode"];
        	//alert(this.response);
        	closeScanner(true, pcode);
        }
        var data=JSON.stringify({"id":content});
        qrReq.open("post", "getpromocode.php", true);
    	qrReq.setRequestHeader("Content-Type", "application/json");
    	qrReq.send(data);
      });
      Instascan.Camera.getCameras().then(function (cameras) {
        if (cameras.length > 0) {
          scanner.start(cameras[0]);
        } else {
          console.error('No cameras found.');
        }
      }).catch(function (e) {
        $("#myModal").modal("hide");
        console.error(e);
      });
}

function closeScanner(flag, data){
	scanner.stop();
    if(flag){
        $("#promop").children('span').text(data);
        $("#myModal").modal("hide");
        $("#promomodal").modal();
    }
	

}