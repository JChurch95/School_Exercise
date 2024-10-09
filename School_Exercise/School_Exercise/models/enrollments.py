from .base import Base

class Enrollment(Base, table=True):
    __tablename__ = "enrollments"

    student_id: int
    course_id: int
    enrollment_date: str