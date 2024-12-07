# Milestone 6
# **Progress Report Dashboard**

## **1. Tasks Completed (by Owner)**
| **Team Member**   | **Task(s)**                                      | **Status**      |
|-------------------|--------------------------------------------------|-----------------|
| **Syed Saad Ali** | - Manage communication between main.js and app.py| Completed       |
|                   | - Create Register User functionality             | In-Progress     |
|                   | - Test security features                         | Done            |
|                   | - Test reliability of app                        | Done            |
|                   | - Test performance of app                        | Done            |
| **Tawana Ndlovu** | - Write test plan                                | Completed       |
|                   | - Create basic testing framework (including CI)  | In-Progress     |
|                   | - Add Dashboard Page feature                     | In-Progress     |
| **Jan Suratos**   | - Create dashboard UI                            | Completed       |
|                   | - Manage connection to Open Weather Map API      | Completed       |
|                   | - Create login UI                                | Completed       |
|                   | - Add C/F toggle button and logic                | Completed       |
|                   | - Add dark mode feature                          | In-Progress     |
| **Ashish Nayak**  | - Database ER/UML Diagram                        | Completed       |
|                   | - Create Docker Database Connection              | Completed       |
|                   | - Implement login/logout feature                 | Completed       |
|                   | - Create main page mini dashboard                | In-Progress     |


## **2. Progress Summary**

### **Where We Are:**
- **Completed:**
  - [x] Test plan written
  - [x] Initial main page UI created
  - [x] Initial dashboard UI created
  - [x] Connection to Open Weather Map API
  - [x] Weather dashboard UI created
  - [x] Database created
  - [x] Backend database manager created and tested 
  - [x] Database ER/UML Diagram
  - [x] Create login/sign up UI 
  - [x] Implement dashboard functionality
  - [x] Implement login functionality
  - [x] Implement logout functionality  
  - [x] Server for end to end communication
  - [x] Configure database and connect to server
- **In Progress:**
  - [ ] Basic testing framework (including CI) [In-Review]
  - [ ] Ongoing Project Documentation
  - [ ] Create Register User functionality  
  - [ ] Create Dashboard Page functionality
  - [ ] Implement C/F switching [In-Review]
  - [ ] Finish writing Non Functional tests

- **Remaining:**
  - [ ] Implement dashboard sharing
  - [ ] Implement C/F saving to database and update on user login
  - [ ] Implement dark mode
  - [ ] Connect dark mode preference to databse and update on user login


---


## **3. Comments on Process**

- **What’s Working:**
  - Kanban board keeps tasks visible and manageable.
  - Iterative work on the project everyday.
  - Communication has been going well between team members since return from reading break. Involving daily check-ins and updates occuring in our project chat. 
  - The proposed scrum-like workflow has been working well and progress has been consistent as well as communication between members.
  - Rotate on roles so everyone understands each part of the project.
  - Following detailed PR template to describe PRs
  - Marking unfinished tasks as issues to priortize them.

- **Challenges:**
  - Communication gaps between integrating certain parts.
  - Keeping up with the PRs including reviewing and merging was initially a challenge, but the team quickly found a rhythm in this area. 
  - Initially the team was not creating issues for the PRs and features-list, however this was caught and the team began creating issues, adding them to PRs and closing them when completed in the kanbam board. 


- **Proposed Changes:**
  - Informal meetings to discuss where we are at, what questions need to be answered and what's next as we move forward.
  - Conduct retrospectives after each milestone to identify areas of improvement and celebrate successes.
  - Each member keeps track of open PRs and reviews when they are able. 

---

## **4. Branches/Tasks Completed and Tested/Merged**
| **Branch Name**             | **Task**                                           | **Merged**    | **Notes**                                             |
|-----------------------------|----------------------------------------------------|---------------|-------------------------------------------------------|
| `development`               | Development Progress                               | No, merged only as stable releases | branch for development, merging new features          |
| `milestone-4--dashboard`    | Summarize milestone 4 work                         | No, planned to be merged at project completion | branch for displaying milestone 4 update              |
| `milestone-5--dashboard`    | Summarize milestone 5 work                         | No, planned to be merged at project completion | branch for displaying milestone 5 update              |
| `milestone-6--dashboard`    | Summarize milestone 6 work                         | No, planned to be merged at project completion | branch for displaying milestone 6 update              |
| `test_Authentication`       | Testing                                            | No            | tests authentication                                  |
| `register_UI`               | Develop and test register user interface           | No            | developing and testing register user features         |
| `requirementsEngineering`   | Requirements Analysis                              | Yes           | branch for specifying requirements                    |
| `database_connection`       | Create docker database and python manager/tests    | Yes           | branch for developing database and the python manager to interact with db |
| `server-development`        | End to end communication                           | Yes           | branch for developing server                          |
| `test_UserFeatures`         | Testing                                            | Yes           | tests user features                                   |
| `test_WeatherDataAPI`       | Testing                                            | Yes           | tests weather data api                                |
| `login_functionality`       | Implement login functionality                      | Yes           | developing and testing login features                 |
| `logout_functionality`      | Implement logout functionality                     | Yes           | developing and testing logout features                |
| `add_pr_template`           | Add PR template                                    | Yes           | added pull request template to repo                   |
| `user_interface`            | Develop and test user interface                    | Yes           | major updates to ui developed                         |`index_locations_functionality` | Implement mini dashboard on index page         | Yes           | developing and testing mini dash features             |
| `test_DashboardConfiguration`| Testing                                           | In-Progress (Active PR) | tests dashboard features                              |
| `test_security`             | Testing security features                          | In-Progress (Active PR) | tests security features                               |
| `test_reliability`          | Testing reliability of app                         | In-Progress (Active PR) | tests reliability of app                              |
| `test_performance`          | Testing performance of app                         | In-Progress (Active PR) | tests performance of app                              |
| `celcius_fahrenheit_toggle` | Implement C/F toggle functionality                 | In-Progress (Active PR) | developing and testing C/F toggle features            |

---

## **5. Reflection**
One of the main challenges we faced was integrating the various components of our application, particularly ensuring that the Flask application could correctly serve static files. We also encountered difficulties with setting up the Docker environment, which required several tries to get right. The frontend has undergone several iterations, however it has been receiving steady development and is reaching our desired state. We believe that we have made good progress during the last milestone and are on track to completing the project. 


---

## **6. Testing Report**

- Create basic testing framework (including CI) is completed
- Failing tests during development of each new feature have been created before implementing functionality. Then after impleneting the feature, along with passing it's own tests, previous tests are expected to pass as well. This has been a requirement for our team as we develop and if the test doesn't psas, the team member resolves the issue before the feature is merged into dev.
- Test Plan spreadsheet has been updated as features have been added. (Seen on team member's UBC sharepoint, populated test plan will be added to repo on completion of project)
 
---

**Reminder:** Book a time with the TA during lab sessions to present this report.