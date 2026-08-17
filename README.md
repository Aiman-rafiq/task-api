 Task API
A simple CRUD API for managing to-do tasks built with FastAPI.
How to Run
1. Install dependencies:
pip install fastapi uvicorn
2. Start the server:
uvicorn main:app �reload
Endpoints
Method
Endpoint
Description
Status Codes
GET
/
API information
200
GET
/health
Health check
200
GET
/tasks
List all tasks
200
GET
/tasks/{id}
Get single task by ID
200, 404
POST
/tasks
Create new task
201, 400
PUT
/tasks/{id}
Update task
200, 400, 404
DELETE
/tasks/{id}
Delete task
204, 404

Example curl Command
Create a new task:
curl -i -X POST http://localhost:8000/tasks -H "Content-Type: application/json" -d '{"title": "Buy milk"}'
Response:
HTTP/1.1 201 Created
content-type: application/json
content-length: 46
date: Mon, 27 Jul 2026 07:28:25 GMT
server: uvicorn
{"id":5,"title":"Buy groceries","done":false}
Swagger UI Screenshot

Features
*  Full CRUD operations (Create, Read, Update, Delete)
*  Input validation (title required, cannot be empty)
*  Proper HTTP status codes (200, 201, 204, 400, 404)
*  Interactive Swagger UI documentation
*  In-memory storage (no database required)
*  Health check endpoint for monitoring
Testing the API
You can test the API using:
* Swagger UI: http://localhost:8000/docs (recommended)
* curl: Command-line tool
* Browser: For GET endpoints
Push on Github:
   git push origin main


## Database Integration (Week 3)

### Why SQLite?
SQLite was chosen because it is a lightweight, serverless database that lives in a single file (`tasks.db`). It requires zero setup and ensures data survives server restarts.

### Database Location
The database file `tasks.db` is created automatically in the root folder when the server starts for the first time. It is usually git-ignored so each clone starts fresh.

### Example SQL Query
In Stage 4, I explored the database using DB Browser for SQLite. I ran the following query to find all completed tasks:
SELECT * FROM tasks WHERE done = 1;

