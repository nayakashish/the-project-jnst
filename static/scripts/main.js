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
    const toggleUnitBtn = document.getElementById('toggleUnit');

    // OpenWeather API details
    const API_KEY = 'b5958d9b3908799da10532d190c26c36'; // Replace with your actual OpenWeather API key
    const WEATHER_URL = 'https://api.openweathermap.org/data/2.5/weather';
    const FORECAST_URL = 'https://api.openweathermap.org/data/2.5/forecast';

    // Default unit system (metric = Celsius)
    let unit = 'metric';

    // Function to update time
    function updateTime(timezone) {
        const now = new Date();
        
        // Convert the current time to the city's timezone
        const utcOffset = timezone * 1000;  // Convert to milliseconds
        const cityTime = new Date(now.getTime() + utcOffset);
        
        const hours = String(cityTime.getUTCHours()).padStart(2, '0'); // Format hours as 2 digits
        const minutes = String(cityTime.getUTCMinutes()).padStart(2, '0'); // Format minutes as 2 digits
        
        // Update the time element with the colon blinking
        time.innerHTML = `${hours}<span class="blinking">:</span>${minutes}`;
    }
    
    
    
    


    // Other weather-related functions
    toggleUnitBtn.addEventListener('click', () => {
        unit = unit === 'metric' ? 'imperial' : 'metric'; // Switch unit
        toggleUnitBtn.textContent = unit === 'metric' ? '°C / °F' : '°F / °C'; // Update button text

        const city = document.getElementById('cityName').textContent.split(',')[0]; // Extract city name
        if (city) {
            getWeather(city);
            getFiveDayForecast(city);
        }
    });

    async function getWeather(city) {
        try {
            const response = await fetch(`${WEATHER_URL}?q=${city}&appid=${API_KEY}&units=${unit}`);
            if (!response.ok) {
                const errorData = await response.json();
                console.error('Weather API Error:', errorData);
                alert(`Error fetching weather: ${errorData.message}`);
                return;
            }
            const data = await response.json();
            updateWeather(data);
    
            // Get the timezone from the weather data and update the time
            updateTime(data.timezone);
        } catch (error) {
            console.error('Error fetching weather data:', error);
            alert('Failed to fetch weather data.');
        }
    }
    
    setInterval(() => {
        if (currentCityData) {
            updateTime(currentCityData.timezone); // Pass the city's timezone
        }
    }, 1000);
    

    async function getFiveDayForecast(city) {
        try {
            const response = await fetch(`${FORECAST_URL}?q=${city}&appid=${API_KEY}&units=${unit}`);
            if (!response.ok) {
                const errorData = await response.json();
                console.error('Forecast API Error:', errorData);
                alert(`Error fetching forecast: ${errorData.message}`);
                return;
            }
            const forecastData = await response.json();
            updateHourlyForecast(forecastData.list.slice(0, 5));
            updateFiveDayForecast(forecastData.list);
        } catch (error) {
            console.error('Error fetching forecast data:', error);
            alert('Failed to fetch forecast data.');
        }
    }

    // Function to update weather UI
    function updateWeather(data) {
        const unitSymbol = unit === 'metric' ? '°C' : '°F';
        cityName.textContent = `${data.name}, ${data.sys.country}`;
        temperature.textContent = `${data.main.temp}${unitSymbol}`;
        feelsLike.textContent = `Feels like: ${data.main.feels_like}${unitSymbol}`;
        sunrise.textContent = `Sunrise: ${new Date(data.sys.sunrise * 1000).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}`;
        sunset.textContent = `Sunset: ${new Date(data.sys.sunset * 1000).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}`;
    }

    // Function to update hourly forecast
    function updateHourlyForecast(forecast) {
        const unitSymbol = unit === 'metric' ? '°C' : '°F';
        hourlyForecastContainer.innerHTML = '';
        const iconBaseURL = 'https://openweathermap.org/img/wn/';

        forecast.forEach((entry) => {
            const time = new Date(entry.dt * 1000).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
            const temp = `${Math.round(entry.main.temp)}${unitSymbol}`;
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

    // Function to update 5-day forecast UI
    function updateFiveDayForecast(forecast) {
        const unitSymbol = unit === 'metric' ? '°C' : '°F';
        const fiveDayForecastContainer = document.querySelector('.five-day-forecast .forecast-container');
        fiveDayForecastContainer.innerHTML = '';
        const iconBaseURL = 'https://openweathermap.org/img/wn/';

        const dailyForecast = {};
        forecast.forEach((entry) => {
            const date = new Date(entry.dt * 1000);
            const dayName = date.toLocaleDateString([], { weekday: 'short' });
            const temp = entry.main.temp;
            const icon = entry.weather[0].icon;

            const dayKey = date.toISOString().split('T')[0];
            if (!dailyForecast[dayKey]) {
                dailyForecast[dayKey] = { dayName, temps: [temp], icon };
            } else {
                dailyForecast[dayKey].temps.push(temp);
            }
        });

        Object.values(dailyForecast).slice(0, 5).forEach(({ dayName, temps, icon }) => {
            const minTemp = Math.round(Math.min(...temps));
            const maxTemp = Math.round(Math.max(...temps));

            const dayElement = document.createElement('div');
            dayElement.classList.add('forecast-day');
            dayElement.innerHTML = `
                <span>${dayName}</span>
                <span>${minTemp}${unitSymbol} - ${maxTemp}${unitSymbol}</span>
                <img src="${iconBaseURL}${icon}.png" alt="Weather Icon" class="weather-icon">
            `;
            fiveDayForecastContainer.appendChild(dayElement);
        });
    }

    // Event listener for the search bar
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

    // Event listener for the current location button
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

    // Check the user's location if geolocation is available
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(async (position) => {
            const lat = position.coords.latitude;
            const lon = position.coords.longitude;
            try {
                const response = await fetch(`${WEATHER_URL}?lat=${lat}&lon=${lon}&appid=${API_KEY}&units=${unit}`);
                if (!response.ok) {
                    const errorData = await response.json();
                    console.error('Location Weather API Error:', errorData);
                    alert(`Error fetching weather: ${errorData.message}`);
                    return;
                }
                const data = await response.json();
                updateWeather(data);
            } catch (error) {
                console.error('Error fetching weather:', error);
                alert('Failed to fetch weather data.');
            }
        });
    }
});


// Event listener for view dashboards button
const viewDashboardsBtn = document.querySelector('.view-dashboards-btn');
if(viewDashboardsBtn) {
    viewDashboardsBtn.addEventListener('click', () => {
        window.location.href = '/dashboards';
    });
}

