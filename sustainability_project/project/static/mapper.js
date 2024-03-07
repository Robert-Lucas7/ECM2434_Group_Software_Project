


function inCircle(distance, radius){
    return distance < radius;
}

// location marker
function markLocation(position) {
    const coordinates = [position.coords.latitude, position.coords.longitude];

    let marker = L.marker(coordinates).addTo(map);
    marker.bindPopup("<b>Current Location</b>");

    // re-enable
    document.getElementById("submitBtn").disabled = false;
}

// finds coordinates and calls markLocation on those coordinates
function findMyCoordinates() {
    return new Promise((resolve, reject) => {
        if (navigator.geolocation) {
            // Disable while loading
            document.getElementById("submitBtn").disabled = true;

            navigator.geolocation.getCurrentPosition(
                position => {
                    markLocation(position);
                    const coordinates = [position.coords.latitude, position.coords.longitude];
                    // // Re-enable the button
                    document.getElementById("submitBtn").disabled = false;
                    resolve(coordinates); // Resolve with the coordinates
                },
                err => {
                    reject(err.message); // Reject with error message
                    // Re-enable the button in case of an error
                    document.getElementById("submitBtn").disabled = false;
                }
            );
        } else {
            alert("Geolocation is not supported by your browser");
            reject("Geolocation not supported");
        }
    });
}

if (LAT != "None"){
    const MIN_ZOOM = 14;
    const EXETER_BOUNDS = L.latLngBounds([50.742380, -3.524876], [50.731452, -3.545301])
    const EXETER_CENTER = [50.737096, -3.535094]
    const CIRCLE_BOUNDS = [LAT, LONG]
    const RADIUS = 80

    var map = L.map('map', {
        center: EXETER_CENTER,
        maxBounds: EXETER_BOUNDS,
        minZoom: MIN_ZOOM
    }).setView(EXETER_CENTER, MIN_ZOOM);



    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map);

    var circle = L.circle(CIRCLE_BOUNDS, {radius: RADIUS}).addTo(map);

    document.querySelector("#submitBtn").addEventListener(
    "click", function(event) {
        event.preventDefault()
        findMyCoordinates()
          .then(coordinates => {
              console.log("Coordinates:", coordinates);
              let fromLatLng = L.latLng(coordinates);
              let toLatLng = L.latLng(CIRCLE_BOUNDS);
              let distance = fromLatLng.distanceTo(toLatLng);

              if(inCircle(distance, RADIUS)) {
                  document.getElementById('userLat').value = coordinates[0]
                  document.getElementById('userLong').value = coordinates[1]
                  document.getElementById('MakePost').submit();
              } else {
                  alert("You are not near the location")
              }
          })
         .catch(error => {
            console.error("Error:", error);
                 // Handle error
         });

    }
)
}


