# Weather App Final Review 
![Weather App Screenshot](/Documentation/images/310index.jpg)

## Milestone #7 - Final Delivery

This markdown file contains the final review of the JNST project.

#### Project Members
 - Jan Suratos
 - Tawana Ndlovu
 - Syed Saad Ali
 - Ashish Nayak

## Table of Contents
- [Project Members](#project-members)
- [Video Walkthrough](#video-walkthrough)
- [General Review](#general-review)
  - [Project Overview](#11---project-overview)
  - [Initial Requirements: Delivered vs. Missing](#12---initial-requirements-delivered-vs-missing)
  - [System Architecture and Key Components](#13---system-architecture-and-key-components)
  - [Re-use Achieved](#14---re-use-achieved)
  - [Remaining Backlog Tasks](#15---remaining-backlog-tasks)
  - [Weather Application Summary](#16---weather--application-summary)
- [CI/CD Report](#2---cicd-report)
  - [Testing Strategies](#21-testing-strategies)
  - [Branching Workflow](#22-branching-workflow)
  - [Deployment](#23-deployment)
- [Reflections](#reflections)
---
## Video Walkthrough 
```https://youtu.be/oklFDtifxXI```

---

## General Review
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

### 1.2 - Initial Requirements: Delivered vs. Missing
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

### 1.4 - Re-use Achieved
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

### 1.6 - Weather  Application Summary

The application meets its primary goals, providing a robust and intuitive platform for users to access weather information and forecasts. While some minor features remain incomplete, the core functionality is operational and demonstrates the potential for real-world use.


## 2 - CI/CD Report

### 2.1 Testing Strategies
#### Implemented Strategies
- **Test Plan**:  
  We developed a [test plan](/Documentation/Models-TestPlan/TestPlanAtDesignStage.pdf) addressing both functional and non-functional requirements. Linked [here](/Documentation/Models-TestPlan/TestPlanAtProjectDueDate.pdf) is the test plan at project completion.
- **Testing Tools and Frameworks**:  
  - **Pytest**: Used extensively to test frontend and backend, including:
    - **Functional Tests**: User requirements, weather data retrival, dashboard customization, page contents, logged-in user vs logged-out user functionality.  
    - **Non Functional Tests**: Security, useability reliablity, performace, maintainability. 
    - **Component Testing**: Database, server, and UI were tested independently to isolate issues.
- **Automation**:  
  - Our project heavily utilized manual tests using Pytest and our Models-Test Plan. We would frequently run through the test plan spreadsheet to ensure new features passed requirements as well as verify previous features continued functioning. We did not utilize automated tests, such as GitHub Actions unfortunately, due to lack of time and the lack of priority our team placed on it. 

#### Reflection and Future Improvements
- **Effectiveness**:  
   - The current approach effectively identified and resolved bugs. However, manually triggering tests was time-consuming.  
   - The test spreadsheet visually showcases the features as they were implemented and prompted team members to test edge cases to validate previous functionality and ensure smooth integration.
- **Future Changes**:  
  - Introduce **automated testing tools** (e.g., GitHub Actions) to streamline testing and integrate it into the CI pipeline.  
  - Expand the test suite to include performance tests and load testing.

---

### 2.2 Branching Workflow
#### Workflow Implementation
- **Branch Organization**:  
   - Separate branches were created for functional and non-functional tests, ensuring clarity and minimizing conflicts.  
   - Branches were created and merged for each feature, which allowed us to asynchronously test and implement our features.
- **Code Review Process**:  
  - A ruleset enforced mandatory reviews:  
    - At least **two team members** had to review and approve a test branch before merging it into the `development` branch.  
    - Direct merges to the `main` branch were blocked to maintain code quality.  
- **Success**:  
  This workflow was highly effective in ensuring code integrity and avoiding untested code in the main branch.
  Having the mandatory reviews ensured that code got inspected visually and was pulled and tested on separate machines than the one developed on to ensure functionality.

---

### 2.3 Deployment

- **Docker Implementation**:  
  The project's database is fully Dockerized, with a Dockerfile and services defined for deployment. Along with the docker database, the front-end is launched through flask. Key configurations include:  
  - A MySQL database service with defined environment variables for database setup (e.g., user credentials and database initialization).  
  - Volume mapping for persistent storage and automatic database initialization using `weatherAppDB.sql`. 
  - Flask app for launching a frontend server for app.py and front-end.

- **Deployment Steps**:  
  1. Install dependencies and requirements.
  2. Build and start the Docker containers using the provided Dockerfile and `docker-compose` configuration.  
  3. The application services will automatically connect to the MySQL container.  
  4. Run app.py and route to the created localhost server.

#### Deployment Testing
 - The Dockerized environment was tested and is functional, ensuring smooth deployment on any compatible system.
 - The frontend content and backend app.py were tested throughout development using pytests and the models-test plan.  

#### Future Improvements in Deployment
 - To make deployment smoother, our team was presented with the idea of launching the flask server through the docker container itself, however due to our limited understanding of flask servers and lack of time, this feature could not be implemented.
 - To enhance deployment reliability, we could integrate Continuous Deployment tools like DockerHub, Kubernetes, GitHub pages, or some other cloud server for scaling and automated updates.

## Reflections:

#### How did your project management work for the team?  What was the hardest thing and what would you do the same/differently the next time you plan to complete a project like this? 

* We needed more consistent development and communication. The system architecture was mildly changed as we started developing so we could have planned that better.
* If we were to do the same project again, next time we would place more priority on communication and understanding of the requirements and final goal. As the features were developed by different team memebers, the description of how it worked and would connect with other components lacked.
* Placing more importance on the initial planning, documentation, and communication would have enabled us to implement the features more seamlessly as we would not have needed to confirm details with one another so frequently.

#### Do you feel that your initial requirements were sufficiently detailed for this project?  Which requirements did you miss or overlook?

* The requirements were a guiding light in helping us imagine what the final product looked like. This helped us in our planning process ultimately leading to coding with less confusion.
* Some functional requirements could have included further detail so each team member would have knowledge on how the feature would function, regardless of whether they implemented it or not. 

#### What did you miss in your initial planning for the project (beyond just the requirements)?
* If we had a prototype or mockup diagram of what the UI would look like and how it would funciton would have been very useful as the team would have a shared vision of what the app would look like. This would have prevented some button placement conflicts that we ran into during development. 
* As well, halfway throughout the project we implemented a scrum-like process which greatly aided the team in  development and communication. Had we initially planned for this right from the start, the initial weeks of the project would have progressed smoother and more consistently.

#### What process did you use (ie Scrum, Kanabn..), how was it managed, and what was observed? 
* Our team utilized the GitHub Project KanBan board. This board tracked Backlog, In-Progress, Review, and Completed tasks. This board was super well received by the team members and allowed us to accurately see what was currently worked on, what was next and also who was working on what. The kanban board also allowed us to see what was actively in review and prompted team members to visit the PR to complete reviews. 
* During the reading break our team lacked in communication and development, so on the Monday we all returned a Scrum-like process was proposed and incorporated into our flow. This process included near-daily check-ins through our team group chat and provided weekly goals and tasks for each team member. This workflow enabled us to speed up development and communication between team members.

#### As a team, did you encounter issues with different team members developing with different IDEs?  In the future, would the team change anything in regard to the uniformity of development environments?
* In our team, all members used VS Code, however some were on Apple Machines and some on Windows. This was not an issue in deploying however, and development across environments was smooth. 
* An issue however, was the initial setup for the environment. Installing python and getting all the dependencies, and launching the appliation initially was not documented very well. But through communication and help sessions between members we encoutered minimal further issues.

#### If you were to estimate the efforts required for this project again, what would you consider?  (Really I am asking the team to reflect on the difference between what you thought it would take to complete the project vs what it actually took to deliver it).   
Our team all agrees that we definitely underestimated the effort the project would take. We did not account for the effort and mostly time it would take in testing, developing, reviewing and launching. With the time constraint realized now, we would have reduced or removed some of the functional requirements such as dark mode, and put more emphasis on initial communication, planning, and documentation so that we could have had more consistent development right from the start. 

#### What did your team do that you feel is unique or something that the team is especially proud of (was there a big learning moment that the team had in terms of gaining knowledge of a new concept/process that was implemented).
 * Utilizing the scrum-like proposed process really helped us pick up from the reading break and begin consistently implementing features. This change of process allowed members to stay up to date with the project status and what was required by a set date. 
 * We used a four layer architecture model where each layer was essentially (UI, front-end server, back-end server and database). Distinguishing between the two servers allowed each to focus on their own task (front-end server managing UI logic and backend server connecting to database). This model prevented the god class antipattern which would have happened had we not used this approach.

#### How did AI impact the development of the project? 
GitHub Copilot and ChatGPT were both utilized through the development of this project. 
 * Both systems helped not only in understanding components or proper syntax, but helped in generating code snippets for use in the application. Although the code snippets always required a code inspection by the team member and some refactoring, it greatly helped in generating the basic code structure and syntax. 
 * The systems also greatly aided in debugging errors and providing potential solutions for problems. 
 * Outside of development, these resources also aided in some problems with git and some errors we encountered during the git integration that some of us are new to.
