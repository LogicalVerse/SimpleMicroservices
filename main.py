from __future__ import annotations

import os
from datetime import datetime
from typing import Dict, List, Optional
from uuid import UUID, uuid4

from fastapi import FastAPI, HTTPException, Query

from models.student import StudentCreate, StudentRead, StudentUpdate
from models.address import AddressRead
from models.courses import CoursesRead, CoursesCreate, CoursesUpdate
from models.hobbies import HobbiesRead, HobbiesCreate, HobbiesUpdate

# -----------------------------------------------------------------------------
# Config
# -----------------------------------------------------------------------------
port = int(os.environ.get("FASTAPIPORT", 8080))

# -----------------------------------------------------------------------------
# Fake in-memory "databases"
# -----------------------------------------------------------------------------
students: Dict[UUID, StudentRead] = {}
courses: Dict[UUID, CoursesRead] = {}
hobbies: Dict[UUID, HobbiesRead] = {}
addresses: Dict[UUID, AddressRead] = {}

# -----------------------------------------------------------------------------
# App
# -----------------------------------------------------------------------------
app = FastAPI(
    title="Student/Address/Courses/Hobbies API",
    description="Demo FastAPI app using Pydantic v2 models",
    version="0.1.0",
)

# -----------------------------------------------------------------------------
# Student endpoints
# -----------------------------------------------------------------------------
@app.post("/students", response_model=StudentRead, status_code=201)
def create_student(student: StudentCreate):
    if student.uni in [s.uni for s in students.values()]:
        raise HTTPException(status_code=400, detail="Student with this UNI already exists")

    student_read = StudentRead(**student.model_dump())
    students[student_read.id] = student_read
    return student_read


@app.delete("/students/{student_id}", status_code=204)
def delete_student(student_id: UUID):
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found")
    del students[student_id]
    return


@app.get("/students", response_model=List[StudentRead])
def list_students(
    uni: Optional[str] = Query(None, description="Filter by Columbia UNI"),
    first_name: Optional[str] = Query(None, description="Filter by first name"),
    last_name: Optional[str] = Query(None, description="Filter by last name"),
    email: Optional[str] = Query(None, description="Filter by email"),
    phone: Optional[str] = Query(None, description="Filter by phone number"),
    birth_date: Optional[str] = Query(None, description="Filter by date of birth (YYYY-MM-DD)"),
    city: Optional[str] = Query(None, description="Filter by city of at least one address"),
    country: Optional[str] = Query(None, description="Filter by country of at least one address"),
):
    results = list(students.values())

    if uni is not None:
        results = [p for p in results if p.uni == uni]
    if first_name is not None:
        results = [p for p in results if p.first_name == first_name]
    if last_name is not None:
        results = [p for p in results if p.last_name == last_name]
    if email is not None:
        results = [p for p in results if p.email == email]
    if phone is not None:
        results = [p for p in results if p.phone == phone]
    if birth_date is not None:
        results = [p for p in results if str(p.birth_date) == birth_date]
    if city is not None:
        results = [p for p in results if any(addr.city == city for addr in p.addresses)]
    if country is not None:
        results = [p for p in results if any(addr.country == country for addr in p.addresses)]

    return results


@app.get("/students/{student_id}", response_model=StudentRead)
def get_student(student_id: UUID):
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found")
    return students[student_id]


@app.patch("/students/{student_id}", response_model=StudentRead)
def update_student(student_id: UUID, update: StudentUpdate):
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found")

    stored = students[student_id].model_dump()
    stored.update(update.model_dump(exclude_unset=True))
    students[student_id] = StudentRead(**stored)
    return students[student_id]

# -----------------------------------------------------------------------------
# Courses endpoints
# -----------------------------------------------------------------------------
@app.post("/courses", response_model=CoursesRead, status_code=201)
def create_course(course: CoursesCreate):
    course_read = CoursesRead(id=uuid4(), **course.model_dump())
    courses[course_read.id] = course_read
    return course_read


@app.get("/courses", response_model=List[CoursesRead])
def list_courses(
    Name: Optional[str] = Query(None, description="Filter by student name"),
    UNI: Optional[str] = Query(None, description="Filter by university ID"),
):
    results = list(courses.values())

    if Name is not None:
        results = [c for c in results if c.Name == Name]
    if UNI is not None:
        results = [c for c in results if c.UNI == UNI]

    return results


@app.get("/courses/{course_id}", response_model=CoursesRead)
def get_course(course_id: UUID):
    if course_id not in courses:
        raise HTTPException(status_code=404, detail="Course not found")
    return courses[course_id]


@app.patch("/courses/{course_id}", response_model=CoursesRead)
def update_course(course_id: UUID, update: CoursesUpdate):
    if course_id not in courses:
        raise HTTPException(status_code=404, detail="Course not found")

    stored = courses[course_id].model_dump()
    stored.update(update.model_dump(exclude_unset=True))
    courses[course_id] = CoursesRead(**stored)
    return courses[course_id]


@app.delete("/courses/{course_id}", status_code=204)
def delete_course(course_id: UUID):
    if course_id not in courses:
        raise HTTPException(status_code=404, detail="Course not found")
    del courses[course_id]
    return

# -----------------------------------------------------------------------------
# Hobbies endpoints
# -----------------------------------------------------------------------------
@app.post("/hobbies", response_model=HobbiesRead, status_code=201)
def create_hobby(hobby: HobbiesCreate):
    hobby_read = HobbiesRead(id=uuid4(), **hobby.model_dump())
    hobbies[hobby_read.id] = hobby_read
    return hobby_read


@app.get("/hobbies", response_model=List[HobbiesRead])
def list_hobbies(
    Name: Optional[str] = Query(None, description="Filter by student name"),
    UNI: Optional[str] = Query(None, description="Filter by university ID"),
):
    results = list(hobbies.values())

    if Name is not None:
        results = [h for h in results if h.Name == Name]
    if UNI is not None:
        results = [h for h in results if h.UNI == UNI]

    return results


@app.get("/hobbies/{hobby_id}", response_model=HobbiesRead)
def get_hobby(hobby_id: UUID):
    if hobby_id not in hobbies:
        raise HTTPException(status_code=404, detail="Hobby not found")
    return hobbies[hobby_id]


@app.patch("/hobbies/{hobby_id}", response_model=HobbiesRead)
def update_hobby(hobby_id: UUID, update: HobbiesUpdate):
    if hobby_id not in hobbies:
        raise HTTPException(status_code=404, detail="Hobby not found")

    stored = hobbies[hobby_id].model_dump()
    stored.update(update.model_dump(exclude_unset=True))
    hobbies[hobby_id] = HobbiesRead(**stored)
    return hobbies[hobby_id]


@app.delete("/hobbies/{hobby_id}", status_code=204)
def delete_hobby(hobby_id: UUID):
    if hobby_id not in hobbies:
        raise HTTPException(status_code=404, detail="Hobby not found")
    del hobbies[hobby_id]
    return

# -----------------------------------------------------------------------------
# Root
# -----------------------------------------------------------------------------
@app.get("/")
def root():
    return {"message": "Welcome to the Student/Address/Courses/Hobbies API. See /docs for OpenAPI UI."}

# -----------------------------------------------------------------------------
# Entrypoint for `python main.py`
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
