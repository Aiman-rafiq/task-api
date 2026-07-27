 Task API
A simple CRUD API for managing to-do tasks built with FastAPI.
How to Run
1. Install dependencies:
pip install fastapi uvicorn
2. Start the server:
uvicorn main:app –reload
Endpoints
MethodEndpointDescriptionStatus CodesGET/API information200GET/healthHealth check200GET/tasksList all tasks200GET/tasks/{id}Get single task by ID200, 404POST/tasksCreate new task201, 400PUT/tasks/{id}Update task200, 400, 404DELETE/tasks/{id}Delete task204, 404
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

