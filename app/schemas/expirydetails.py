from enum import Enum
from pydantic import BaseModel
from datetime import date
from typing import Optional

class ExpiryStatus(str, Enum):
    Expired = "Expired"
    Active = "Active"




class ExpiryDetailsBase(BaseModel):
    assetid: int
    expireddate: date
    daysexpired: int
    expirystatus: ExpiryStatus = ExpiryStatus.Expired
    approvedby: Optional[str] = None


class ExpiryDetailsCreate(ExpiryDetailsBase):
    pass

class ExpiryDetailsResponse(BaseModel):
    expiryid: int
    assetid: int
    assetname: str            # ✅ ADD THIS
    expireddate: date
    expirystatus: str
    daysremaining: Optional[int]

    class Config:
        orm_mode = True
