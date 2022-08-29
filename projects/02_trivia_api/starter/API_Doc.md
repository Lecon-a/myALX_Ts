# API Documentation

## Getting Started

- Base URL: Currently this app is ran locally, and not yet hosted on production environment as a Base URL. Therefore, the backend app is hosted at http://127.0.0.1:5000/ or localhost:5000/ which is the default address. And also set as a proxy in the frontend configuration.

- API Keys or Authentication: This current version does not use authentication (API Keys) to access it.

## * Error Handling

Errors are turned as JSON objects (i.e key:Value pair) in the following structure:

```
    {
      'success': False,
      'error': 422,
      'message': 'unprocessable'
    }
```

The API will return five error types when requests failed:

- 404: Resource not found
- 405: Method not allowed
- 400: Bad request
- 422: Unprocessable
- 500: Internal server error

## Endpoints

### GET /categories

- General:
    - Returns a success, list of all the avialable category objects value, total number of categories
    
- Sample: curl -X GET http://127.0.0.1:5000/categories

```
    {
    "categories": [
        "Science",   
        "Art",       
        "Geography",
        "History",
        "Entertainment",
        "Sports",
        "Spiritual",
        "Traditional",
        "Programming"
    ],
    "success": true,
    "total_categories": 9
    }
```

### GET or POST /questions

- General:
This endpoint does listen to two different methods (GET and POST), therefore, responsible in handling three operations (retrieve, create, and search).

    - Returns a success, list of paginated (10 at a time) questions objects value, total number of questions, current category and list of all the avialable categories without pagination.

For POST method, this check for search term to decide which of operation to be performed between *create now question or *search questions based on a term supplied (*Note: substring in respective of the category).
    
    - If true, returns a success, list of questions found with the term part of its content, total questions in the database all together both the searched and unsearched ones, and also returns current category the first search belongs.

    - Else, creates a new question, and returns success on successful insertion.
    
- Sample: curl -X GET http://127.0.0.1:5000/questions

```
{
    "categories": [
        "Science",
        "Art",
        "Geography",
        "History",
        "Entertainment",
        "Sports",
        "Spiritual",
        "Traditional",
        "Programming"
    ],
    "current_category": "Science",
    "questions": [
        {
            "answer": "The Liver",
            "category": 1,
            "difficulty": 4,
            "id": 20,
            "question": "What is the heaviest organ in the human body?", 
            "rating": 1
        },
        {
            "answer": "Blood",
            "category": 1,
            "difficulty": 4,
            "id": 22,
            "question": "Hematology is a branch of medicine involving the study of what?",        
            "rating": 1
        },
        {
            "answer": "Alexander Fleming",
            "category": 1,
            "difficulty": 3,
            "id": 21,
            "question": "Who discovered penicillin?",
            "rating": 1
        },
        {
            "answer": "One",
            "category": 2,
            "difficulty": 4,
            "id": 18,
            "question": "How many paintings did Van Gogh sell in his lifetime?",
            "rating": 1
        },
        {
            "answer": "Escher",
            "category": 2,
            "difficulty": 1,
            "id": 16,
            "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?",
            "rating": 1
        },
        {
            "answer": "Mona Lisa",
            "category": 2,
            "difficulty": 3,
            "id": 17,
            "question": "La Giaconda is better known as what?",
            "rating": 1
        },
        {
            "answer": "Jackson Pollock",
            "category": 2,
            "difficulty": 2,
            "id": 19,
            "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?",
            "rating": 1
        },
        {
            "answer": "Lake Victoria",
            "category": 3,
            "difficulty": 2,
            "id": 13,
            "question": "What is the largest lake in Africa?",
            "rating": 1
        },
        {
            "answer": "The Palace of Versailles",
            "category": 3,
            "difficulty": 3,
            "id": 14,
            "question": "In which royal palace would you find the Hall of       Mirrors?",
            "rating": 1
        },
        {
            "answer": "Agra",
            "category": 3,
            "difficulty": 2,
            "id": 15,
            "question": "The Taj Mahal is located in which Indian city?",
            "rating": 1
        }
    ],
    "success": true,
    "total_questions": 20
}   
```

##### For search:

- Sample: curl -X POST -H "Content-Type: application/json" -d '{"search_term":"Dutch"}' http://127.0.0.1:5000/questions

    - Without result

```   
    {
    "success": true
    }
```

    - With result

```
    {
        'success': True,
        'questions': [
            {
                'id': 16,
                'question': 'Which Dutch graphic artist–initials M C was a creator of optical illusions?',
                'answer': 'Escher',
                'category': 2,
                'difficulty': 1,
                'rating': 1
            }
        ], 
        'total_questions': 1,
        'current_category': 'Art'
    }
```    

##### For create:

Sample: curl -X POST -H "Content-Type: application/json" -d '{"question":"What is Rate of a Chemical Reaction?", "answer":"The rate of a chemical reaction is the number of moles of reactant converted or product formed per unit time.", "category":1, "difficulty":5, "rating":5}' http://127.0.0.1:5000/questions

```
    {
        'success': True
    }
```

### GET /categories/{category_id}/questions

Where category_id is an integer, so, this endpoint expects integer value.

Sample: curl -X GET /categories/6/questions

- Returns all questions belonging to category 6 in json object format as follows:

```
{
    "current_category": "Sports",
    "questions": [
        {
            "answer": "Brazil",
            "category": 6,
            "difficulty": 3,
            "id": 10,
            "question": "Which is the only team to play in every soccer World Cup tournament?",   
            "rating": 1
        },
        {
            "answer": "Uruguay",
            "category": 6,
            "difficulty": 4,
            "id": 11,
            "question": "Which country won the first ever soccer World Cup in       1930?",
            "rating": 1
        }
    ],
    "success": true,
    "total_questions": 26
}
```

### POST /quizzes

This endpoint listens to POST method and returns success, quiz_category, previous questions in a list format, a randomized distinct question by taking track of the previous question(s) id(s) whither filtered by distinct category or query all categories, 

Sample: curl -X POST -H "Content-Type: application/json" -d '{"quiz_category": "Science", "previous_questions": []}' http://127.0.0.1:5000/quizzes

```
    {
        'success': True, 
        'quiz_category': 'Science', 
        'previous_questions': [20], 
        'question': {
            'id': 20, 'question': 'What is the heaviest organ in the human body?', 
            'answer': 'The Liver', 
            'category': 1, 
            'difficulty': 4, 
            'rating': 1
        }
    }  
```

Note: The above is on one trial/play. Also, when you try that sample of your own terminal distinct question might comes up because it is randomized.

### PATCH /scores

This endpoint listens to PATCH method to update user's score, and also returns success, username. 

Sample: curl -X PATCH -H "Content-Type: application/json" -d '{"id":33, "name":"spog08", "user_score": 3}' http://127.0.0.1:5000/scores

```
    {
        'success': True, 
        'user_name': 'spog08'
    }  
```

### POST /users

Sample: curl -X POST -H "Content-Type: application/json" -d '{"name": "spog", "score":0}' http://127.0.0.1:5000/users

```
{
    'success': True
}
```

##### Appendices

```
Pagination function takes two parameters and return slided seletion
      
      Parameters:
        @request
        @selection => list of questions

      Returns:
        10 questions at a time  
```

```
    def randomizeQuiz(previous_ids, selection):
        size = len(selection)
        randomIndex = random.randint(0, size)
        if len(previous_ids) != 0:
            if randomIndex == size:
                return False
            s = selection[randomIndex]
            while s['id'] in previous_ids:
                randomIndex = random.randint(0, size)
    
        return randomIndex 
```

## Deployment N/A

## Authors

Sunday P. Afolabi

## Acknowledgements

The wonderfully Coach Caryn, Mr. Michael my session leader, community of developers alx-t slack channels, Stack-Overflow, Google search engine, the team developers of the libraries used to accomplish this trivia app project 2 to my becoming Full Stack Developer.