from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.assets import Asset
from app.models.expiry_alerts import ExpiryAlert
from sqlalchemy import desc


router = APIRouter()

@router.get("/")
def asset_dashboard(db: Session = Depends(get_db)):
    total_assets = db.query(Asset).count()
    active_assets = db.query(Asset).filter(Asset.status == "Active").count()
    nearly_expired = db.query(ExpiryAlert).count()
    expired_assets = db.query(Asset).filter(Asset.status == "Expired").count()
    Pending_Review = db.query(Asset).filter(Asset.compliance_status == "Pending Review").count()
    Non_Compliant = db.query(Asset).filter(Asset.compliance_status == "Non-Compliant").count()
    Compliant = db.query(Asset).filter(Asset.compliance_status == "Compliant").count()
    tenassets = db.query(Asset).order_by(desc(Asset.created_at)).limit(10).all()
    

    return {
        "total_assets": total_assets,
        "active_assets": active_assets,
        "nearly_expired": nearly_expired,
        "expired_assets": expired_assets,
        "Pending_Review":Pending_Review,
        "Non_Compliant":Non_Compliant,
        "Compliant":Compliant,
        "tenassets":tenassets

    }
