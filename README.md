# Full Stack Capstone Project "Mymed"

## Application Purpose:
* Create a web service to keep track of medical information

### Main Files: Project Structure

  ```sh
  ./README.md
  ./config.yaml
  ./db-info.yaml
  ./requirements.txt      --> pip dependencies  
  ./migrations/           --> database migration files
  ./project/
  ./../app/
  ./../lib/
  ./../models/
  ./../setup/
  ./../views/
  ./../static/
  ./../../css /
  ./../../font/
  ./../../ico/
  ./../../img/
  ./../../js/
  ./../templates/
  ./../../errors/
  ./../../forms/
  ./../../layouts/
  ./../../pages/  
  ./conftest.py           --> configuration file for pytest
  ./setup.cfg             --> application setup (primarily for pytest) 
  ./tdd/                  --> folder for tests
  ./../fixtures/          --> directory for general test fixtures 
  ./../../static          --> directory for static test configuration files
  ./../../../config.yaml  --> app configuration file used for testing 
  ./../**/tdd_*.py *** pytest files
  ```

## Getting Started

### Install Python and Dependencies

#### Python 3.8
#### Virtual Environment
We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies
Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:
```bash
pip install -r requirements.txt
```
##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.
- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 
- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Configure Application:

Application environment variables are set using the `/config.yaml` file. 

1) Copy `/temp.config.yaml` to `/config.yaml`
2) Edit `/config.yaml` to set `port`, `mode`, `secret_key` and `jwt_secret`

## Database Setup: 

1) Install postrgesql and set up permissions.
    1) ##TODO: ADD postgres install commands! 
2) Copy /temp.db-info.yaml to /db-info.yaml and edit permissions.  
    1) To use defaults, leave username/password alone. 
        1) `username:default --> postgres`
        2) `password:default --> no password`
3) Initialize application databases.
4) Create application and testing databases: 

```bash
createdb db_project
createdb db_project_testing
```

5) Run migration scripts to seed/update database
```bash
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
```

## Testing deployment: 

#TODO --> FILL THIS SECTION OUT!!!!!!!

## Running the server

To run the server, execute:

In Linux:
```bash
export FLASK_APP=project
export FLASK_ENV=development
flask run
```

In Windows: 
```bash
set FLASK_APP=project
set FLASK_ENV=development
flask run
```

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 



## Permissions
### Commentary

A main application goal is to empower the everyday User who is considered the Patron of their information instead of being treated as a Customer or Patient of a health institution. 

With this in mind, I implemented my own Role Based Access Control outside of Auth0 for a number of reasons:
* Client-side Authentication Flow Ignorance (When the project began)
  * Initially unsure of how to programmatically test authentication flow efficiently  
  * Initially unsure of how the application could log users in and capture jwts for future use
  * Auth0 based test efficiency struggles:
    * Long Token expiry when using Auth0 lowered confidence in authentication flow 
    * Unknown number of profile cases
      * Need to create profile test cases with minimal setup time
      * No desire to create a large number of dummy emails for project. 
      * Feels wrong to include publish production tokens to public repository
    * Distribution of test tokens to tests:
      * Manual token management through postman or config files slowed time-to-development
      * Uncontrolled token expiry creates test friction
* Desire to build security into the database interactions within api access methods
  * RBAC presented in course followed the "What kind of verb should the role have?" was a secondary concern to "How can we securely empower the user to the fullest extent?"


With this internal implementation of RBAC, I learned a lot about the challenges associated with owning this aspect of application design. 
* Tracking "who was involved with the action" behaviors is less trivial than simply granting permissions to perform actions
* Fully testing more complex database architectures takes a lot of integration testing, planning and setup. 


In the spirit of project completion, I am limiting my scope by acknowledging a few issues that would need to be addressed to protect from bad actors: 
* External bad actors
  * Implement /api/userprofile email verification
  * Implement consent processes to:
    * add userprofiles to addresses
    * add (schedule) appointments for patrons and providers
    * add managers/schedulers/providers to addresses
    * Confirm provider certifications
* Internal bad actors:
  * Userprofile data isolation 
  * End-to-end encryption
  * Distributed application deployment

Some other philosophical concerns related to patron data ownership which were solved with the simplest implementation include:
* Should both patron and provider own the records they generate?
* Do addresses with managed providers need to be verified/certified before appointments can be scheduled?


### Role Based Permissions (The Nouns and Verbs):

#### Anonymous Client:
Though no 'permissions' structure is explicitly implemented for anonymous visitors, any application visitor should be able to retrieve a list of publicly listed addresses

#### UserProfile/Patron (All UserProfiles are Patrons):
Separating these two ideas into different tables helped me reason about the authentication and registration flow separate from the internal business logic. 
```

```

## Potential Performance Enhancements:
* Result Pagination

# API Reference 

## API Errors
#### 404 Resource Not Found
Server could not find requested resource.
#### 422 Unprocessable
Method used incorrectly on the target resource.
#### 405 Method Not Allowed
Request Method cannot be used on the target resource.
#### 500 Internal Server Error
Server encountered an issue while processing the request.  

### GET /api/categories
#### General
* Retrieves all available question categories in json format
#### Sample Request
```bash
curl -X GET --url http://localhost:5000/api/categories
```
#### Sample Response
```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true,
  "total_categories": 6
}
```


### GET /api/questions
#### General
* Get a page of 10 questions from all categories.
* To request a specific page of questions, use 'page' arg in get request. 
* Returns fields: success, categories, current_category, page, questions, total_questions
#### Sample Request
```bash
curl -X GET --url http://localhost:5000/api/questions
curl -X GET --url http://localhost:5000/api/questions?page=1
```
#### Sample Response
```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": "ALL",
  "page": 1,
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ],
  "success": true,
  "total_questions": 19
}
```

### POST /api/questions (add new question)
#### General
* Adds a question to the list of available questions.
* Requires fields 'answer', 'category', 'difficulty', 'question'.
* (optional) 'id' field may be specified and will be used if it does not already exist. 
#### Sample Request
```bash
curl --url http://localhost:5000/api/questions --data "{\"category\": \"5\", \"answer\": \"Nowhere\", \"question\": \"There is a Korean Film titled \\\"The Man From _________\\\"\", \"difficulty\": 3}" -H "Content-Type: application/json"
```
#### Sample Response
```json
{
  "question": {
    "answer": "Nowhere",
    "category": 5,
    "difficulty": 3,
    "id": 26,
    "question": "There is a Korean Film titled \"The Man From _________\""
  },
  "success": true
}
```

### POST /api/questions (search)
#### General
* Search for questions containing the provided 'searchTerm' 
#### Sample Request
```bash
 curl --url http://localhost:5000/api/questions --data "{\"searchTerm\": \"Lestat\"}" -H "Content-Type: application/json"
```
#### Sample Response
```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": "ALL",
  "page": 1,
  "questions": [
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }
  ],
  "success": true,
  "total_questions": 1
}
```  

### DELETE /api/questions/#
#### General
* Deletes the question with an id=#
#### Sample Request
```bash
curl --url http://localhost:5000/api/questions/25 -X DELETE
```
#### Sample Response
```json
{
  "deleted": 25,
  "success": true
}
``` 

### GET /api/questions/#
#### General
* Retrieves data on the question with id=#
#### Sample Request
```bash
curl --url http://localhost:5000/api/questions/5
```
#### Sample Response
```json
{
  "question": {
    "answer": "Maya Angelou",
    "category": 4,
    "difficulty": 2,
    "id": 5,
    "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
  },
  "success": true
}
``` 



### TEMPLATE /api/
#### General
* 
#### Sample Request
```bash

```
#### Sample Response
```json

``` 

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```