from enum import Enum

from pydantic import BaseModel
from typing import Optional
from datetime import date

class AssignmentStatus(str, Enum):
    Assigned = "Assigned"
    Returned = "Returned"
    Lost = "Lost"
    Damaged = "Damaged"

class UsageType(str, Enum):
    Permanent = "Permanent"
    Temporary = "Temporary"

class AssetCondition(str, Enum):
    New = "New"
    Good = "Good"
    Fair = "Fair"




class AssignmentBase(BaseModel):
    assetid: int
    employeeid: int
    assigneddate: date
    expectedreturndate: Optional[date] = None
    actualreturndate: Optional[date] = None
    assignmentstatus: AssignmentStatus = AssignmentStatus.Assigned
    location: Optional[str] = None
    usagetype: Optional[UsageType] = None
    conditionatassign: Optional[AssetCondition] = None
    approvedby: Optional[str] = None
    assignedby: Optional[str] = None
    remarks: Optional[str] = None


class AssignmentCreate(AssignmentBase):
    pass


class AssignmentUpdate(BaseModel):
    expectedreturndate: Optional[date]
    actualreturndate: Optional[date]
    assignmentstatus: Optional[AssignmentStatus]
    location: Optional[str]
    usagetype: Optional[UsageType]
    conditionatassign: Optional[AssetCondition]
    approvedby: Optional[str]
    remarks: Optional[str]

    class Config:
        orm_mode = True


class AssignmentResponse(AssignmentBase):
    assignmentid: int
    employeename:str
    assetname:str

    class Config:
        orm_mode = True
