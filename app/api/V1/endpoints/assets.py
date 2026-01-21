from fastapi import APIRouter, Depends, HTTPException, Query,status
from sqlalchemy.orm import Session
from sqlalchemy import cast, String
from typing import List, Optional

from app.db.session import get_db
from app.models.assets import Asset
from app.schemas.assets import AssetCreate, AssetResponse, AssetUpdate,AssetPatch

router = APIRouter()

# 🔹 Create Asset
@router.post("/", response_model=AssetResponse)
def create_asset(data: AssetCreate, db: Session = Depends(get_db)):
    asset = Asset(
        name=data.name,
        category=data.category,
        serialno=data.serialno,
        brand=data.brand,
        status=data.status.value,
        purchasedate=data.purchasedate,
        expirydate=data.expirydate,
        warrentyexpiry=data.warrentyexpiry,
        notes=data.notes,
        compliance_status=data.compliance_status
    )
    db.add(asset)
    db.commit()
    db.refresh(asset)
    return asset


# 🔹 Get All Assets
@router.get("/", response_model=List[AssetResponse])
def get_assets(db: Session = Depends(get_db)):
    return db.query(Asset).all()


# 🔍 SEARCH — MUST BE ABOVE /{assetid}
@router.get("/searchbyInputs")
def search_assets(
    q: Optional[str] = Query(None, min_length=1),
    db: Session = Depends(get_db)
):
    query_db = db.query(Asset)

    if q:
        search = f"%{q}%"
        query_db = query_db.filter(
            Asset.name.ilike(search) |
            Asset.category.ilike(search) |
            Asset.serialno.ilike(search) |
            cast(Asset.status, String).ilike(search)
        )

    return query_db.all()


# 🔹 Get Asset by Serialno
@router.get("/assetbySerialno/{serialno}", response_model=AssetResponse)
def get_assetbySerialno(serialno: str, db: Session = Depends(get_db)):
    asset = db.query(Asset).filter(Asset.serialno == serialno).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return asset


# 🔹 Get Asset by Category and Status
@router.get("/assetbycatANDstat/{cat}/{stat}", response_model=List[AssetResponse])
def get_assetby_cat_and_stat(cat: str, stat: str, db: Session = Depends(get_db)):
    assets = db.query(Asset).filter(
        Asset.category == cat,
        Asset.status == stat
    ).all()
    if not assets:
        raise HTTPException(status_code=404, detail="Asset not found")
    return assets


# 🔹 Get Asset by Category
@router.get("/assetbycat/{cat}", response_model=List[AssetResponse])
def get_assetbycat(cat: str, db: Session = Depends(get_db)):
    assets = db.query(Asset).filter(Asset.category == cat).all()
    if not assets:
        raise HTTPException(status_code=404, detail="Asset not found")
    return assets


# 🔹 Get Asset by Status
@router.get("/assetbystat/{stat}", response_model=List[AssetResponse])
def get_assetbystat(stat: str, db: Session = Depends(get_db)):
    assets = db.query(Asset).filter(Asset.status == stat).all()
    if not assets:
        raise HTTPException(status_code=404, detail="Asset not found")
    return assets


# 🔹 Get Asset by ID (KEEP LAST)
@router.get("/{assetid:int}", response_model=AssetResponse)
def get_asset(assetid: int, db: Session = Depends(get_db)):
    asset = db.query(Asset).filter(Asset.assetid == assetid).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return asset


@router.delete("/{asset_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_asset(asset_id: int, db: Session = Depends(get_db)):
    asset = db.query(Asset).filter(Asset.assetid == asset_id).first()

    if not asset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asset not found"
        )

    db.delete(asset)
    db.commit()

    return None


@router.patch("/{asset_id}")
def patch_asset(
    asset_id: int,
    asset_data: AssetPatch,
    db: Session = Depends(get_db)
):
    asset = db.query(Asset).filter(Asset.assetid == asset_id).first()

    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")

    update_data = asset_data.dict(exclude_unset=True)

    for field, value in update_data.items():
        setattr(asset, field, value)

    db.commit()
    db.refresh(asset)

    return {
        "message": "Asset updated successfully",
        "assetid": asset.assetid
    }