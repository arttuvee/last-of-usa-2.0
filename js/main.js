'use strict';
/* 1. show map using Leaflet library. (L comes from the Leaflet library) */

const map = L.map('map').setView([37.8, -96], 4);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'}).addTo(map);

// global variables

// icons

// form for player name

// function to fetch data from API
async function fetchData(url) {
    const response = await fetch(url);
    if (!response.ok) throw new Error('Invalid server input!'); //if wrong data is sent there will be error message and it wont continue.
    const data = await response.json();
    return data;
}

// function to update game status

// function to show weather at selected airport

// function to check if any goals have been reached

// function to update goal data and goal table in UI

// function to check if game is over

// function to set up game
// this is the main function that creates the game and calls the other functions
async function gameSetup() {
    try {
        const gameData = await fetchData('testdata/testi.json');
        console.log(gameData);

        for (let airport of gameData.location) {
            const marker = L.marker([airport.latitude, airport.longitude]).addTo(map)
            .bindPopup('testi testes').openPopup();

        }

    } catch (error) {
        console.log(error);
    }
}

gameSetup();

// event listener to hide goal splash
