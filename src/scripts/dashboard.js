document.addEventListener('DOMContentLoaded', async () => {
  const API_KEY = 'b5958d9b3908799da10532d190c26c36'; // Replace with your OpenWeather API key TBD
  const WEATHER_URL = 'https://api.openweathermap.org/data/2.5/weather';

  // Get reference to html elements
  const dashboardCards = document.querySelectorAll('.dashboard-card');

  // Function to fetch and populate weather data for the city
   // Fetch saved locations and populate the dashboard
   async function loadSavedLocations() {
    try {
      // Fetch saved locations from the server
      const response = await fetch('http://localhost:5000/dashboard/locations');
      if (!response.ok) throw new Error('Failed to fetch saved locations');  // Error if response fails
      const locations = await response.json();  // Parse the response as JSON

      // Loop through locations and fetch weather for each
      locations.forEach((location, index) => {
        if (dashboardCards[index]) {
          getWeather(location.city, dashboardCards[index]);  // Call getWeather to update card with weather
        }
      });
    } catch (error) {
      console.error('Error loading saved locations:', error);  // Log any error
    }
  }

  async function getWeather(city, card) {
    try {
      const response = await fetch(`${WEATHER_URL}?q=${city}&appid=${API_KEY}&units=metric`);  // API call to get weather
      if (!response.ok) throw new Error(`Failed to fetch weather for ${city}`);  // Error handling
      const data = await response.json();  // Parse weather data as JSON
      updateCardWithWeather(data, card, city);  // Update the card with weather data
    } catch (error) {
      console.error('Error fetching weather data:', error);  // Log error
    }
  }

  // Function to update the card with weather data
  function updateCardWithWeather(data, card, city) {
    const cityName = data.name;  // Extract city name from response
    const temperature = `${data.main.temp}°C`;  // Get the temperature
    const weatherIcon = `https://openweathermap.org/img/wn/${data.weather[0].icon}.png`;  // Get weather icon URL

    // Get the current time and date
    const formattedTime = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

    // Update the card's inner HTML with weather info
    card.innerHTML = `
      <h4>${cityName}</h4>
      <span>${formattedTime}</span>
      <span>${new Date().toLocaleDateString()}</span>
      <span>${temperature}</span>
      <img src="${weatherIcon}" alt="Weather Icon" class="weather-icon">
      <button class="remove-btn">Remove</button>
    `;

    // Add event listener to the "Remove" button
    const removeButton = card.querySelector('.remove-btn');
    removeButton.addEventListener('click', async () => {
      resetCardToAddButton(card);  // Reset card to "Add" button state
      await removeLocation(city);  // Remove location from backend
    });
  }

  // Function to reset the card to the "Add" button state
  function resetCardToAddButton(card) {
    card.innerHTML = `<button class="add-btn"></button>`;  // Add "Add" button
    const addButton = card.querySelector('.add-btn');
    addButton.addEventListener('click', async () => {
      const city = prompt('Enter city name:');  // Prompt user for a city
      if (city) {
        await addLocation(city);  // Add location to backend
        getWeather(city, card);  // Fetch and display weather for the new city
      }
    });

  // Add a location to the backend
  async function addLocation(city) {
    try {
      // Send a POST request to add the city
      const response = await fetch('http://localhost:5000/dashboard/locations', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ city }),
      });
      if (!response.ok) throw new Error('Failed to save location');  // Error if adding fails
    } catch (error) {
      console.error('Error saving location:', error);  // Log error
    }
}
  }});