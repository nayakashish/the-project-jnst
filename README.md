# Weather App

This project is a web-based weather application that provides users with real-time weather data, location-specific forecasts, and a customizable dashboard. Users can view, share, and customize their weather data and dashboards, all powered by the OpenWeather API.

## Table of Contents

- [Overview](#overview)
- [Requirements](#requirements)
- [Use Cases](#use-cases)
- [Setup](#setup)
- [License](#license)

---

## Overview

Project Description & Scope -  
 This application will be a user-focused weather platform offering real-time weather updates and a 5-day forecast for selected locations. The platform will allow users to create accounts, allowing them to access, personalize, and share their dashboards with other users. The system will support search functionality, enabling users to retrieve weather details by city name. For each selected location, it will display current temperature, weather conditions, and an appropriate weather icon, with user-selectable display formats for personalization. Users will also benefit from quick access to saved favorite locations on their dashboards and can share this information with others once they have created an account. In addition, the application will maintain a simple and intuitive interface, ensuring accessibility across multiple web screen sizes and browser environments like Chrome and Safari. It will adhere to data privacy standards, disclosing only necessary user information. Users can expect seamless login and logout functionality to protect their accounts. The platform will also notify users of any errors in retrieving weather data, managing accounts, or sharing features, making the experience smooth and user-friendly.



---

## Requirements

Requirements - 

Functional:
Users must be able to create, edit, and delete accounts.
Users will be able to log in to access their personal dashboard.
Users can personalize their dashboard (e.g., select favorite locations or adjust themes).
Logged-in users will be able to save favorite locations for quick access on the dashboard.
Logged-in users will be able to share their dashboard with other users.
The system will allow users to search for weather information by city name.
The system will display current weather for the selected location, including temperature, weather conditions (e.g., cloudy, rainy), and an icon representing the current weather condition.
The system will display a 5-day weather forecast, showing daily temperatures, weather conditions.
Users will be able to choose how to display temperature (Celsius/Fahrenheit) and weather formats (e.g., detailed/summary view).
Shared dashboards will be view-only for other users.
The system will notify the user of any errors in retrieving weather, account management, or sharing, if they occur.

Non-Functional:
The user interface should be simple and intuitive, allowing users to quickly access weather information.
The system will support multiple active users simultaneously. 
The system must not disclose any personal information about users apart from their name and shared dashboards to users of the system.
The app must work on common browsers like Chrome and Safari.
Basic login and logout functionality should be implemented to protect accounts.
The application must adapt to various screen sizes (web), so that it displays content properly depending on how large the browser screen size is.


---

## Proto Personas
![Alt text](Images\Persona1.png "Persona1")
![Alt text](Images\Persona2.png "Persona2")
![Alt text](Images\Persona3.png "Persona3")
![Alt text](Images\Persona4.png "Persona4")

## Use Cases

![Alt text](Images\useCaseDiagram.png "UseCaseDiagram")

### OpenWeatherAPI
**Actor**: OpenWeatherAPI (Secondary)  
**Description**: The OpenWeatherAPI receives requests from the application to provide weather data for viewing by users.

---

### Use Case 1. View Weather
**Primary Actor**: User  
**Description**: Users view the weather for a default location upon opening the app.  
**Pre-condition**: Successful API connection.  
**Post-condition**: Accurate weather data is displayed, including forecast and summary.

**Main Scenario**:
1. User opens the application.
2. Application requests data from the API.
3. API provides weather data.
4. Application displays the data.

**Extension**:
- 1a. Process completes within seconds.
- 2a. API connection fails.
    - 2a1. Application notifies the user of an error.

---

### Use Case 2. Set Location
**Primary Actor**: User  
**Description**: Users select a location to view weather data.  
**Pre-condition**: User has a location in mind.  
**Post-condition**: Application refreshes with accurate data for the selected location.

**Main Scenario**:
1. User inputs a location in the search bar.
2. System requests data for the location from OpenWeatherAPI.
3. API responds with weather data for the location.
4. System updates displayed information.

**Extension**:
- 1a. User misspells location.
    - 1a1. System notifies of invalid input.
- 1b. User selects location from dashboard if logged in.
- 2a. API request fails.
    - 2a1. System notifies of an error.

---

### Use Case 3. Login
**Primary Actor**: User  
**Description**: User logs into the application.  
**Pre-condition**: User has an account.  
**Post-condition**: User is logged in and sees saved dashboard.

**Main Scenario**:
1. System prompts login details.
2. User inputs username and password.
3. System validates credentials.
4. System logs user in and displays saved dashboard.

**Extension**:
- 2a. User does not have an account.
    - 2a1. System prompts to create an account.
- 2b. Invalid username or password.
    - 2b1. System notifies of error.

---

### Use Case 4. View Dashboard
**Primary Actor**: User  
**Description**: User views active dashboard.  
**Pre-condition**: User is logged in.  
**Post-condition**: Correct dashboard displayed.

**Main Scenario**:
1. System starts with a blank dashboard.
2. System verifies the user.
3. Dashboard is updated to display saved locations.

**Extension**:
- 2a. User not logged in.
    - 2a1. System prompts for login.
    - 2a2. Dashboard remains blank until login.
- 3a. No saved dashboard found.
    - 3a1. System displays default dashboard.

---

### Use Case 5. View Shared Dashboard
**Primary Actor**: User  
**Description**: User views a shared dashboard.  
**Pre-condition**: User is authenticated.  
**Post-condition**: Shared dashboard displayed in view-only mode.

**Main Scenario**:
1. User requests to view another user’s shared dashboard.
2. System authenticates the user.
3. System displays shared dashboard.

**Extension**:
- 2a. User not logged in.
    - 2a1. System prompts for login.

---

### Use Case 6. Add Locations to Dashboard
**Primary Actor**: User  
**Description**: User adds a selected location to their dashboard.  
**Pre-condition**: User is logged in with a selected location.  
**Post-condition**: Location added to dashboard and page updated.

**Main Scenario**:
1. User favorites the current location.
2. System authenticates the user.
3. System adds location to the dashboard.

**Extension**:
- 2a. User not logged in.
    - 2a1. System prompts for login.
- 3a. Location already favorited.
    - 3a1. System notifies location is already saved.

---

### Use Case 7. Share Dashboard
**Primary Actor**: User  
**Description**: User shares their dashboard.  
**Pre-condition**: User is logged in.  
**Post-condition**: Application generates a shareable link to the dashboard.

**Main Scenario**:
1. User requests to share dashboard.
2. System authenticates the user.
3. System generates and shares a link to the dashboard.

**Extension**:
- 2a. User not logged in.
    - 2a1. System prompts for login.

---

### Use Case 8. Customize Dashboard
**Primary Actor**: User  
**Description**: User customizes their dashboard layout.  
**Pre-condition**: User is logged in.  
**Post-condition**: Dashboard saved with custom layout.

**Main Scenario**:
1. User edits dashboard.
2. System authenticates user.
3. User rearranges locations as desired.
4. System saves changes.

**Extension**:
- 2a. User not logged in.
    - 2a1. System prompts for login.

---

### Use Case 9. Fetch Weather Data
**Primary Actor**: OpenWeather API  
**Description**: Requests weather data from API.  
**Pre-condition**: System has an authenticated API key.  
**Post-condition**: System receives weather data from API.

**Main Scenario**:
1. System requests data from API.
2. API responds with weather data.
3. System displays data to user.

**Extension**:
- 1a. API request fails.
    - 1a1. System notifies user of an error.

---


