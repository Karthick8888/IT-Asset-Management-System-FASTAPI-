from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List


from app.db.session import get_db
from app.models.assignments import Assignment
from app.models.employees import Employee
from app.models.assets import Asset
from app.schemas.assignments import AssignmentCreate,AssignmentResponse,AssignmentStatus,AssignmentUpdate

router = APIRouter()


# 🔹 Get All Assets
@router.get("/")
def get_assignments(db: Session = Depends(get_db)):
    rows = (
        db.query(
            Assignment.assignmentid,
            Assignment.assigneddate,
            Assignment.assignmentstatus,
            Assignment.actualreturndate,
            Employee.employeeid,
            Employee.fullname.label("employeename"),
            Asset.assetid,
            Asset.name.label("assetname"),
        )
        .join(Employee, Assignment.employeeid == Employee.employeeid)
        .join(Asset, Assignment.assetid == Asset.assetid)
        .all()
    )

    return [
        {
            "assignmentid": r.assignmentid,
            "assigneddate": r.assigneddate,
            "assignmentstatus": r.assignmentstatus,
            "actualreturndate": r.actualreturndate,
            "employeeid": r.employeeid,
            "employeename": r.employeename,
            "assetid": r.assetid,
            "assetname": r.assetname,
        }
        for r in rows
    ]



@router.post("/")
def create_assignment(
    assignment: AssignmentCreate,
    db: Session = Depends(get_db)
):
    new_assignment = Assignment(
        assetid=assignment.assetid,
        employeeid=assignment.employeeid,
        assigneddate=assignment.assigneddate,
        expectedreturndate=assignment.expectedreturndate,
        actualreturndate=assignment.actualreturndate,
        assignmentstatus=assignment.assignmentstatus,
        location=assignment.location,
        usagetype=assignment.usagetype,
        conditionatassign=assignment.conditionatassign,
        approvedby=assignment.approvedby,
        assignedby=assignment.assignedby,
        remarks=assignment.remarks
    )

    db.add(new_assignment)
    db.commit()
    db.refresh(new_assignment)

    return {
        "message": "Assignment created successfully",
        "assignmentid": new_assignment.assignmentid
    }