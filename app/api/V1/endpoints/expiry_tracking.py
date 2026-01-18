from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.expiry_alerts import ExpiryAlert
from app.models.assets import Asset
from app.schemas.expiry_alerts import ExpiryAlertResponse
from app.models.expirydetails import ExpiryDetails
from app.schemas.expirydetails import ExpiryDetailsResponse

router = APIRouter()


@router.get("/expirysoon", response_model=List[ExpiryAlertResponse])
def get_all_expiry_soon(db: Session = Depends(get_db)):
    rows = (
        db.query(ExpiryAlert, Asset.name)
        .join(Asset, ExpiryAlert.assetid == Asset.assetid)
        .all()
    )

    return [
        {
            "expiredid": alert.expiredid,
            "assetid": alert.assetid,
            "assetname": assetname,   # ✅ explicit
            "expireddate": alert.expireddate,
            "expirystatus": alert.expirystatus,
            "daysexpired": alert.daysexpired,
            "approvedby": alert.approvedby,
        }
        for alert, assetname in rows
    ]



@router.get("/expirydetails", response_model=List[ExpiryDetailsResponse])
def get_all_expiry_details(db: Session = Depends(get_db)):
    rows = (
        db.query(ExpiryDetails, Asset.name)
        .join(Asset, ExpiryDetails.assetid == Asset.assetid)
        .all()
    )

    return [
        {
            "expiryid": detail.expiredid,
            "assetid": detail.assetid,
            "assetname": asset_name,   # ✅ FORCE INCLUDE
            "expireddate": detail.expireddate,
            "expirystatus": detail.expirystatus,
            "daysremaining": detail.daysexpired,
        }
        for detail, asset_name in rows
    ]



