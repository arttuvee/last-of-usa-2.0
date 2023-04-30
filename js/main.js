'use strict';
/* 1. show map using Leaflet library. (L comes from the Leaflet library) */

const map = L.map('map').setView([37.8, -96], 4);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'}).addTo(map);

// global variables
const apiUrl = 'http://127.0.0.1:3000/';

// icons
const blueIcon = L.divIcon({className:'blue-icon'});
const greenIcon = L.divIcon({className:'green-icon'});
const not_in_range_Icon = L.divIcon({className:'not-in-range-icon'});

// form for player name - Asks for player name and after submit disappears
document.querySelector('#player-form').addEventListener('submit', function(evt) {
    evt.preventDefault();
    const playerName = document.querySelector('#player-input').value;
    document.querySelector('#player-modal').classList.add('hide');

    // pass the player name from the form to the url
    gameSetup(`http://127.0.0.1:3000/creategame?name=${playerName}`);
});

// function to fetch data from API
async function fetchData(url) {
    const response = await fetch(url);
    console.log(response)

    //if wrong data is sent there will be error message and it won't continue.
    if (!response.ok) throw new Error('Invalid server input!');
  return await response.json();
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
  document.querySelector('#player-name').innerHTML = `Player: ${status.status.name}`;
  document.querySelector('#player-location').innerHTML = status.status.current_airport[0].name;
  document.querySelector('#range-left').innerHTML = status.status.battery_range;
  document.querySelector('#days-left').innerHTML = status.status.days_left;

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
async function gameSetup(url) {
    try {

        // Fetches a JSON that has all the data for a new game
          const gameData = await fetchData(url);

          // Adds a marker for the starting airport
          const current_location_marker = L.marker([gameData.status.current_airport[0].latitude_deg, gameData.status.current_airport[0].longitude_deg]).addTo(map)
            .bindPopup(`<b>This is the starting airport</b> <br>${gameData.status.current_airport[0].name}`).openPopup();

        // Set current location icon to blue
        current_location_marker.setIcon(blueIcon)


        // Iterate over all airports
        for (let i = 0; i < gameData.all_airports.length; i++) {

          // Access one specific airport from the dataset
          let airport = gameData.all_airports[i];

          // Using a boolean determine if airport is in range --> green marker
          if (airport.in_range){
            // Add a map marker for a specific airport
            const airport_marker = L.marker([airport.latitude_deg, airport.longitude_deg]).addTo(map);
            airport_marker.setIcon(greenIcon);

            // Make a div for where all popup content is stored
            const popupContent = document.createElement('div')
            const h4 = document.createElement('h4')
            h4.innerHTML = airport.name
            popupContent.append(h4)

            // Add 'Fly here' button to popup content
            const goButton = document.createElement('button')
            goButton.classList.add('button')
            goButton.innerHTML = 'Fly here'
            popupContent.append(goButton)

            // Add text content to popup content
            const p = document.createElement('p')
            p.innerHTML = `This airport is ${airport.distance_to}km away!`
            popupContent.append(p)

            airport_marker.bindPopup(popupContent)

            }
          // If the in_range boolean is false --> gray marker
          else{
            const airport_marker = L.marker([airport.latitude_deg, airport.longitude_deg]).addTo(map);
            airport_marker.setIcon(not_in_range_Icon);

            // Make a div for where all popup content is stored
            const popupContent = document.createElement('div')
            const h4 = document.createElement('h4')
            h4.innerHTML = airport.name
            popupContent.append(h4)

            // Add text content to popup content
            const p = document.createElement('p')
            p.innerHTML = `You dont have enough range!`
            popupContent.append(p)

            airport_marker.bindPopup(popupContent)
          }
        }
        // Send gameData to updateStatus function
        updateStatus(gameData);

    } catch (error) {
        console.log(`this is gameSetup catch block error: ${error}`);
    }
}



