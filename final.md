# Weather App Final Review 

This markdown file contains the final review of the jnst project.

#### Project Members
 - Jan Suratos
 - Tawana Ndlovu
 - Syed Saad Ali
 - Ashish Nayak

## Table of Contents

- [1 - General Requirements](#General-Requirements)
- [Requirements](#requirements)
- [Proto Personas](#proto-personas)
- [Use Cases](#use-cases)
- [Setup](#setup)
- [License](#license)

---

## 1 - General Requirements
  ### 1.1 - Project Overview
  We developed a **Weather Forecast Application** that provides real-time weather updates and a 5-day forecast for a user-selected location. Below is an overview of the features and their state:  


#### Features Overview
- **User Account Management**:  
  - Users can create accounts, log in, and access their personalized dashboards.  
  - **Status**: Fully implemented and functional.
- **Location Search**:  
  - Users can search for weather information by city name.  
  - **Status**: Fully implemented and functional.
- **Current Weather Display**:  
  - Displays temperature, weather conditions, and an icon representing the current weather.  
  - **Status**: Fully implemented and functional.
- **5-Day Weather Forecast**:  
  - Displays basic forecast information for the next five days.  
  - **Status**: Fully implemented and functional.
- **Dashboard Customization**:  
  - Users can personalize their dashboards by adding/removing widgets and saving favorite locations.  
  - **Status**: Fully implemented and functional.
- **Sharing Dashboards**:  
  - Users can share their dashboards with others.  
  - **Status**: Not implemented (saving functionality is incomplete).

### 1.2 Initial Requirements: Delivered vs. Missing
| **Requirement**                               | **Status**           |
|-----------------------------------------------|----------------------|
| User account creation and login               | Delivered           |
| Location-based weather search                 | Delivered           |
| Display of current weather with icon          | Delivered           |
| 5-day weather forecast display                | Delivered           |
| Dashboard sharing                       | Partially delivered |
| Dashboard customization                              | Delivered           |

- **Summary**: We delivered most of the requirements except for the dashboard sharing functionality, we did not get to start developing. Our initial requirements captured the necessary details to guide the project effectively.

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
   - Stores user data, dashboard configurations, and weather preferences.  
4. **External Weather API Integration**:  
   - **API**: OpenWeather API  
   - Provides real-time weather and forecast data.  

#### Design Patterns
- **Adapter Pattern**:  
  - Used to interface with the OpenWeather API for consistent data formatting.  
- **Singleton Pattern**:  
  - Ensures a single instance of the API client for optimal performance.  
- **Facade Pattern**:  
  - Simplifies the interface for fetching and displaying weather data to the front-end.  

### 1.4 Re-use Achieved
We implemented modular and reusable components, such as:  
- A centralized API client for weather data fetching.  
- Reusable UI components for weather widgets and forecasts.  
- [ PLEASE HELP HERE]

This approach facilitated clean code, reduced redundancy, and allowed for easier debugging.

### 1.5 - Remaining Backlog Tasks
- **Dashboard Sharing Functionality**: Finalize and integrate the feature. [TENTATIVE]
- **Dark Mode**: Personalize background to a dark theme.
- **Temperature Unit Conversion**: Implement functionality of converting between Celsius to fahrenheit

## Weather Forecast Application Summary
The application meets its primary goals, providing a robust and intuitive platform for users to access weather information and forecasts. While a minor feature remains incomplete, the core functionality is operational and demonstrates the potential for real-world use.

---

## 2 - CI/CD Report

### 2.1 Testing Strategies
#### Implemented Strategies
- **Test Plan**:  
  We developed a test plan addressing both functional and non-functional requirements.  
- **Testing Tools and Frameworks**:  
  - **Pytest**: Used extensively to test:  
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

