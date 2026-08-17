from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import Response
import sqlite3

app = FastAPI(
    title="Task API",
    description="A simple CRUD API for managing to-do tasks with SQLite database",
    version="1.0"
)

# Database setup
def get_db_connection():
    conn = sqlite3.connect('tasks.db')
    conn.row_factory = sqlite3.Row  # This allows us to access columns by name
    return conn

def init_db():
    """Initialize database with tasks table and seed data"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done INTEGER DEFAULT 0
        )
    ''')
    
    # Check if table is empty (only seed if empty)
    cursor.execute('SELECT COUNT(*) FROM tasks')
    count = cursor.fetchone()[0]
    
    if count == 0:
        # Seed 3 example tasks
        seed_tasks = [
            ("Complete Week 2 assignment", 0),
            ("Learn FastAPI basics", 1),
            ("Build CRUD API", 0)
        ]
        cursor.executemany('INSERT INTO tasks (title, done) VALUES (?, ?)', seed_tasks)
    
    conn.commit()
    conn.close()

# Initialize database on startup
init_db()

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
    """Get all tasks from the database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks')
    tasks = cursor.fetchall()
    conn.close()
    
    # Convert to list of dictionaries
    return [dict(task) for task in tasks]

@app.get("/tasks/{task_id}", tags=["Tasks"])
def get_task(task_id: int):
    """Get a single task by its ID"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
    task = cursor.fetchone()
    conn.close()
    
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    
    return dict(task)

@app.post("/tasks", status_code=201, tags=["Tasks"])
def create_task(task: TaskCreate):
    """Create a new task with title validation"""
    if not task.title or not task.title.strip():
        raise HTTPException(status_code=400, detail="Title is required and cannot be empty")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO tasks (title, done) VALUES (?, ?)', (task.title, 0))
    conn.commit()
    
    # Get the newly created task
    new_id = cursor.lastrowid
    cursor.execute('SELECT * FROM tasks WHERE id = ?', (new_id,))
    new_task = cursor.fetchone()
    conn.close()
    
    return dict(new_task)

@app.put("/tasks/{task_id}", tags=["Tasks"])
def update_task(task_id: int, task_update: TaskUpdate):
    """Update an existing task's title and/or done status"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if task exists
    cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
    existing_task = cursor.fetchone()
    
    if existing_task is None:
        conn.close()
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    
    # Update fields
    new_title = task_update.title if task_update.title is not None else existing_task['title']
    new_done = task_update.done if task_update.done is not None else existing_task['done']
    
    # Validate title if it's being updated
    if task_update.title is not None and not new_title.strip():
        conn.close()
        raise HTTPException(status_code=400, detail="Title cannot be empty")
    
    cursor.execute('''
        UPDATE tasks 
        SET title = ?, done = ? 
        WHERE id = ?
    ''', (new_title, 1 if new_done else 0, task_id))
    
    conn.commit()
    
    # Fetch updated task
    cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
    updated_task = cursor.fetchone()
    conn.close()
    
    return dict(updated_task)

@app.delete("/tasks/{task_id}", status_code=204, tags=["Tasks"])
def delete_task(task_id: int):
    """Delete a task by ID - returns 204 No Content on success"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if task exists
    cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
    task = cursor.fetchone()
    
    if task is None:
        conn.close()
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    
    cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    
    return Response(status_code=204)