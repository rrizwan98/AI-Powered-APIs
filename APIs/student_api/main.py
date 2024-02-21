
from fastapi import FastAPI, HTTPException
from sqlmodel import Session, select

from sqlmodel import SQLModel, Field, create_engine
from typing import Optional

from fastapi.middleware.cors import CORSMiddleware

class Student(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    age: int
    grade: str

# Database URL
DATABASE_URL = "postgresql://raza03492128287:wl0IsGkS8Fug@ep-frosty-sunset-a5cam3pe.us-east-2.aws.neon.tech/neondb?sslmode=require"

# Create the database engine
engine = create_engine(DATABASE_URL)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

app = FastAPI(
    title = "Student API",
    description = "A simple API to perform CRUD operations on students.",
    version = "0.1",
    servers=[{"url": "https://singular-sought-sunbeam.ngrok-free.app", "description": "Localhost"}], 
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/students/")
def read_students():
    """
    Retrieve all the students from the database.

    Returns:
        list: A list of student objects.
    """
    with Session(engine) as session:
        students = session.exec(select(Student)).all()
        return students

@app.get("/students/{student_id}")
def read_student(student_id: int):
    """
    Retrieve a student by their ID.

    Args:
        student_id (int): The ID of the student to retrieve.

    Returns:
        Student: The student object.

    Raises:
        HTTPException: If the student is not found.
    """
    with Session(engine) as session:
        student = session.get(Student, student_id)
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        return student

@app.post("/students/")
def create_student(student: Student):
    """
    Creates a new student record in the database.

    Args:
        student (Student): The student object to be created.

    Returns:
        Student: The created student object.
    """
    with Session(engine) as session:
        session.add(student)
        session.commit()
        session.refresh(student)
        return student

@app.put("/students/{student_id}")
def update_student(student_id: int, student: Student):
    """
    Update a student record in the database.

    Args:
        student_id (int): The ID of the student to update.
        student (Student): The updated student data.

    Returns:
        Student: The updated student record.

    Raises:
        HTTPException: If the student with the given ID is not found in the database.
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

@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    """
    Deletes a student with the given student_id.

    Args:
        student_id (int): The ID of the student to be deleted.

    Returns:
        dict: A dictionary indicating the success of the deletion operation.
            If the student is successfully deleted, 
            the dictionary will contain {"ok": True}.
    """
    with Session(engine) as session:
        student = session.get(Student, student_id)
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        session.delete(student)
        session.commit()
        return {"ok": True}
