from pydantic import BaseModel
from typing import Optional
from datetime import date
from enum import Enum


class AssetStatus(str, Enum):
    Active = "Active"
    Expired = "Expired"


class compliance_Status(str, Enum):
    Pending_Review = "Pending Review"
    Compliant = "Compliant"
    Non_Compliant="Non-Compliant"


class AssetBase(BaseModel):
    name: str
    category: str
    serialno: str
    brand: Optional[str] = None
    status: Optional[AssetStatus]
    purchasedate: date
    expirydate: Optional[date] = None
    warrentyexpiry: Optional[date] = None
    notes: Optional[str] = None
    compliance_status: Optional[compliance_Status]


class AssetCreate(AssetBase):
    pass


class AssetUpdate(BaseModel):
    name: Optional[str]
    category: Optional[str]
    brand: Optional[str]
    status: Optional[AssetStatus]
    expirydate: Optional[date]
    warrentyexpiry: Optional[date]
    notes: Optional[str]
    compliance_status:Optional[str]

    class Config:
        orm_mode = True


class AssetResponse(AssetBase):
    assetid: int

    class Config:
        orm_mode = True
