<!DOCTYPE html>
<html>
<head>
    <title>EV Stations - Smart Navigation</title>

    <link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css"/>
    <script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>

    <link rel="stylesheet" href="https://unpkg.com/leaflet-routing-machine/dist/leaflet-routing-machine.css"/>
    <script src="https://unpkg.com/leaflet-routing-machine/dist/leaflet-routing-machine.js"></script>

    <style>
        body {
            margin: 0;
            display: flex;
            font-family: 'Segoe UI', sans-serif;
            background: #000;
            color: #00ffff;
        }

        #sidebar {
            width: 30%;
            padding: 20px;
            background: #020617;
            overflow-y: auto;
        }

        .station {
            padding: 14px;
            margin: 10px 0;
            border-radius: 12px;
            cursor: pointer;
            border: 1px solid #00ffff55;
        }

        .station:hover {
            box-shadow: 0 0 15px #00ffff;
        }

        button {
            width: 100%;
            padding: 10px;
            margin-bottom: 8px;
            background: #00ffff;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-weight: bold;
        }

        #map {
            width: 70%;
            height: 100vh;
        }
    </style>
</head>

<body>

<div id="sidebar">
    <h2>⚡ EV Stations</h2>

    <button id="stopVoice">🛑 Stop Voice</button>

    <!-- FILTERS -->
    <button onclick="filterStations('all')">⚡ All</button>
    <button onclick="filterStations('Ather Fast')">⚡ Ather Fast</button>
    <button onclick="filterStations('Normal')">🔌 Normal</button>
    <button onclick="filterStations('Other EV')">🚗 Other EV</button>
    <button onclick="filterStations('available')">🟢 Available Only</button>

    <div id="list"></div>
</div>

<div id="map"></div>

<script>

// ---------------- DATA ----------------
const stations = [
    {name:"Ather Grid - Banjara Hills",lat:17.4126,lon:78.4482,type:"Ather Fast",available:true},
    {name:"Ather Grid - Jubilee Hills",lat:17.4319,lon:78.4070,type:"Ather Fast",available:false},
    {name:"Ather Grid - Begumpet",lat:17.4440,lon:78.4620,type:"Ather Fast",available:true},

    {name:"Gachibowli EV Hub",lat:17.4401,lon:78.3489,type:"Other EV",available:true},
    {name:"Hitech City Charger",lat:17.4435,lon:78.3772,type:"Other EV",available:false},

    {name:"Sarath City Mall",lat:17.4573,lon:78.3630,type:"Normal",available:true},
    {name:"Kondapur Station",lat:17.4698,lon:78.3566,type:"Normal",available:false},

    {name:"Secunderabad EV Hub",lat:17.4399,lon:78.4983,type:"Other EV",available:true},
    {name:"LB Nagar Station",lat:17.3457,lon:78.5520,type:"Normal",available:true}
];

// ---------------- MAP ----------------
const map = L.map('map').setView([17.3850, 78.4867], 12);

// ✅ FIX: Use CartoDB tiles — no referer restrictions, works from file://
L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/">CARTO</a>',
    subdomains: 'abcd',
    maxZoom: 19
}).addTo(map);

// ---------------- NAVIGATION ----------------
let routingControl = null;
let marker = null;
let currentStep = 0;
let routeSteps = [];
let watchId = null;

// 🔊 VOICE
function speak(text) {
    speechSynthesis.cancel();
    const msg = new SpeechSynthesisUtterance(text);
    speechSynthesis.speak(msg);
}

// 📏 DISTANCE
function getDistance(lat1, lon1, lat2, lon2) {
    const R = 6371000;
    const dLat = (lat2 - lat1) * Math.PI/180;
    const dLon = (lon2 - lon1) * Math.PI/180;

    const a =
        Math.sin(dLat/2)**2 +
        Math.cos(lat1*Math.PI/180) *
        Math.cos(lat2*Math.PI/180) *
        Math.sin(dLon/2)**2;

    return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
}

// START NAVIGATION
function startNavigation(lat, lon, name) {

    if (routingControl) map.removeControl(routingControl);

    currentStep = 0;
    routeSteps = [];

    routingControl = L.Routing.control({
        waypoints: [
            L.latLng(17.3850, 78.4867),
            L.latLng(lat, lon)
        ],
        routeWhileDragging: false,
        show: true
    }).addTo(map);

    speak("Starting navigation to " + name);

    routingControl.on('routesfound', function(e) {
        routeSteps = e.routes[0].instructions || [];
    });

    if (watchId) navigator.geolocation.clearWatch(watchId);

    watchId = navigator.geolocation.watchPosition(pos => {

        const userLat = pos.coords.latitude;
        const userLon = pos.coords.longitude;

        if (currentStep < routeSteps.length) {

            const step = routeSteps[currentStep];
            if (!step.latLng) return;

            const dist = getDistance(userLat, userLon, step.latLng.lat, step.latLng.lng);

            if (dist < 30) {
                speak(step.text);
                currentStep++;
            }
        }

    });
}

function showRoute(lat, lon, name) {
    startNavigation(lat, lon, name);
}

// STOP BUTTON
document.getElementById("stopVoice").onclick = () => {
    speechSynthesis.cancel();
    if (watchId) navigator.geolocation.clearWatch(watchId);
};

// ---------------- FILTER SYSTEM ----------------
let filteredStations = [...stations];

function renderStations() {

    listDiv.innerHTML = "";

    map.eachLayer(layer => {
        if (layer instanceof L.Marker) map.removeLayer(layer);
    });

    filteredStations.forEach(s => {

        const div = document.createElement("div");
        div.className = "station";

        div.innerHTML = `
            <b>${s.name}</b><br>
            ⚡ ${s.type}<br>
            ${s.available ? "🟢 Available" : "🔴 Busy"}
        `;

        div.onclick = () => {

            map.setView([s.lat, s.lon], 15);

            if (marker) map.removeLayer(marker);

            marker = L.marker([s.lat, s.lon])
                .addTo(map)
                .bindPopup(s.name)
                .openPopup();

            showRoute(s.lat, s.lon, s.name);
        };

        listDiv.appendChild(div);

        L.marker([s.lat, s.lon])
            .addTo(map)
            .bindPopup(`${s.name}<br>${s.type}`);
    });
}

function filterStations(type) {

    if (type === "all") {
        filteredStations = [...stations];
    }
    else if (type === "available") {
        filteredStations = stations.filter(s => s.available);
    }
    else {
        filteredStations = stations.filter(s => s.type === type);
    }

    renderStations();
}

// ---------------- INIT ----------------
const listDiv = document.getElementById("list");
renderStations();

</script>

</body>
</html>
