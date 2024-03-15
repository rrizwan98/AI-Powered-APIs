import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

@pytest.fixture(scope="module")
def new_student():
    return {
        "name": "ali",
        "age": 20,
        "grade": "A"
    }

class TestRoutes:
    def test_create_student(self, new_student):
        response = client.post("/students/", json=new_student)
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert data["name"] == new_student["name"]
        assert data["age"] == new_student["age"]
        assert data["grade"] == new_student["grade"]

    def test_read_student(self, new_student):
        response = client.post("/students/", json=new_student)
        assert response.status_code == 200
        data = response.json()
        student_id = data["id"]
        
        response = client.get(f"/students/{student_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == new_student["name"]
        assert data["age"] == new_student["age"]
        assert data["grade"] == new_student["grade"]

    def test_update_student(self, new_student):
        response = client.post("/students/", json=new_student)
        assert response.status_code == 200
        data = response.json()
        student_id = data["id"]
        
        updated_student = {
            "name": "Jane Doe",
            "age": 21,
            "grade": "B"
        }
        response = client.put(f"/students/{student_id}", json=updated_student)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == updated_student["name"]
        assert data["age"] == updated_student["age"]
        assert data["grade"] == updated_student["grade"]

    def test_delete_student(self, new_student):
        response = client.post("/students/", json=new_student)
        assert response.status_code == 200
        data = response.json()
        student_id = data["id"]
        
        response = client.delete(f"/students/{student_id}")
        assert response.status_code == 200
        data = response.json()
        assert data == {"ok": True}
