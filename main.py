from fastapi import FastAPI

app = FastAPI()

# Root endpoint
@app.get("/")
def read_root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "ok"}