from fastapi import FastAPI, HTTPException

app = FastAPI()

# In-memory "database" - 3 example tasks
tasks = [
    {"id": 1, "title": "Complete Week 2 assignment", "done": False},
    {"id": 2, "title": "Learn FastAPI basics", "done": True},
    {"id": 3, "title": "Build CRUD API", "done": False}
]

@app.get("/")
def read_root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}

@app.get("/health")
def health_check():
    return {"status": "ok"}

# GET /tasks - List all tasks
@app.get("/tasks")
def get_tasks():
    return tasks

# GET /tasks/{id} - Get single task by ID
@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    # Task not found - return 404
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")