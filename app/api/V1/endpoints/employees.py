from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.models.employees import Employee
from app.schemas.employees import (
    EmployeeCreate,
    EmployeeResponse
)
from app.db.session import get_db

router = APIRouter()


@router.post("/", response_model=EmployeeResponse)
def create_employee(
    employee: EmployeeCreate,
    db: Session = Depends(get_db)
):
    # Check if email already exists
    existing = db.query(Employee).filter(
        Employee.email == employee.email
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    new_employee = Employee(
        fullname=employee.fullname,
        email=employee.email,
        department=employee.department,
        role=employee.role
    )

    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)

    return new_employee


@router.get("/", response_model=List[EmployeeResponse])
def get_all_employees(
    db: Session = Depends(get_db)
):
    return db.query(Employee).all()


@router.get("/search", response_model=List[EmployeeResponse])
def search_employees(
    q: str = Query(..., min_length=1),
    db: Session = Depends(get_db)
):
    return (
        db.query(Employee)
        .filter(
            (Employee.fullname.ilike(f"%{q}%")) |
            (Employee.email.ilike(f"%{q}%")) |
            (Employee.department.ilike(f"%{q}%")) |
            (Employee.role.ilike(f"%{q}%"))
        )
        .all()
    )

