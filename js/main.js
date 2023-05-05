'use strict';

// Establish leaflet map into the game
const map = L.map('map').setView([37.8, -96], 4);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
  maxZoom: 19,
  attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
}).addTo(map);

// global variables
const apiUrl = 'http://127.0.0.1:3000/';
let days_left = 10

// icons
const blueIcon = L.divIcon({className: 'blue-icon'});
const greenIcon = L.divIcon({className: 'green-icon'});
const not_in_range_Icon = L.divIcon({className: 'not-in-range-icon'});
const goldenIcon = L.divIcon({className: 'golden-icon'})
const airportMarkers = L.featureGroup().addTo(map);

// form for player name - Asks for player name and after submit disappears
document.querySelector('#player-form').
    addEventListener('submit', function(evt) {
      evt.preventDefault();
      const playerName = document.querySelector('#player-input').value;
      document.querySelector('#player-modal').classList.add('hide');

      // pass the player name from the form to the url and start a new game
      gameSetup(`http://127.0.0.1:3000/creategame?name=${playerName}`);
    });

// function to fetch data from API
async function fetchData(url) {
  const response = await fetch(url);
  console.log(response);

  //if wrong data is sent there will be error message and it won't continue.
  if (!response.ok) throw new Error('Invalid server input!');
  return await response.json();
}

// function to check if game is over
function checkGameOver(range) {
  if (range <= 0) {
    alert(
        `You ran out of range Game Over. ${globalGoals.length} goals reached.`);
    return false;
  }
  return true;
}

function updateStatus(gameData) {

  // Insert player name and range to the HTML-page. Source for information is the 'status' part of the JSON
  document.querySelector(
      '#player-name').innerHTML = `Player: ${gameData.status.name}`;
  document.querySelector(
      '#player-location').innerHTML = gameData.current_airport.name;
  document.querySelector('#range-left').innerHTML = Math.round(
      gameData.status.battery_range);
  document.querySelector('#days-left').innerHTML = Math.round(days_left);
  document.querySelector('#dialogue-target').innerHTML = gameData.status.event;

  // Update recourse icon colours if player finds them. Gets the data from same 'status'
  if (gameData.status.water_collected === true) {
    document.querySelector('#water-outline').classList.add('config-1');
  }
  if (gameData.status.food_collected === true) {
    document.querySelector('#fast-food-outline').classList.add('config-1');
  }
  if (gameData.status.solar_collected === true) {
    document.querySelector('#sunny-outline').classList.add('config-1');
  }
  if (gameData.status.medicine_collected === true) {
    document.querySelector('#medkit-outline').classList.add('config-1');
  }
  // Check if all recources are found
  if (gameData.status.water_collected && gameData.status.food_collected && gameData.status.solar_collected && gameData.status.medicine_collected) {
    if (gameData.final_airport.in_range){

        // Add a map marker for the final airport
        const final_airport_marker = L.marker([gameData.final_airport.latitude_deg, gameData.final_airport.longitude_deg]).addTo(map);
        final_airport_marker.setIcon(goldenIcon);
        airportMarkers.addLayer(final_airport_marker)

        // Make a div for where all popup content is stored
        const popupContent = document.createElement('div')
        const h4 = document.createElement('h4')
        h4.innerHTML = gameData.final_airport.name
        popupContent.append(h4)

        // Add 'End game' button to popup content
        const goButton = document.createElement('button')
        goButton.classList.add('button')
        goButton.innerHTML = 'End game'
        popupContent.append(goButton)

        // Add text content to popup content
        const p = document.createElement('p')
        p.innerHTML = `<b>You have collected all necessary resources and the airport is only
        ${Math.round(gameData.final_airport.distance_to)}km away! <br> Your crew is waiting for you already <b>`
        popupContent.append(p)

        final_airport_marker.bindPopup(popupContent)
        popupContent.classList.add('popup');

        goButton.addEventListener('click',  function () {
          alert('Congrats you accomplished your mission!')
          // Tähän vois lisää viel esim sitä html elementtii
        });
    }

    if (gameData.final_airport.charge_possibility){

        // Add a map marker for the final airport
        const final_airport_marker = L.marker([gameData.final_airport.latitude_deg, gameData.final_airport.longitude_deg]).addTo(map);
        final_airport_marker.setIcon(goldenIcon);
        airportMarkers.addLayer(final_airport_marker)

        // Make a div for where all popup content is stored
        const popupContent = document.createElement('div')
        const h4 = document.createElement('h4')
        h4.innerHTML = gameData.final_airport.name
        popupContent.append(h4)

        // Add text content to popup content
        const p = document.createElement('p')
        p.innerHTML = `You have collected all necessary resources but your planes range doesnt reach key west! Try your luck at a large airport to try and gain more range to get you to Key west`
        popupContent.append(p)

        final_airport_marker.bindPopup(popupContent)
        popupContent.classList.add('popup');

    } else if (!gameData.final_airport.in_range && !gameData.final_airport.charge_possibility){
      alert('range loppu ja ei largeja rangessa')
    }
  }


  //if player doesn't have enough range to continue the game.
  const inRange = gameData.all_airports.filter(airport => airport.in_range);
  const noneRange = inRange.every(airport => !airport.in_range);

  if (noneRange) {
    setTimeout(() => {
    alert("Your plane has ran out of battery. Game over!");
  }, 500);
    const text = document.querySelector('#dialogue-target')
    text.textContent = "Your plane has ran out of battery. You didn't survive :("
  }
}

// Function to set up game - this is the main function that creates the game and calls the other functions
async function gameSetup(url) {
try {

    // Fetches a JSON that has all the data for a new game
    const gameData = await fetchData(url);

    // Clear old markers from the map
    airportMarkers.clearLayers();

    // Adds a marker for current airport
    const current_location_marker = L.marker([gameData.current_airport.latitude_deg, gameData.current_airport.longitude_deg])
    .addTo(map).bindPopup(`<b>You are here!</b> <br>${gameData.current_airport.name}`).openPopup();

    // Set current location icon to blue
    current_location_marker.setIcon(blueIcon)
    airportMarkers.addLayer(current_location_marker)

    // Iterate over all airports
    for (let i = 0; i < gameData.all_airports.length; i++) {

      // Access one specific airport from the dataset
      let airport = gameData.all_airports[i];

      // Using a boolean determine if airport is in range --> green marker
      if (airport.in_range){

        // Add a map marker for a specific airport
        const airport_marker = L.marker([airport.latitude_deg, airport.longitude_deg]).addTo(map);
        airport_marker.setIcon(greenIcon);
        airportMarkers.addLayer(airport_marker)

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
        p.innerHTML = `This ${airport.type} is ${airport.distance_to}km away`
        popupContent.append(p)

        airport_marker.bindPopup(popupContent)
        popupContent.classList.add('popup');

        goButton.addEventListener('click',  function () {
          if (airport.type === 'medium_airport'){
            document.querySelector('#day-usage-taget').innerHTML = `You've chosen to explore two medium airports during day ${Math.round(days_left)}.`;
            days_left -= 0.5;
          } else {
            document.querySelector('#day-usage-taget').innerHTML = `You've chosen to explore one large airport during day ${days_left}.`;
            days_left -= 1;
          }
          gameSetup(`http://127.0.0.1:3000/flyto?game=${parseInt(gameData.status.id)}&dest=${airport.ident}&dist=${airport.distance_to}&day=${days_left}`);
          gameSetup(`http://127.0.0.1:3000/flyto?game=${parseInt(gameData.status.id)}&dest=${airport.ident}&dist=${airport.distance_to}&day=${days_left}`);

        });
      }
      // If the in_range boolean is false --> gray marker
      else{
        const gray_airport_marker = L.marker([airport.latitude_deg, airport.longitude_deg]).addTo(map);
        gray_airport_marker.setIcon(not_in_range_Icon);

        airportMarkers.addLayer(gray_airport_marker);

        // Make a div for where all popup content is stored
        const popupContent = document.createElement('div')
        const h4 = document.createElement('h4')
        h4.innerHTML = airport.name
        popupContent.append(h4)

        // Add text content to popup content
        const p = document.createElement('p')
        p.innerHTML = `You dont have enough range!`
        popupContent.append(p)

        gray_airport_marker.bindPopup(popupContent)
        popupContent.classList.add('popup');
      }
    }
    // Send gameData to updateStatus function
    updateStatus(gameData);

} catch (error) {
    console.log(`this is gameSetup catch block error: ${error}`);
}
}
