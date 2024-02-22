const MIN_ZOOM = 12;
const EXETER_BOUNDS = L.latLngBounds([50.759496, -3.583118], [50.693802, -3.440272])

console.log(context)

// creating map and setting parameters
let map = L.map('map', {
    center: EXETER_BOUNDS.getCenter(),
    maxBounds: EXETER_BOUNDS,
    minZoom: MIN_ZOOM
}).setView(EXETER_BOUNDS.getCenter(), MIN_ZOOM);

// adding map tile from openstreetmap
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

// adding marker and binding popup
marker_bounds = EXETER_BOUNDS.getCenter()
let marker = L.marker(marker_bounds).addTo(map);
marker.bindPopup("<b>Challenge Name</b><br>Description about challange");

let RADIUS = 500
let circle_bounds = [50.736542, -3.537569]
let circle = L.circle(circle_bounds, {radius: RADIUS}).addTo(map);

var fromLatLng = L.latLng(marker_bounds);
var toLatLng = L.latLng(circle_bounds);

var dis = fromLatLng.distanceTo(toLatLng);
console.log(dis);
document.querySelector("#share").addEventListener(
    "click", () => {
        findMyCoordinates()
    }
)

function inCircle(distance){
    return distance < RADIUS;
}

// location marker
function markLocation(position) {
    const coordinates = [position.coords.latitude, position.coords.longitude];

    let marker = L.marker(coordinates).addTo(map);
    marker.bindPopup("<b>Current Location</b>");

    // Hide the loading message
    document.getElementById("loading").style.display = "none";

    // Disable further clicks on the button
    document.getElementById("share").disabled = false;
}

// finds coordinates and calls markLocation on those coordinates
function findMyCoordinates() {
    if (navigator.geolocation) {
        // Show the loading message
        document.getElementById("loading").style.display = "block";
        document.getElementById("share").disabled = true;

        navigator.geolocation.getCurrentPosition(
            markLocation,
            (err) => {
                alert(err.message);
                // Re-enable the button in case of an error
                document.getElementById("share").disabled = false;
                document.getElementById("loading").style.display = "none";
            }
        );
    } else {
        alert("Geolocation is not supported by your browser");
    }
}
