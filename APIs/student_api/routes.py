# routes.py
from fastapi import APIRouter, HTTPException
from db import Session, engine, Student
from sqlmodel import Session, select
import yaml
# from utils import read_student
from utils import read_all_students, read_students, create_students, update_students, delete_students, privacy_policys

def get_session():
    with Session(engine) as session:
        yield session


router = APIRouter()

@router.get("/students/")
async def read_student():
    """
    Retrieve all students from the database.
    
    """
    get_all_students = read_all_students()
    return get_all_students

@router.get("/students/{student_id}")
async def read_student_by_id(student_id: int):
    print(f"read_student called with ID: {student_id}")

    """
    Retrieve a student by their ID.
    """
    student:int = read_students(student_id)
    print(student)
    return student

@router.post("/students/")
async def create_student(student: Student):
    """
    Creates a new student record in the database.

    """
    create_student = create_students(student)
    return create_student

@router.put("/students/{student_id}")
async def update_student(student_id: int, student: Student):
    """
    Update a student in the database.

    """
    update_student = update_students(student_id, student)
    return update_student

@router.delete("/students/{student_id}")
async def delete_student(student_id: int):
    """
    Deletes a student with the given student_id.
    
    """
    delete_student = delete_students(student_id)
    return {"Student Delete Sucessfully": True}

@router.get("/student/privacy")
async def privacy_policy():
    """
    Retrieves the privacy policy data from the 'privacy_policy.yaml' file.

    """
    return privacy_policys()