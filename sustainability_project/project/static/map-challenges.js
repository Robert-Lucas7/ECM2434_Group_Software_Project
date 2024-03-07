const MIN_ZOOM = 14;
const EXETER_BOUNDS = L.latLngBounds([50.742380, -3.524876], [50.731452, -3.545301])
const EXETER_CENTER = [50.737096, -3.535094]
const RADIUS = 80

var env_icon = L.icon({
    iconUrl: marker_pic,

    iconSize:     [35, 35], // size of the icon
});

var map = L.map('map', {
    center: EXETER_CENTER,
    maxBounds: EXETER_BOUNDS,
    minZoom: MIN_ZOOM
}).setView(EXETER_CENTER, MIN_ZOOM);


L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

// console.log(challenges[0][2])

for(let i=0; i<challenges.length; i++){
    let coordinates = [challenges[i][1], challenges[i][2]]

    let marker = L.marker(coordinates, {icon: env_icon}).addTo(map);
    marker.bindPopup("<b>" + challenges[i][0] + "</b>");
}

