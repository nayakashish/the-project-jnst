

## Table of Contents

- [Architecture diagram](#architecture-diagram)
- [Sequence diagrams](#sequence-diagrams)
- [DFD](#dfd)
- [Activity plan](#activity-plan)
- [Test plan](#test-plan)


<img src="/the-project-jnst/images/architectureDiagram.png" alt="architectureDiagram" title="architectureDiagram" style="width: 50%;">

## Architecture diagram
Presentation Layer (Manages front end):

    UI: The main interface where the user interacts with. Sends and receives data from the server. 

Application Layer (Middle layer that manages client side requests, application logic, and data flow): 

    Server: Manages end to end requests and sends data appropriately.
    Authentication Module: Handles user authentication for login and log out.

Communication Layer (Handles external communication):

    Weather App API: The main source of weather data that sends data on a POST request.
    Firebase API: Authenticates users and handles login/logout. Stores user credentials.

Data Layer: Handles data storage 

    Weather JSON File: Weather data is stored in a JSON file upon saving or sharing the weather.

---

## Test plan
<div style="display: flex; flex-wrap: wrap; justify-content: space-between;">

  <div style="flex: 1 1 45%; margin: 5px;">
    <img src="images/TestPlan1.png" alt="Image 1" title="Persona 1" width="100%">
  </div>
  
  <div style="flex: 1 1 45%; margin: 5px;">
    <img src="images/TestPlan2.png" alt="Image 2" title="Persona 2" width="100%">
  </div>

</div>