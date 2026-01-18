from sqlalchemy import (
    Column, Integer, Date, Enum, String, Text, ForeignKey, TIMESTAMP
)
from sqlalchemy.sql import func
from app.db.base import Base

class Assignment(Base):
    __tablename__ = "assignments"

    assignmentid = Column(Integer, primary_key=True, index=True)

    assetid = Column(Integer, ForeignKey("assets.assetid", ondelete="CASCADE"), nullable=False)
    employeeid = Column(Integer, ForeignKey("employees.employeeid", ondelete="CASCADE"), nullable=False)

    assigneddate = Column(Date, nullable=False)
    expectedreturndate = Column(Date)
    actualreturndate = Column(Date)

    assignmentstatus = Column(
        Enum("Assigned", "Returned", "Lost", "Damaged"),
        default="Assigned"
    )

    location = Column(String(100))
    usagetype = Column(Enum("Permanent", "Temporary"))
    conditionatassign = Column(Enum("New", "Good", "Fair"))

    approvedby = Column(String(100))
    assignedby = Column(String(100))
    remarks = Column(Text)

    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(
        TIMESTAMP,
        server_default=func.now(),
        onupdate=func.now()
    )
