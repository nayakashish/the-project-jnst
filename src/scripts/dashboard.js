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
          const response = await fetch(`${WEATHER_URL}?q=${city}&appid=${API_KEY}&units=metric`);
          if (!response.ok) {
              const errorData = await response.json();
              console.error('Weather API Error:', errorData);
              alert(`Error fetching weather for ${city}: ${errorData.message}`);
              return;
          }
          const data = await response.json();
          updateCardWithWeather(data, card);
      } catch (error) {
          console.error('Error fetching weather data:', error);
          alert('Failed to fetch weather data.');
      }
  }

  // Function to update the card with weather data
  function updateCardWithWeather(data, card) {
      const cityName = data.name;
      const temperature = `${data.main.temp}°C`;
      const weatherIcon = `https://openweathermap.org/img/wn/${data.weather[0].icon}.png`;

      // Format time without seconds
      const formattedTime = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

      // Populate the card with the weather data
      card.innerHTML = `
          <h4>${cityName}</h4>
          <span>${formattedTime}</span>
          <span>${new Date().toLocaleDateString()}</span>
          <span>${temperature}</span>
          <img src="${weatherIcon}" alt="Weather Icon" class="weather-icon">
          <button class="remove-btn">Remove</button>
      `;

      // Add event listener for the "Remove" button
      const removeButton = card.querySelector('.remove-btn');
      removeButton.addEventListener('click', () => {
          // Reset the card to its original state with just the "Add" button
          resetCardToAddButton(card);
      });
  }

   // TODO: edit this method such that a commmand is passed to app.py to delete the weather card from the database,
  // (I think you can use a get or a post request here)

  // Function to reset the card to the "Add" button state
  function resetCardToAddButton(card) {
      card.innerHTML = `
          <button class="add-btn"></button>
      `;

      // Reattach event listener to the "Add" button after resetting
      const addButton = card.querySelector('.add-btn');
      addButton.addEventListener('click', () => {
          const city = prompt('Enter city name:');
          if (city) {
              getWeather(city, card);
          }
      });
  }

  // Event listener for the "Add" button in each card
  addButtons.forEach((button, index) => {
      button.addEventListener('click', () => {
          const city = prompt('Enter city name:');
          if (city) {
              getWeather(city, dashboardCards[index]);
          }
      });
  });
});
