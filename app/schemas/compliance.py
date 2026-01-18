from pydantic import BaseModel
from typing import Optional


class ComplianceBase(BaseModel):
    assetid: int
    complianttype: str
    recommendaction: Optional[str] = None
    notes: Optional[str] = None


class ComplianceCreate(ComplianceBase):
    pass


class ComplianceUpdate(BaseModel):
    complianttype: Optional[str]
    recommendaction: Optional[str]
    notes: Optional[str]

    class Config:
        orm_mode = True


class ComplianceResponse(ComplianceBase):
    complianceid: int

    class Config:
        orm_mode = True
