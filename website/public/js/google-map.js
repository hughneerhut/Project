// JavaScript source code

function initMap() {
    var directionsService = new google.maps.DirectionsService;
    var directionsDisplay = new google.maps.DirectionsRenderer;
    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 7,
        center: { lat: 37.81, lng: 144.96 }
    });
    directionsDisplay.setMap(map);

    var onChangeHandler = function () {
        DisplayRoute(directionsService, directionsDisplay);
    };
    document.getElementById('display').addEventListener('change', onChangeHandler);
}

function DisplayRoute(directionsService, directionsDisplay) {
    directionsService.route({
        origin: 3135 //NEED TO REQUEST START POSITION HERE,
        destination: 3140, //NEED TO REQUEST END POSITION HERE
        travelMode: 'DRIVING'
    }, function (response, status) {
        if (status === 'OK') {
            directionsDisplay.setDirections(response);
        } else {
            window.alert('Directions request failed due to ' + status);
        }
    });
}
