from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import Response

app = FastAPI(
    title="Task API",
    description="A simple CRUD API for managing to-do tasks",
    version="1.0"
)

# In-memory "database"
tasks = [
    {"id": 1, "title": "Complete Week 2 assignment", "done": False},
    {"id": 2, "title": "Learn FastAPI basics", "done": True},
    {"id": 3, "title": "Build CRUD API", "done": False}
]

# Models for validation
class TaskCreate(BaseModel):
    title: str | None = None

class TaskUpdate(BaseModel):
    title: str | None = None
    done: bool | None = None

@app.get("/", tags=["Root"])
def read_root():
    """Root endpoint - API information"""
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}

@app.get("/health", tags=["Health"])
def health_check():
    """Health check endpoint - returns server status"""
    return {"status": "ok"}

@app.get("/tasks", tags=["Tasks"])
def get_tasks():
    """Get all tasks from the list"""
    return tasks

@app.get("/tasks/{task_id}", tags=["Tasks"])
def get_task(task_id: int):
    """Get a single task by its ID"""
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

@app.post("/tasks", status_code=201, tags=["Tasks"])
def create_task(task: TaskCreate):
    """Create a new task with title validation"""
    if not task.title or not task.title.strip():
        raise HTTPException(status_code=400, detail="Title is required and cannot be empty")
    next_id = max([t["id"] for t in tasks]) + 1 if tasks else 1
    new_task = {"id": next_id, "title": task.title, "done": False}
    tasks.append(new_task)
    return new_task

@app.put("/tasks/{task_id}", tags=["Tasks"])
def update_task(task_id: int, task_update: TaskUpdate):
    """Update an existing task's title and/or done status"""
    for task in tasks:
        if task["id"] == task_id:
            if task_update.title is not None:
                if not task_update.title.strip():
                    raise HTTPException(status_code=400, detail="Title cannot be empty")
                task["title"] = task_update.title
            if task_update.done is not None:
                task["done"] = task_update.done
            return task
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

@app.delete("/tasks/{task_id}", status_code=204, tags=["Tasks"])
def delete_task(task_id: int):
    """Delete a task by ID - returns 204 No Content on success"""
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(i)
            return Response(status_code=204)
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")