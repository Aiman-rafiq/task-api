from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import Response

app = FastAPI()

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

@app.get("/")
def read_root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/tasks")
def get_tasks():
    return tasks

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):
    if not task.title or not task.title.strip():
        raise HTTPException(status_code=400, detail="Title is required and cannot be empty")
    next_id = max([t["id"] for t in tasks]) + 1 if tasks else 1
    new_task = {"id": next_id, "title": task.title, "done": False}
    tasks.append(new_task)
    return new_task

# PUT endpoint - Update a task
@app.put("/tasks/{task_id}")
def update_task(task_id: int, task_update: TaskUpdate):
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

# DELETE endpoint - Delete a task
@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(i)
            return Response(status_code=204) # 204 means success but no body
            
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")