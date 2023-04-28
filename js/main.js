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
  document.querySelector('#player-name').innerHTML = `Player: ${status.name}`;
  document.querySelector('#player-location').innerHTML = status.location;
}


// function to set up game
// this is the main function that creates the game and calls the other functions
async function gameSetup() {
    try {
        // Fetches a list of airports from a url
        const airportData = await fetchData('http://127.0.0.1:3000/airport');
        console.log(airportData);

        // Iterates over the search result and adds a map-marker for them
        for (let airport of airportData) {
            const marker = L.marker([airport.latitude_deg, airport.longitude_deg]).addTo(map)
            .bindPopup(airport.name);
        }
        const gameData = await fetchData('http://127.0.0.1:3000/creategame');
        console.log(gameData);
                    const marker = L.marker([gameData.airport_data.latitude_deg, gameData.airport_data.longitude_deg]).addTo(map)
                    .bindPopup(`<b>This is the starting airport</b> <br>${gameData.airport_data.name}`)
                    .openPopup();
        updateStatus(gameData.status);
    } catch (error) {
        console.log(error);
    }
}



gameSetup();



// event listener to hide goal splash


