// Initialize the map at a default location and zoom level
var map = L.map('map').setView([0, 0], 2); // Start with a global view

// Add OpenStreetMap tiles
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// Check if there are any restaurants to display
if (restaurants.length > 0) {
    var bounds = L.latLngBounds();  // Create bounds to fit all markers

    // Loop through each restaurant and add a marker
    restaurants.forEach(function (restaurant) {
        // Check if latitude and longitude are valid
        if (!isNaN(restaurant.latitude) && !isNaN(restaurant.longitude)) {
            // Create a marker at the restaurant's location
            var marker = L.marker([restaurant.latitude, restaurant.longitude]).addTo(map);

            // Add a popup to the marker with restaurant details
            marker.bindPopup('<b>' + restaurant.name + '</b><br>' + restaurant.description);

            // Extend the map bounds to include this marker
            bounds.extend([restaurant.latitude, restaurant.longitude]);
        } else {
            console.error('Invalid coordinates for restaurant:', restaurant.name);
        }
    });

    // Adjust the map view to fit all the markers
    map.fitBounds(bounds);
} else {
    console.log("No restaurants available to display.");
}
