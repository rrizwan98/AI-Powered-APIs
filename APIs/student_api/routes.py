# routes.py
from fastapi import APIRouter, HTTPException
from db import Session, engine, Student
from sqlmodel import Session, select
import yaml

def load_privacy_policy():
    with open("privacy_policy.yaml", "r") as file:
        privacy_policy = yaml.safe_load(file)
    return privacy_policy

def get_session():
    with Session(engine) as session:
        yield session


router = APIRouter()

@router.get("/students/")
def read_students():
    """
    Retrieve all students from the database.

    Returns:
       - list: A list of all students.
    """
    with Session(engine) as session:
        students = session.exec(select(Student)).all()
        return students

@router.get("/students/{student_id}")
def read_student(student_id: int):
    """
    Retrieve a student by their ID.

    Args:
      - student_id (int): The ID of the student to retrieve.

    Returns:
      -  Student: The student object.

    Raises:
      -  HTTPException: If the student is not found.
    """
    with Session(engine) as session:
        student = session.get(Student, student_id)
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        return student

@router.post("/students/")
def create_student(student: Student):
    """
    Creates a new student record in the database.

    Args:
      - student (Student): The student object to be created.

    Returns:
       - Student: The created student object.
    """
    with Session(engine) as session:
        session.add(student)
        session.commit()
        session.refresh(student)
        return student

@router.put("/students/{student_id}")
def update_student(student_id: int, student: Student):
    """
    Update a student in the database.

    Args:
      -  student_id (int): The ID of the student to update.
      -  student (Student): The updated student data.

    Returns:
      -  Student: The updated student object.

    Raises:
      -  HTTPException: If the student is not found in the database.
    """
    with Session(engine) as session:
        db_student = session.get(Student, student_id)
        if not db_student:
            raise HTTPException(status_code=404, detail="Student not found")
        student_data = student.dict(exclude_unset=True)
        for key, value in student_data.items():
            setattr(db_student, key, value)
        session.add(db_student)
        session.commit()
        session.refresh(db_student)
        return db_student

@router.delete("/students/{student_id}")
def delete_student(student_id: int):
    """
    Deletes a student with the given student_id.
    
    Args:
      - student_id (int): The ID of the student to be deleted.
    
    Returns:
       - dict: A dictionary indicating the success of the deletion.
    """
    with Session(engine) as session:
        student = session.get(Student, student_id)
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        session.delete(student)
        session.commit()
        return {"ok": True}

@router.get("/student/privacy")
def privacy_policy():
    """
    Retrieves the privacy policy data from the 'privacy_policy.yaml' file.

    Returns:
        dict: The privacy policy data.
    
    Raises:
        HTTPException: If there is an error reading the file or if the file is empty or incorrectly formatted.
    """
    try:
        with open("privacy_policy.yaml", "r") as file:
            policy_data = yaml.safe_load(file)
            if policy_data is None:
                raise ValueError("The YAML file is empty or incorrectly formatted.")
            return policy_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))