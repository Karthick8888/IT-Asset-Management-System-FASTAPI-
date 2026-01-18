
from enum import Enum
from typing import Optional

class AlertStatus(str, Enum):
    Pending = "Pending"
    Notified = "Notified"
    Resolved = "Resolved"

from pydantic import BaseModel
from datetime import date

class ExpiryAlertBase(BaseModel):
    assetid: int
    expirydate: date
    days_remaining: int
    alert_status: AlertStatus = AlertStatus.Pending



class ExpiryAlertCreate(ExpiryAlertBase):
    pass




class ExpiryAlertUpdate(BaseModel):
    alert_status: Optional[AlertStatus]

    class Config:
        orm_mode = True

class ExpiryAlertResponse(BaseModel):
    expiredid: int
    assetid: int
    assetname: str
    expireddate: date
    expirystatus: str
    daysexpired: int
    Objectapprovedby: Optional[str]

    class Config:
        orm_mode = True

