import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select
from db import get_session, init_db
from models.students import Student
from models.courses import Course
from models.enrollments import Enrollment
from pydantic import BaseModel
from typing import List
from datetime import date

app = FastAPI()

# Initialize the database
init_db()

# Pydantic models for request bodies
class StudentCreate(BaseModel):
    student_name: str

class CourseCreate(BaseModel):
    course_name: str

class EnrollmentCreate(BaseModel):
    student_id: int
    course_id: int
    enrollment_date: date

# Create operations
@app.post("/create/student", response_model=Student)
def create_student(student: StudentCreate, session: Session = Depends(get_session)):
    db_student = Student(student_name=student.student_name)
    session.add(db_student)
    session.commit()
    session.refresh(db_student)
    return db_student

@app.post("/create/course", response_model=Course)
def create_course(course: CourseCreate, session: Session = Depends(get_session)):
    db_course = Course(course_name=course.course_name)
    session.add(db_course)
    session.commit()
    session.refresh(db_course)
    return db_course

@app.post("/create/enrollment", response_model=Enrollment)
def create_enrollment(enrollment: EnrollmentCreate, session: Session = Depends(get_session)):
    db_enrollment = Enrollment(**enrollment.dict())
    session.add(db_enrollment)
    session.commit()
    session.refresh(db_enrollment)
    return db_enrollment

# Read operations
@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/students", response_model=List[Student])
def list_students(session: Session = Depends(get_session)):
    students = session.exec(select(Student)).all()
    return students

@app.get("/courses", response_model=List[Course])
def list_courses(session: Session = Depends(get_session)):
    courses = session.exec(select(Course)).all()
    return courses

@app.get("/enrollments", response_model=List[Enrollment])
def list_enrollments(session: Session = Depends(get_session)):
    enrollments = session.exec(select(Enrollment)).all()
    return enrollments

# Update operations
@app.put("/update/student/{id}", response_model=Student)
def update_student(id: int, student: StudentCreate, session: Session = Depends(get_session)):
    db_student = session.get(Student, id)
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    student_data = student.dict(exclude_unset=True)
    for key, value in student_data.items():
        setattr(db_student, key, value)
    session.add(db_student)
    session.commit()
    session.refresh(db_student)
    return db_student

@app.put("/update/course/{id}", response_model=Course)
def update_course(id: int, course: CourseCreate, session: Session = Depends(get_session)):
    db_course = session.get(Course, id)
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")
    course_data = course.dict(exclude_unset=True)
    for key, value in course_data.items():
        setattr(db_course, key, value)
    session.add(db_course)
    session.commit()
    session.refresh(db_course)
    return db_course

@app.put("/update/enrollment/{id}", response_model=Enrollment)
def update_enrollment(id: int, enrollment: EnrollmentCreate, session: Session = Depends(get_session)):
    db_enrollment = session.get(Enrollment, id)
    if not db_enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    enrollment_data = enrollment.dict(exclude_unset=True)
    for key, value in enrollment_data.items():
        setattr(db_enrollment, key, value)
    session.add(db_enrollment)
    session.commit()
    session.refresh(db_enrollment)
    return db_enrollment

# Delete operations
@app.delete("/delete/student/{id}", response_model=dict)
def delete_student(id: int, session: Session = Depends(get_session)):
    student = session.get(Student, id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    session.delete(student)
    session.commit()
    return {"ok": True}

@app.delete("/delete/course/{id}", response_model=dict)
def delete_course(id: int, session: Session = Depends(get_session)):
    course = session.get(Course, id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    session.delete(course)
    session.commit()
    return {"ok": True}

@app.delete("/delete/enrollment/{id}", response_model=dict)
def delete_enrollment(id: int, session: Session = Depends(get_session)):
    enrollment = session.get(Enrollment, id)
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    session.delete(enrollment)
    session.commit()
    return {"ok": True}

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)