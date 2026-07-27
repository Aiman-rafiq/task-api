from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# In-memory "database"
tasks = [
    {"id": 1, "title": "Complete Week 2 assignment", "done": False},
    {"id": 2, "title": "Learn FastAPI basics", "done": True},
    {"id": 3, "title": "Build CRUD API", "done": False}
]

# Pydantic model: yeh batayega ke client ko JSON mein kya bhejna hai
class TaskCreate(BaseModel):
    title: str | None = None  # None isliye rakha taake agar title missing ho toh error aaye

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

# POST endpoint - Naya task create karne ke liye
@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):
    # Validation: agar title missing hai ya empty string hai
    if not task.title or not task.title.strip():
        raise HTTPException(status_code=400, detail="Title is required and cannot be empty")

    # Next free ID calculate karna
    next_id = max([t["id"] for t in tasks]) + 1 if tasks else 1

    # Naya task object banana
    new_task = {
        "id": next_id,
        "title": task.title,
        "done": False
    }
    
    tasks.append(new_task)
    return new_task