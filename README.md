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

## Adding a Todo List item using Curl

```bash
curl -s -X POST -H 'Accept: application/json' -H 'Content-Type: application/json' -H "Authorization: Bearer ${TOKEN}"  --data '{"id":45,"title":"Drop it like its hot","description":"It is very hot.  It has to be dropped and dropped now", "due_date":"2024-01-26", "status":"researching", "category":"Shepard"}' http://127.0.0.1:5000/api/todo
```

## Retrieving an existing Todo by it's ID
```bash
curl -s -X GET -H 'Accept: application/json' -H 'Content-Type: application/json' -H "Authorization: Bearer ${TOKEN}" http://127.0.0.1:5000/api/todo/45 | jq .
{
  "category": "Shepard",
  "description": "It is very hot.  It has to be dropped and dropped now",
  "due_date": "Fri, 26 Jan 2024 00:00:00 GMT",
  "id": 45,
  "status": "researching",
  "title": "Drop it like its hot"
}
```

## Updating a TODO list item by it's id

Lets update the status to pending, and change the category to 'slinky' for item with id '45'

```bash
curl -s -X PUT -H 'Accept: application/json' -H 'Content-Type: application/json' -H "Authorization: Bearer ${TOKEN}" --data '{"status":"pending", "category":"Slinky"}' http://127.0.0.1:5000/api/todo/45
```

Now lets re-print the specific item by id to see the changes

```bash
curl -s -X GET -H 'Accept: application/json' -H 'Content-Type: application/json' -H "Authorization: Bearer ${TOKEN}" http://127.0.0.1:5000/api/todo/45 | jq .
{
  "category": "Slinky",
  "description": "It is very hot.  It has to be dropped and dropped now",
  "due_date": "Fri, 26 Jan 2024 00:00:00 GMT",
  "id": 45,
  "status": "pending",
  "title": "Drop it like its hot"
}
```

## Deleting a todo list item by it's id

```bash
curl -s -X DELETE -H 'Accept: application/json' -H 'Content-Type: application/json' -H "Authorization: Bearer ${TOKEN}" http://127.0.0.1:5000/api/todo/45 
{"message":"Todo item deleted successfully."}
```