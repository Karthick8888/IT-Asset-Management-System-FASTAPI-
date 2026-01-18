from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.sql import func
from app.db.base import Base

class Employee(Base):
    __tablename__ = "employees"

    employeeid = Column(Integer, primary_key=True, index=True)
    fullname = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    department = Column(String(100))
    role = Column(String(50))

    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(
        TIMESTAMP,
        server_default=func.now(),
        onupdate=func.now()
    )
