# flask-simple-todo
A very simple todo list manager using Flask as a front-end to a MongoDB backend

# Purpose
This fairly simple Flask application is meant as a fairly straightforward REST API implementation of a Tod List manager.  This todo list manager will be deployed as a locally executing REST API application acting as a API backend for an Autogen Python API services.

the end goal is to have a ChatGPT like interface on top of a todo list manager.  Ideally, it will be the backend for a platform such as Autogen.

## Authenticating using curl

```bash
curl -s -X POST -H 'Accept: application/json' -H 'Content-Type: application/json' --data '{"username":"admin","email":"admin@admin.com","password":"bad_password","rememberMe":false}' http://127.0.0.1:5000/api/auth

{"data":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiZW1haWwiOiJhZG1pbkBhZG1pbi5jb20iLCJyb2xlcyI6WyJhZG1pbiIsInVzZXIiXSwiZXhwIjoxNzA1ODA5NjAzLjM0NzU5MX0.YDesh_W0Ur5-H8Fvux3kEOqajDmXjrkM2tXxUdWRdM4","status":200}

```

```bash
TOKEN=$(curl -s -X POST -H 'Accept: application/json' -H 'Content-Type: application/json' --data '{"username":"admin","email":"admin@admin.com","password":"bad_password","rememberMe":false}' http://127.0.0.1:5000/api/auth | jq -r '.data')

echo $TOKEN
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiZW1haWwiOiJhZG1pbkBhZG1pbi5jb20iLCJyb2xlcyI6WyJhZG1pbiIsInVzZXIiXSwiZXhwIjoxNzA1ODA5NjMyLjE5ODQ0Nn0.J944iZx7lBCQxLWXtUfRKHazYfQAMokPtg3iHjLhOjM

curl -H 'Accept: application/json' -H "Authorization: Bearer ${TOKEN}" http://127.0.0.1:5000/api/todos | jq .

[
  {
    "category": null,
    "description": "Milk, Bread, Eggs",
    "due_date": "Thu, 25 Jan 2024 00:00:00 GMT",
    "id": 1,
    "status": "pending",
    "title": "Buy Groceries"
  },
  {
    "category": null,
    "description": "Milk, Bread, Eggs",
    "due_date": "Thu, 25 Jan 2024 00:00:00 GMT",
    "id": 2,
    "status": "pending",
    "title": "Buy Groceries"
  },
  {
    "category": null,
    "description": "Milk, Bread, Eggs",
    "due_date": "Thu, 25 Jan 2024 00:00:00 GMT",
    "id": 3,
    "status": "pending",
    "title": "Buy Groceries"
  },
  {
    "category": null,
    "description": "Milk, Bread, Eggs",
    "due_date": "Thu, 25 Jan 2024 00:00:00 GMT",
    "id": 4,
    "status": "pending",
    "title": "Buy Groceries"
  },
  {
    "category": null,
    "description": "Milk, Bread, Eggs",
    "due_date": "Thu, 25 Jan 2024 00:00:00 GMT",
    "id": 5,
    "status": "pending",
    "title": "Buy Groceries"
  },
  ... continued
]
```