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
    const fiveDayForecastContainer = document.querySelector('.five-day-forecast ul');

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

            // Update UI with weather data
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

            // Process the forecast data for the next 5 days (we will extract daily data)
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

        // Calculate UTC time
        const utcNow = new Date().getTime() + new Date().getTimezoneOffset() * 60000;

        // Adjust to city's local time
        const cityLocalTime = new Date(utcNow + data.timezone * 1000);

        // Extract hours and minutes
        const hours = String(cityLocalTime.getHours()).padStart(2, '0');
        const minutes = String(cityLocalTime.getMinutes()).padStart(2, '0');

        // Update time and date for the city's local timezone
        time.innerHTML = `${hours}<span class="blinking">:</span>${minutes}`; // Add blinking colon
        date.textContent = cityLocalTime.toLocaleDateString();
    }

    // Update 5-hour forecast UI
    function updateHourlyForecast(forecast) {
        hourlyForecastContainer.innerHTML = ''; // Clear existing content

        forecast.forEach((entry) => {
            const time = new Date(entry.dt * 1000).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
            const temp = `${Math.round(entry.main.temp)}°C`;
            const description = entry.weather[0].description;

            // Create a forecast hour element
            const hourElement = document.createElement('div');
            hourElement.classList.add('hour');
            hourElement.innerHTML = `
                <span>${time}</span>
                <span>${temp}</span>
                <span>${description}</span>
            `;

            // Append to the container
            hourlyForecastContainer.appendChild(hourElement);
        });
    }

    // Update 5-day forecast UI
    function updateFiveDayForecast(forecast) {
        fiveDayForecastContainer.innerHTML = ''; // Clear existing content

        // Process the forecast data to show the next 5 days
        const dailyForecast = [];

        forecast.forEach((entry) => {
            const date = new Date(entry.dt * 1000);
            const day = date.toLocaleDateString([], { weekday: 'short', month: 'short', day: 'numeric' });
            const temp = `${Math.round(entry.main.temp)}°C`;

            if (!dailyForecast[date.getDate()]) {
                dailyForecast[date.getDate()] = { date: day, temp: temp };
            }
        });

        // Now update the 5-day forecast list
        Object.values(dailyForecast).slice(0, 5).forEach((dayData) => {
            const dayElement = document.createElement('li');
            dayElement.textContent = `${dayData.temp} - ${dayData.date}`;
            fiveDayForecastContainer.appendChild(dayElement);
        });
    }

    // Event listener for the search bar (on enter key press)
    searchBar.addEventListener('keydown', (event) => {
        if (event.key === 'Enter') {
            const city = searchBar.value.trim();
            if (city) {
                getWeather(city);
                getFiveDayForecast(city); // Fetch 5-day forecast
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

                    // Fetch and display 5-day forecast for the current location
                    const forecastResponse = await fetch(`${FORECAST_URL}?lat=${lat}&lon=${lon}&appid=${API_KEY}&units=metric`);
                    if (forecastResponse.ok) {
                        const forecastData = await forecastResponse.json();
                        updateFiveDayForecast(forecastData.list);
                    }
                } catch (error) {
                    console.error('Error fetching location weather:', error);
                    alert('Failed to fetch weather data for your location.');
                }
            }, (error) => {
                alert('Unable to access your location. Please enable location services.');
            });
        } else {
            alert('Geolocation is not supported by your browser.');
        }
    });
});
