from pydantic import BaseModel, EmailStr
from typing import Optional

class EmployeeBase(BaseModel):
    fullname: str
    email: EmailStr
    department: Optional[str] = None
    role: Optional[str] = None


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(BaseModel):
    fullname: Optional[str]
    department: Optional[str]
    role: Optional[str]

    class Config:
        orm_mode = True



class EmployeeResponse(EmployeeBase):
    employeeid: int

    class Config:
        orm_mode = True
