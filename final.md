# Weather App Final Review 
## Milestone #7 - Final Delivery

This markdown file contains the final review of the jnst project.

#### Project Members
 - Jan Suratos
 - Tawana Ndlovu
 - Syed Saad Ali
 - Ashish Nayak

## Table of Contents
- [Video Walkthrough](#video-walkthrough)
- [1 - General Requirements](#General-Requirements)
- [Requirements](#requirements)
- [Proto Personas](#proto-personas)
- [Use Cases](#use-cases)
- [Setup](#setup)
- [License](#license)

---
## Video Walkthrough 
```https://youtu.be/oklFDtifxXI```

---

## 1 - General Requirements
  ### 1.1 - Project Overview
  Our team developed a web-based **Weather Forecast Application** that provides user with real-time weather data and a 5-day forecast for the user-selected location. Below is an overview of the features and their state:  


#### Features Overview
- **User Account Management**:  
  - Users can create accounts, log in/out, and access their personalized dashboards.  
  - **Status**: Fully implemented and functional.
- **Location Search**:  
  - Users can search for weather information by city name and receive current data. 
  - **Status**: Fully implemented and functional.
- **Current Weather Display**:  
  - Displays temperature, weather conditions, and an icon representing the current weather.  
  - **Status**: Fully implemented and functional.
  - **Temperature Unit Conversion**:  
    - Users can switch between Celsius and Fahrenheit for temperature display.  
    - **Status**: Fully implemented and functional.
- **5-Day Weather Forecast**:  
  - Displays basic forecast information for the next five days.  
  - **Status**: Fully implemented and functional.
- **Dashboard Customization**:  
  - Users can personalize their dashboards by adding/removing widgets and saving favorite locations.  
  - **Status**: Partially implemented and functional. User's are currently unable to toggle dark mode customization.
- **Sharing Dashboards**:  
  - Users can share their dashboards with others.  
  - **Status**: Fully implemented and functional.

### 1.2 Initial Requirements: Delivered vs. Missing
| **Requirement**                               | **Status**           |
|-----------------------------------------------|----------------------|
| User account creation and login               | Delivered           |
| Location-based weather search                 | Delivered           |
| Display of current weather with icon          | Delivered           |
| Temperature unit conversion                    | Delivered           |
| 5-day weather forecast display                | Delivered           |
| Dashboard sharing                       | Delivered |
| Dashboard customization                              | Partially Delivered           |


 **Summary**: We delivered most of the requirements except for customization for light/dark mode, we did not get to start developing. As well, the dashboard page does not have c/f toggling functionality. We believe our initial requirements captured the necessary details to guide the project effectively.

### 1.3 - System Architecture and Key Components
#### Architecture Overview
The system follows a **Client-Server Architecture** with the following components:  
1. **Front-End**:  
   - **Technology**: Webpages (HTML files) JavaScript (main.js, register.js, dashboard.js, etc)  
   - Displays weather data and supports user interaction.  
2. **Back-End Server**:  
   - **Technology**: Python Flask (app.py)  
   - Handles API requests, user authentication, and database interactions.  
3. **Database**:  
   - **Technology**: MySQL  
   - Stores user data, dashboard configurations, and weather preferences. Launched and handled through docker.
4. **External Weather API Integration**:  
   - **API**: OpenWeatherMap API  
   - Provides real-time weather and forecast data.  

#### Design Patterns
- **Adapter Pattern**:  
  - Used to interface with the OpenWeather API for consistent data formatting. 
  - The python database manger file acts as an adapter as it bridges the gap between app.py and the mysql database, which on their own are incompatible.
- **Singleton Pattern**:  
  - Ensures a single instance of the API client for optimal performance.  
  - In the python database manager, a singleton pattern was utilized for creation of new queries. If the query already existed in the database, it would return the primary key for the attribute rather than creating a new one. (For example, when adding locations, if the location already existed it would return the id.)
- **Facade Pattern**:  
  - Simplifies the interface for fetching and displaying weather data to the front-end.  
  - The weather_app_DB.py also utilizes facade pattern as it hides the complexity of interacting with MySql from app.py and works as a black box in the perspective of app.py.

### 1.4 Re-use Achieved
We implemented modular and reusable components, such as:  
- A centralized API client for weather data fetching.  
- Reusable UI components for weather widgets and forecasts.  
- Reusable python functions for fetching weather data and wrapping as an object. 
- Reused javascript code for similar interfaces such as the dashboard page and shared_dashboard page.
- The alert function on the front end was one method that was reused several times with the message varying.

This approach facilitated clean code, reduced redundancy, and allowed for easier debugging.

### 1.5 - Remaining Backlog Tasks
- **Dark Mode**: Personalize background to a dark theme.
- **Temperature Unit Conversion**: Implement functionality of converting between Celsius to fahrenheit in the dashboards.
- **Sharing Page blocked to logged out users**: Implement a restriction to prevent users from accessing a shared dashboard unless they are logged in.
- **BugFixes**: 
   - The dashboard cards do not hold their position and will move on their own. This may be due to the way the db queries for saved locations.
   - Edge cases: There are some missed edge cases found that were not considered such as certain page routes.

## Weather Forecast Application Summary
The application meets its primary goals, providing a robust and intuitive platform for users to access weather information and forecasts. While some minor feature remains incomplete, the core functionality is operational and demonstrates the potential for real-world use.

---

## 2 - CI/CD Report

### 2.1 Testing Strategies
#### Implemented Strategies
- **Test Plan**:  
  We developed a test plan addressing both functional and non-functional requirements.  
- **Testing Tools and Frameworks**:  
  - **Pytest**: Used extensively to test
    - **Functional Tests**: User requirements, weather data retrival, dashboard customization, CI/CD pipeline database testing.  
    - **Non Functional Tests**: Security, useability reliablity, performace, maintainability. 
    - **Component Testing**: Database, server, and UI were tested independently to isolate issues.
- **Automation**:  
  - All tests were manually initiated using Pytest. No automated CI tools (e.g., Jenkins or GitHub Actions) were employed to run tests automatically.  

#### Reflection and Future Improvements
- **Effectiveness**:  
  The current approach effectively identified and resolved bugs. However, manually triggering tests was time-consuming.  
- **Future Changes**:  
  - Introduce **automated testing tools** (e.g., GitHub Actions) to streamline testing and integrate it into the CI pipeline.  
  - Expand the test suite to include performance tests and load testing.

---

### 2.2 Branching Workflow
#### Workflow Implementation
- **Branch Organization**:  
  Separate branches were created for functional and non-functional tests, ensuring clarity and minimizing conflicts.  
- **Code Review Process**:  
  - A ruleset enforced mandatory reviews:  
    - At least **two team members** had to review and approve a test branch before merging it into the `development` branch.  
    - Direct merges to the `main` branch were blocked to maintain code quality.  
- **Success**:  
  This workflow was highly effective in ensuring code integrity and avoiding untested code in the main branch.

---

### 2.3 Deployment

- **Docker Implementation**:  
  The project is fully Dockerized, with a **Dockerfile** and services defined for deployment. Key configurations include:  
  - A MySQL database service with defined environment variables for database setup (e.g., user credentials and database initialization).  
  - Volume mapping for persistent storage and automatic database initialization using `weatherAppDB.sql`.  
- **Deployment Steps**:  
  1. Build and start the Docker containers using the provided Dockerfile and `docker-compose` configuration.  
  2. The application services will automatically connect to the MySQL container.  
  3. Use GitHub Pages for front-end deployment.  

#### Deployment Testing
The Dockerized environment was tested and is functional, ensuring smooth deployment on any compatible system.  

#### Future Enhancements
To enhance deployment reliability, consider integrating **Continuous Deployment tools** like Docker Hub or Kubernetes for scaling and automated updates.

Reflections (Comment on the following items as a team):

How did your project management work for the team?  What was the hardest thing and what would you do the same/differently the next time you plan to complete a project like this? 

* We needed more consistent development and communication. The system architecture was mildly changed as we started developing so we could have planned that better.

Do you feel that your initial requirements were sufficiently detailed for this project?  Which requirements did you miss or overlook?

* The requirements were a guiding light in helping us imagine what the final product looked like. This helped us in our planning process ultimately leading to coding with less confusion.

What did you miss in your initial planning for the project (beyond just the requirements)?

What process did you use (ie Scrum, Kanabn..), how was it managed, and what was observed? 

As a team, did you encounter issues with different team members developing with different IDEs?  In the future, would the team change anything in regard to the uniformity of development environments?

If you were to estimate the efforts required for this project again, what would you consider?  (Really I am asking the team to reflect on the difference between what you thought it would take to complete the project vs what it actually took to deliver it).   

What did your team do that you feel is unique or something that the team is especially proud of (was there a big learning moment that the team had in terms of gaining knowledge of a new concept/process that was implemented).
How did AI impact the development of the project? 