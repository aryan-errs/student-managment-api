from bson import ObjectId

def student_serializer(student: dict) -> dict:
    student["id"] = str(student["_id"])
    del student["_id"]
    return student

