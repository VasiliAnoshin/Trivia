# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

# API Reference

### Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, ```http://127.0.0.1:5000/```, which is set as a proxy in the frontend configuration.
- Authentification: This version of the application does not require authentification or API keys.

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
  "success": False,
  "error": 400,
  "message": "bad request"
}
```

The API will return:
- 400: Bad request
- 404: Resource Not found
- 422: Not processable
- 500: Server error
- 405: Method not allowed

### Endpoints
### GET '/categories'
- Genreal:
  - Fetches a list of categories
  - Request Arguments: None
  - Returns: List with  categories
- Sample
  -```curl localhost:5000/categories```
```
  [ "Science",
    "Art",
    "Geography",
    "History",
    "Entertainment",
    "Sports"
    ]
```

#### GET /questions
- Genreal:
  - Return a list of questions, number of total questions, current category,categories. 
  - Result are paginated in group of 10. Include a request argument to choose page number, starting from 1
  - Request Argument: page
- Sample:
  - Sample: ``` curl localhost:5000/questions ```
```
{
  'success': True,
  'questions':
  [
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 4, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }
  ],
  'total_questions': 18,
  'current_category': '',
  'categories' : [
    "Entertainment", 
    "History", 
    "Sports", 
    "Geography", 
    "Art", 
    "Science"
  ],
}
```
#### DELETE /questions/<int:id>
- Genreal:
  - DELETE question using a question ID.
  - Request Argument: None
- Sample: ```curl -X DELETE localhost:5000/questions/1```
```
{
  "success": true
}
```
#### POST /questions
- Genreal:
  - POST a new question,  which will require the question and answer text, category, and difficulty score. (When you submit a question on     the "Add" tab, the form will clear and the question will appear at the end of the last page of the questions list in the "List" tab)
  - Request Argument for Post new question: None
  - Get questions based on a search term. Return any questions for whom the search term is a substring of the question.
    (Search by any phrase. The questions list will update to include only question that include that string within their question. 
    Try using the word "title" to start.)
  - Request Argument for Search: page

#### GET /categories/<int:id>/questions
- Genreal:
  - Get questions based on category.
  - Request Argument: page
- Sample: ```curl -X GET localhost:5000/categories/3/questions```
```
{
  "categories": [
    "Science",
    "Art",
    "Geography",
    "History",
    "Entertainment",
    "Sports"
  ],
  "current_category": 3,
  "questions": [
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
    },
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ],
  "success": true,
  "total_questions": 3
}
```  
#### POST /quizzes
- Genreal:
  - Get questions to play the quiz. This endpoint recieve category + previous question parameters 
    and return a random questions within the given category, if provided, and that is not one of the previous questions.
  - Request Argument: None

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
