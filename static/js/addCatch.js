// Initialize and add the map
let map;
let marker; // Declare marker here

// Moves the marker on the map.
function moveMarker(location, map, marker) {
  // Set the marker's position.
  marker.setPosition(location);
  map.panTo(location); // Optional: re-center the map on the new marker.
  console.log(location.lat() + ', ' + location.lng()); // Log or store location

  // Update the hidden form fields with the new location
  document.getElementById('latitude').value = location.lat();
  document.getElementById('longitude').value = location.lng();
}

async function initMap() {
  // The location of Uluru
  const position = { lat: 35.612, lng: -77.366};
  // Request needed libraries.
  //@ts-ignore
  const { Map } = await google.maps.importLibrary("maps");
  const { AdvancedMarkerElement } = await google.maps.importLibrary("marker");

  // The map, centered at Uluru
  map = new Map(document.getElementById("map"), {
    zoom: 4,
    center: position,
    mapId: "DEMO_MAP_ID",
    
  });
  console.log("Map loaded");

  // The marker, positioned at Uluru
  marker = new google.maps.Marker({
    position: position,
    map: map,
    title: "Uluru",
  });

  // This event listener will call moveMarker() when the map is clicked.
  map.addListener('click', function(event) {
    console.log(event.latLng.lat() + ', ' + event.latLng.lng());
    
    moveMarker(event.latLng, map, marker);
  });
}

initMap();