document.addEventListener('DOMContentLoaded', () => {
    // Select DOM elements
    const searchBar = document.querySelector('.search-bar');
    const currentLocationBtn = document.querySelector('.current-location-btn');
    const cityName = document.getElementById('cityName');
    const time = document.getElementById('time');
    const date = document.getElementById('date');
    const temperature = document.getElementById('temperature');
    const feelsLike = document.getElementById('feelsLike');
    const sunrise = document.getElementById('sunrise');
    const sunset = document.getElementById('sunset');
    const hourlyForecastContainer = document.querySelector('.hourly-forecast');
    const fiveDayForecastContainer = document.querySelector('.five-day-forecast .forecast-container');

    // OpenWeather API details
    const API_KEY = 'b5958d9b3908799da10532d190c26c36'; // Replace with your actual OpenWeather API key
    const WEATHER_URL = 'https://api.openweathermap.org/data/2.5/weather';
    const FORECAST_URL = 'https://api.openweathermap.org/data/2.5/forecast';

    // Fetch weather data based on city name
    async function getWeather(city) {
        try {
            const response = await fetch(`${WEATHER_URL}?q=${city}&appid=${API_KEY}&units=metric`);
            if (!response.ok) {
                const errorData = await response.json();
                console.error('Weather API Error:', errorData);
                alert(`Error fetching weather: ${errorData.message}`);
                return;
            }
            const data = await response.json();
            updateWeather(data);
        } catch (error) {
            console.error('Error fetching weather data:', error);
            alert('Failed to fetch weather data.');
        }
    }

    // Fetch 5-day forecast
    async function getFiveDayForecast(city) {
        try {
            const response = await fetch(`${FORECAST_URL}?q=${city}&appid=${API_KEY}&units=metric`);
            if (!response.ok) {
                const errorData = await response.json();
                console.error('Forecast API Error:', errorData);
                alert(`Error fetching forecast: ${errorData.message}`);
                return;
            }
            const forecastData = await response.json();
            updateHourlyForecast(forecastData.list.slice(0, 5)); // Display next 5 hours
            updateFiveDayForecast(forecastData.list);
        } catch (error) {
            console.error('Error fetching forecast data:', error);
            alert('Failed to fetch forecast data.');
        }
    }

    // Update current weather UI
    function updateWeather(data) {
        cityName.textContent = `${data.name}, ${data.sys.country}`;
        temperature.textContent = `${data.main.temp}°C`;
        feelsLike.textContent = `Feels like: ${data.main.feels_like}°C`;
        sunrise.textContent = `Sunrise: ${new Date(data.sys.sunrise * 1000).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}`;
        sunset.textContent = `Sunset: ${new Date(data.sys.sunset * 1000).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}`;

        const utcNow = new Date().getTime() + new Date().getTimezoneOffset() * 60000;
        const cityLocalTime = new Date(utcNow + data.timezone * 1000);
        const hours = String(cityLocalTime.getHours()).padStart(2, '0');
        const minutes = String(cityLocalTime.getMinutes()).padStart(2, '0');
        time.innerHTML = `${hours}<span class="blinking">:</span>${minutes}`;
        date.textContent = cityLocalTime.toLocaleDateString();
    }

    // Update 5-hour forecast UI
    function updateHourlyForecast(forecast) {
        hourlyForecastContainer.innerHTML = ''; // Clear existing content
        const iconBaseURL = 'https://openweathermap.org/img/wn/';

        forecast.forEach((entry) => {
            const time = new Date(entry.dt * 1000).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
            const temp = `${Math.round(entry.main.temp)}°C`;
            const icon = entry.weather[0].icon;
            const description = entry.weather[0].description;

            const hourElement = document.createElement('div');
            hourElement.classList.add('hour');
            hourElement.innerHTML = `
                <span>${time}</span>
                <span>${temp}</span>
                <img src="${iconBaseURL}${icon}.png" alt="${description}" class="weather-icon">
            `;
            hourlyForecastContainer.appendChild(hourElement);
        });
    }

    // Update 5-day forecast UI
    function updateFiveDayForecast(forecast) {
        fiveDayForecastContainer.innerHTML = ''; // Clear existing content
        const iconBaseURL = 'https://openweathermap.org/img/wn/';

        // Group forecast data by day
        const dailyForecast = {};

        forecast.forEach((entry) => {
            const date = new Date(entry.dt * 1000);
            const dayName = date.toLocaleDateString([], { weekday: 'short' }); // Abbreviated day of the week
            const temp = entry.main.temp;
            const icon = entry.weather[0].icon;

            const dayKey = date.toISOString().split('T')[0]; // Group by unique date
            if (!dailyForecast[dayKey]) {
                dailyForecast[dayKey] = { dayName, temps: [temp], icon };
            } else {
                dailyForecast[dayKey].temps.push(temp);
            }
        });

        // Add the first 5 days to the forecast container
        Object.values(dailyForecast).slice(0, 5).forEach(({ dayName, temps, icon }) => {
            const minTemp = Math.round(Math.min(...temps));
            const maxTemp = Math.round(Math.max(...temps));

            // Create a forecast-day element
            const dayElement = document.createElement('div');
            dayElement.classList.add('forecast-day');
            dayElement.innerHTML = `
                <span>${dayName}</span>
                <span>${minTemp}°C - ${maxTemp}°C</span>
                <img src="${iconBaseURL}${icon}.png" alt="Weather Icon" class="weather-icon">
            `;
            fiveDayForecastContainer.appendChild(dayElement);
        });
    }

    // Event listener for the search bar (on enter key press)
    searchBar.addEventListener('keydown', (event) => {
        if (event.key === 'Enter') {
            const city = searchBar.value.trim();
            if (city) {
                getWeather(city);
                getFiveDayForecast(city);
            } else {
                alert('Please enter a city!');
            }
        }
    });

    // Event listener for current location button
    currentLocationBtn.addEventListener('click', () => {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(async (position) => {
                const lat = position.coords.latitude;
                const lon = position.coords.longitude;
                try {
                    const response = await fetch(`${WEATHER_URL}?lat=${lat}&lon=${lon}&appid=${API_KEY}&units=metric`);
                    if (!response.ok) {
                        const errorData = await response.json();
                        console.error('Location Weather API Error:', errorData);
                        alert(`Error fetching weather: ${errorData.message}`);
                        return;
                    }
                    const data = await response.json();
                    updateWeather(data);

                    const forecastResponse = await fetch(`${FORECAST_URL}?lat=${lat}&lon=${lon}&appid=${API_KEY}&units=metric`);
                    if (forecastResponse.ok) {
                        const forecastData = await forecastResponse.json();
                        updateHourlyForecast(forecastData.list.slice(0, 5));
                        updateFiveDayForecast(forecastData.list);
                    }
                } catch (error) {
                    console.error('Error fetching location weather:', error);
                    alert('Failed to fetch weather data for your location.');
                }
            }, () => {
                alert('Unable to access your location. Please enable location services.');
            });
        } else {
            alert('Geolocation is not supported by your browser.');
        }
    });
});



// LOGIN:
// main.js

// main.js


