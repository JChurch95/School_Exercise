from .base import Base

class Student(Base, table=True):
    __tablename__ = "students"

    student_name: str