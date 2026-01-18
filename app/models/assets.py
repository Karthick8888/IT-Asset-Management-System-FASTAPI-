from sqlalchemy import Column, Integer, String, Date, Enum, Text, TIMESTAMP
from sqlalchemy.sql import func
from app.db.base import Base

class Asset(Base):
    __tablename__ = "assets"

    assetid = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    category = Column(String(50), nullable=False)
    serialno = Column(String(100), unique=True, nullable=False)
    brand = Column(String(50))
    status = Column(Enum("Active", "Expired"), default="Active")
    purchasedate = Column(Date, nullable=False)
    expirydate = Column(Date)
    warrentyexpiry = Column(Date)
    notes = Column(Text)
    compliance_status = Column(Enum("Pending Review", "Compliant","Non-Compliant"), default="Pending Review")

    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(
        TIMESTAMP,
        server_default=func.now(),
        onupdate=func.now()
    )
