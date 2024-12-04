document.addEventListener('DOMContentLoaded', () => {
  const API_KEY = 'b5958d9b3908799da10532d190c26c36'; // Replace with your OpenWeather API key
  const WEATHER_URL = 'https://api.openweathermap.org/data/2.5/weather';

  const addButtons = document.querySelectorAll('.add-btn');
  const dashboardCards = document.querySelectorAll('.dashboard-card');

  // Function to fetch and populate weather data for the city
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

   // Function to get the first available (empty) card to populate with weather data
   function getAvailableCard() {
    return Array.from(dashboardCards).find(card => !card.querySelector('h4'));
}

 // Load saved locations from the database (via Flask API)
 async function loadSavedLocations() {
    try {
        const response = await fetch('/dashboards');
        if (response.ok) {
            const locations = await response.json(); // Expect an array of cities
            locations.forEach(city => {
                const card = getAvailableCard();
                if (card) {
                    getWeather(city, card);
                }
            });
        } else {
            console.error('Failed to load saved locations');
        }
    } catch (error) {
        console.error('Error loading locations:', error);
    }
}

// Add a city to the saved locations (via Flask API)
async function addLocation(city) {
    try {
        const response = await fetch('/add_location', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ city }),
        });
        if (!response.ok) {
            const errorData = await response.json();
            console.error('Error adding location:', errorData);
            alert(`Failed to add ${city}: ${errorData.message}`);
        }
    } catch (error) {
        console.error('Error adding location:', error);
        alert('Failed to add the location.');
    }
}

// Remove a city from the saved locations (via Flask API)
async function removeLocation(city) {
    try {
        const response = await fetch('/remove_location', {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ city }),
        });
        if (!response.ok) {
            const errorData = await response.json();
            console.error('Error removing location:', errorData);
            alert(`Failed to remove ${city}: ${errorData.message}`);
        }
    } catch (error) {
        console.error('Error removing location:', error);
        alert('Failed to remove the location.');
    }
}

// Initial loading of saved locations
loadSavedLocations();

});
