document.addEventListener('DOMContentLoaded', () => {
    // Select DOM elements
    const searchBar = document.querySelector('.search-bar');
    const currentLocationBtn = document.querySelector('.current-location-btn');
    const cityName = document.getElementById('cityName');
    const time = document.getElementById('time');
    const date = document.getElementById('date');
    const temperature = document.getElementById('temperature');
    const feelsLike = document.getElementById('feelsLike');
    const humidity = document.getElementById('humidity');
    const windSpeed = document.getElementById('windSpeed');
    const pressure = document.getElementById('pressure');
    const uvIndex = document.getElementById('uvIndex');
    const sunrise = document.getElementById('sunrise');
    const sunset = document.getElementById('sunset');

    // OpenWeather API details
    const API_KEY = 'b5958d9b3908799da10532d190c26c36';  // Replace with your actual OpenWeather API key
    const BASE_URL = 'https://api.openweathermap.org/data/2.5/weather';

    // Fetch weather data based on city name
    async function getWeather(city) {
        try {
            const response = await fetch(`${BASE_URL}?q=${city}&appid=${API_KEY}&units=metric`);
            const data = await response.json();

            // If the city is not found or the response is not successful
            if (data.cod !== 200) {
                alert('City not found!');
                return;
            }

            // Update UI with weather data
            cityName.textContent = `${data.name}, ${data.sys.country}`;
            temperature.textContent = `${data.main.temp}°C`;
            feelsLike.textContent = `Feels like: ${data.main.feels_like}°C`;
            humidity.textContent = `Humidity: ${data.main.humidity}%`;
            windSpeed.textContent = `Wind Speed: ${data.wind.speed} m/s`;
            pressure.textContent = `Pressure: ${data.main.pressure} hPa`;
            sunrise.textContent = `Sunrise: ${new Date(data.sys.sunrise * 1000).toLocaleTimeString()}`;
            sunset.textContent = `Sunset: ${new Date(data.sys.sunset * 1000).toLocaleTimeString()}`;

            // Update time and date (local time)
            const currentTime = new Date();
            time.textContent = currentTime.toLocaleTimeString();
            date.textContent = currentTime.toLocaleDateString();

        } catch (error) {
            console.error('Error fetching weather data:', error);
            alert('Failed to fetch weather data.');
        }
    }

    // Event listener for the search bar (on enter key press)
    searchBar.addEventListener('keydown', (event) => {
        if (event.key === 'Enter') {
            const city = searchBar.value.trim();
            if (city) {
                getWeather(city);
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
                    const response = await fetch(`${BASE_URL}?lat=${lat}&lon=${lon}&appid=${API_KEY}&units=metric`);
                    const data = await response.json();
                    if (data.cod !== 200) {
                        alert('Unable to fetch weather for your current location');
                        return;
                    }
                    // Update the UI with current location weather data
                    getWeatherFromCoordinates(data);
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

    // Function to update UI from coordinates (current location)
    function getWeatherFromCoordinates(data) {
        cityName.textContent = `${data.name}, ${data.sys.country}`;
        temperature.textContent = `${data.main.temp}°C`;
        feelsLike.textContent = `Feels like: ${data.main.feels_like}°C`;
        humidity.textContent = `Humidity: ${data.main.humidity}%`;
        windSpeed.textContent = `Wind Speed: ${data.wind.speed} m/s`;
        pressure.textContent = `Pressure: ${data.main.pressure} hPa`;
        sunrise.textContent = `Sunrise: ${new Date(data.sys.sunrise * 1000).toLocaleTimeString()}`;
        sunset.textContent = `Sunset: ${new Date(data.sys.sunset * 1000).toLocaleTimeString()}`;

        // Update time and date (local time)
        const currentTime = new Date();
        time.textContent = currentTime.toLocaleTimeString();
        date.textContent = currentTime.toLocaleDateString();
    }
});
