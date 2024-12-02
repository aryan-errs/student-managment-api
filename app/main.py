from fastapi import FastAPI
from app.routers import students

app = FastAPI()

# Include routers
app.include_router(students.router, prefix="/students", tags=["Students"])

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to the Student Managment API!"}

