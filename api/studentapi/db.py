# database.py
from sqlmodel import SQLModel, create_engine, Session, Field
from typing import Optional

# Database URL
DATABASE_URL = "postgresql://raza03492128287:wl0IsGkS8Fug@ep-frosty-sunset-a5cam3pe.us-east-2.aws.neon.tech/neondb?sslmode=require"

engine = create_engine(DATABASE_URL)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

class Student(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    age: int
    grade: str
