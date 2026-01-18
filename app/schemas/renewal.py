from pydantic import BaseModel
from datetime import date

class RenewalBase(BaseModel):
    assetid: int
    expiryid: int
    renewaltype: str
    reneweddate: date


class RenewalCreate(RenewalBase):
    pass


class RenewalResponse(RenewalBase):
    renewalid: int

    class Config:
        orm_mode = True
