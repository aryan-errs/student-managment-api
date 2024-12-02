from fastapi import FastAPI
from app.routers import students

app = FastAPI()

# Include routers
app.include_router(students.router, prefix="/students", tags=["Students"])

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to the Student Managment API!"}


if __name__ == "__main__":
    # Get the port from the environment or use 8000 as a fallback
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
