from fastapi import APIRouter, HTTPException, Query, Path
from typing import Optional, List

from app.database import students_collection
from app.models.student import student_serializer
from app.schemas.student import Student, UpdateStudent, StudentResponse, DetailedStudentResponse
from bson import ObjectId

router = APIRouter()

@router.post("", status_code=201)
async def create_student(student: Student):
    # Convert the student object to a dictionary
    student_dict = student.dict()
    
    # check if the student already exists in the database
    existing_student = await students_collection.find_one({
        "name": student_dict["name"],
        "address.city": student_dict["address"]["city"],
        "address.country": student_dict["address"]["country"]
    })
    
    if existing_student:
        raise HTTPException(
            status_code=400, 
            detail="A student with the same name and address already exists."
        )
    # insert if not found
    result = await students_collection.insert_one(student_dict)
    return {"id": str(result.inserted_id)}

@router.get("", response_model=List[StudentResponse])
async def list_students(
    country: Optional[str] = Query(None),
    age: Optional[int] = Query(None)
):
    query = {}
    if country:
        query["address.country"] = country
    if age:
        query["age"] = {"$gte": age}
    
    students = await students_collection.find(query).to_list(100)
    return [student_serializer(student) for student in students]

@router.get("/{id}", response_model=DetailedStudentResponse)
async def fetch_student(id: str = Path(...)):
    student = await students_collection.find_one({"_id": ObjectId(id)})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student_serializer(student)

@router.patch("/{id}", status_code=204)
async def update_student(id: str, student: UpdateStudent):
    update_data = {k: v for k, v in student.dict().items() if v is not None}
    if update_data:
        result = await students_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": update_data}
        )
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Student not found")
    return

@router.delete("/{id}", status_code=200)
async def delete_student(id: str = Path(...)):
    result = await students_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student deleted successfully"}

