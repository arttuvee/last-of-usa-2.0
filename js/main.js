'use strict';
/* 1. show map using Leaflet library. (L comes from the Leaflet library) */

const map = L.map('map').setView([37.8, -96], 4);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'}).addTo(map);

// global variables
const apiUrl = 'http://127.0.0.1:3000/';

// icons


// prompt for player name
/*
document.querySelector('player-form').addEventListener('submit', function(evt) {
    evt.preventDefault();
    const playerName = document.querySelector('#player-input').value;
    document.querySelector('#player-modal').classList.add('hide');
});
*/

// function to fetch data from API
async function fetchData(url) {
    const response = await fetch(url);
    console.log(response)

    //if wrong data is sent there will be error message and it won't continue.
    if (!response.ok) throw new Error('Invalid server input!');
    const data = await response.json();
    return data;
}



// function to update game status

// function to show weather at selected airport

// function to check if any goals have been reached

// function to update goal data and goal table in UI

// function to check if game is over
function checkGameOver(range) {
    if (range <= 0) {
        alert(`You ran out of range Game Over. ${globalGoals.length} goals reached.`)
        return false;
    }
    return true;
}

function updateStatus(status) {
    // Insert player name and range to the HTML-page. Source for information is the 'status' part of the JSON
  document.querySelector('#player-name').innerHTML = `Player: ${status.player_name}`;
  document.querySelector('#player-location').innerHTML = status.location;
  document.querySelector('#range-left').innerHTML = status.battery_range;
  document.querySelector('#days-left').innerHTML = status.days_left;

  // Update recourse icon colours if player finds them. Gets the data from same 'status'
  if (status.water_collected === 1) {
  document.querySelector('#water-outline').classList.add('config-1');
}
  if (status.food_collected === 1) {
  document.querySelector('#fast-food-outline').classList.add('config-1');
}
  if (status.solar_collected === 1) {
  document.querySelector('#sunny-outline').classList.add('config-1');
}
  if (status.medicine_collected === 1) {
  document.querySelector('#medkit-outline').classList.add('config-1');
}



}


// Function to set up game - this is the main function that creates the game and calls the other functions
async function gameSetup() {
    try {
        // Fetches a list of airports from an url
        const airportData = await fetchData('http://127.0.0.1:3000/airport');
        console.log(`This is all the airportData: ${airportData}`);

        // Iterates over the search result and adds a map-marker for them
        for (let airport of airportData) {
            const marker = L.marker([airport.latitude_deg, airport.longitude_deg]).addTo(map).bindPopup(airport.name);
        }

        // Fetches a JSON that has all the data for a new game
        const gameData = await fetchData('http://127.0.0.1:3000/creategame');
        console.log(`This is all the gameData ${gameData}`);
                    const marker = L.marker([gameData.start_airport_data.latitude_deg, gameData.start_airport_data.longitude_deg]).addTo(map)
                    .bindPopup(`<b>This is the starting airport</b> <br>${gameData.start_airport_data.name}`).openPopup();

        // Send gameData to updateStatus function
        updateStatus(gameData.status);

    } catch (error) {
        console.log(`this is gameSetup catch block error: ${error}`);
    }
}

gameSetup();


