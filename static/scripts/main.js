document.addEventListener('DOMContentLoaded', () => {
    // Check if the database connection failed and display an alert
    if (typeof dbConnectionFailed !== 'undefined' && dbConnectionFailed) {
        alert('Error: Failed to connect to the database.\nIs Database Server Running?');
    }

    function getQueryParameter(name) { //for code reuse
        const urlParams = new URLSearchParams(window.location.search);
        return urlParams.get(name);
    }

    // Check for success message in URL parameters and display an alert
    const alertMSG = getQueryParameter('alert_msg');
    if (alertMSG) {
        alert(alertMSG);
    }


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

    const darkModeSwitch = document.getElementById('darkModeSwitch');
    let darkModeEnabled = false;
    darkModeSwitch.addEventListener('change', function () {
        darkModeEnabled = !darkModeEnabled;
        console.log('Dark mode toggle clicked'); // This ensures the event is firing
        console.log(darkModeEnabled)

        if(darkModeEnabled) {
            enableDarkMode();
        } else {
            disableDarkMode();
        }

        
    });
  

    // OpenWeather API details
    const API_KEY = 'b5958d9b3908799da10532d190c26c36'; // Replace with your actual OpenWeather API key
    const WEATHER_URL = 'https://api.openweathermap.org/data/2.5/weather';
    const FORECAST_URL = 'https://api.openweathermap.org/data/2.5/forecast';


    // Function to convert temperatures in the list
    function convertTemperatures() {
        const unitSymbol = unit === 'metric' ? '°C' : '°F';
        const weatherItems = document.querySelectorAll('.weather-list-item');
    
        weatherItems.forEach((item) => {
            const temperatureElement = item.querySelector('.temperature');
            const temperatureText = temperatureElement.textContent;
            const currentTemp = parseFloat(temperatureText.replace(/[^\d.-]/g, '')); // Extract number
            
            if (!isNaN(currentTemp)) {
                const newTemp = unit === 'metric'
                    ? ((currentTemp - 32) * 5) / 9 // Convert Fahrenheit to Celsius
                    : (currentTemp * 9) / 5 + 32; // Convert Celsius to Fahrenheit
                temperatureElement.textContent = `${Math.round(newTemp)}${unitSymbol}`;
            }
        });
    }
    
    
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
        const today = new Date();

        const options = { weekday: 'long', day: '2-digit', month: 'short' };
        const formattedDate = new Intl.DateTimeFormat('en-US', options).format(today);

        date.innerText = formattedDate;
        

    }
    
    
    
    


    // Other weather-related functions
    toggleUnitBtn.addEventListener('click', () => {
        unit = unit === 'metric' ? 'imperial' : 'metric'; // Switch unit
        toggleUnitBtn.textContent = unit === 'metric' ? '°C / °F' : '°F / °C'; // Update button text
    
        const city = document.getElementById('cityName')?.textContent?.split(',')[0]; // Extract city name
        if (city) {
            getWeather(city);
            getFiveDayForecast(city);
        }
    
        // Update the temperatures in the list dynamically
        convertTemperatures();
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
    
    // setInterval(() => {
    // if (currentCityData) {
        // updateTime(currentCityData.timezone); // Pass the city's timezone
    // }
// }, 1000);


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
                <span>${minTemp}${unitSymbol} to ${maxTemp}${unitSymbol}</span>
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
                window.history.replaceState(null, '', '/index'); //clear url after updating
            } else {
                alert('Please enter a city!');
            }
        }
    });

    // Event listener for the welcome button
    const welcomeBtn = document.querySelector('.welcome-btn');
    if (welcomeBtn) {
        const originalText = welcomeBtn.textContent; // Capture the original text content
        
        welcomeBtn.addEventListener('mouseover', () => {
            welcomeBtn.textContent = 'Logout?';
        });
        welcomeBtn.addEventListener('mouseout', () => {
            welcomeBtn.textContent = originalText;
        });

        welcomeBtn.addEventListener('click', () => {
            // Your desired function here
            window.location.href = '/logout';

        });
    }   

    // Event listener for login button
    const loginBtn = document.querySelector('.login-btn');
    if(loginBtn) {
        loginBtn.addEventListener('click', () => {
            window.location.href = '/login';
        });
    }

    // Event listener for view dashboards button
    const viewDashboardsBtn = document.querySelector('.view-dashboards-btn');
    if(viewDashboardsBtn) {
        viewDashboardsBtn.addEventListener('click', () => {
            window.location.href = '/dashboards';
        });
    }

    //If city location is given in url ... if /weather routed
    const location = getQueryParameter('location');
    if (location) {
        getWeather(location);
        getFiveDayForecast(location);
    }

    // Event listener for view dashboards button non-logged-in-users
    const viewDashboardsBtnNotLoggedIn = document.querySelector('.view-dashboards-btn-not-logged-in');
    if(viewDashboardsBtnNotLoggedIn) {
        viewDashboardsBtnNotLoggedIn.addEventListener('click', () => {
            const userConfirmed = confirm('You need to login first. Do you want to login now?');
            if (userConfirmed) {
                window.location.href = '/login';
            }
        });
    }

// Event listener for the current location button
currentLocationBtn.addEventListener('click', () => {
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
                updateTime(data.timezone); // Update the time with the timezone of the current location

                const forecastResponse = await fetch(`${FORECAST_URL}?lat=${lat}&lon=${lon}&appid=${API_KEY}&units=${unit}`);
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
    document.addEventListener('DOMContentLoaded', () => {
        // Automatically prompt for the user's location when the page loads
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
                    updateTime(data.timezone); // Update time with the timezone of the current location
    
                    const forecastResponse = await fetch(`${FORECAST_URL}?lat=${lat}&lon=${lon}&appid=${API_KEY}&units=${unit}`);
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


    console.log("main.js loaded");
});

function enableDarkMode() {
    document.documentElement.style.setProperty('--white', '#ffffff');
    document.documentElement.style.setProperty('--lighterblue', '#005abe');
    document.documentElement.style.setProperty('--lightblue', '#001e48');
    document.documentElement.style.setProperty('--darkblue', '#002c63');
    document.documentElement.style.setProperty('--background', '#000516');
    document.documentElement.style.setProperty('----dark-to-light-txt', '#ffffff');
}

function disableDarkMode() {
    document.documentElement.style.setProperty('--white', '#ffffff');
    document.documentElement.style.setProperty('--lighterblue', '#e1f5fe');
    document.documentElement.style.setProperty('--lightblue', '#81d4fa');
    document.documentElement.style.setProperty('--darkblue', '#03a9f4');
    document.documentElement.style.setProperty('--background', '#ffffff');
    document.documentElement.style.setProperty('----dark-to-light-txt', '#000000');
}
