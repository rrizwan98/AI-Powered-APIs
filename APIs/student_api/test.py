import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session
from db import Student, engine as main_engine  # adjust import path as necessary
from main import app  # adjust import path as necessary

# Use a separate test database if possible
TEST_DATABASE_URL = "postgresql://raza03492128287:wl0IsGkS8Fug@ep-frosty-sunset-a5cam3pe.us-east-2.aws.neon.tech/neondb?sslmode=require"
engine = create_engine(TEST_DATABASE_URL)

# Dependency override for testing
def get_test_db():
    try:
        db = Session(bind=engine)
        yield db
    finally:
        db.close()

app.dependency_overrides[app.get_db] = get_test_db

# Create test client
client = TestClient(app)

# Setup and teardown for the test database
@pytest.fixture(scope="module", autouse=True)
def create_test_database():
    SQLModel.metadata.create_all(bind=engine)
    yield  # Run tests
    SQLModel.metadata.drop_all(bind=engine)

def test_create_student():
    response = client.post("/students/", json={"name": "John Doe", "age": 22, "grade": "A"})
    data = response.json()
    assert response.status_code == 200
    assert data["name"] == "John Doe"
    assert "id" in data

def test_read_students():
    response = client.get("/students/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0  # Assuming at least one student was added in test_create_student

def test_read_student():
    # Create a student to ensure there is one to read
    student = {"name": "Jane Doe", "age": 23, "grade": "B"}
    post_response = client.post("/students/", json=student)
    student_id = post_response.json()["id"]

    # Test reading the newly created student
    response = client.get(f"/students/{student_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Jane Doe"

def test_update_student():
    # Create a student to ensure there is one to update
    student = {"name": "Update Test", "age": 20, "grade": "C"}
    post_response = client.post("/students/", json=student)
    student_id = post_response.json()["id"]

    # Test updating the student
    update_data = {"name": "Updated Name", "age": 21, "grade": "B"}
    response = client.put(f"/students/{student_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Name"
    assert data["age"] == 21

def test_delete_student():
    # Create a student to ensure there is one to delete
    student = {"name": "Delete Test", "age": 24, "grade": "D"}
    post_response = client.post("/students/", json=student)
    student_id = post_response.json()["id"]

    # Test deleting the student
    response = client.delete(f"/students/{student_id}")
    assert response.status_code == 200
    data = response.json()
    assert data == {"ok": True}

def test_privacy_policy():
    response = client.get("/student/privacy")
    assert response.status_code == 200
    # Your assertion here depends on the actual content you expect
    # For example:
    # assert response.json() == {"url": "http://api.example.com/privacy"}
