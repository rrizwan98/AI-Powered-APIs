from fastapi import APIRouter, HTTPException
from db import Session, engine, Student
from sqlmodel import Session, select
import yaml

def read_all_students() -> list[Student]:
    """
    Retrieve all students from the database.

    Returns:
       - list: A list of all students.
    """
    with Session(engine) as session:
        students = session.exec(select(Student)).all()
        return students
    
def read_students(student_id) -> Student:
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

def create_students(student: Student) -> Student:
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

def update_students(student_id: int, student: Student) -> Student:
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

def delete_students(student_id: int) -> str:
    """
    Deletes a student with the given student_id.
    
    """
    with Session(engine) as session:
        student = session.get(Student, student_id)
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        session.delete(student)
        session.commit()
        return {"ok": True}

def privacy_policys():
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