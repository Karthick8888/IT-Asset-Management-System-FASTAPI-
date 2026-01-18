from pydantic import BaseModel
from datetime import date

class ComplianceResolvedBase(BaseModel):
    complianceid: int
    assetid: int
    checkby: str
    checkeddate: date


class ComplianceResolvedCreate(ComplianceResolvedBase):
    pass


class ComplianceResolvedResponse(ComplianceResolvedBase):
    resolvedid: int

    class Config:
        orm_mode = True
