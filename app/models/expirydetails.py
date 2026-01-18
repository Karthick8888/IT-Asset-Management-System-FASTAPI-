from sqlalchemy import Column, Integer, Date, Enum, String, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from app.db.base import Base

class ExpiryDetails(Base):
    __tablename__ = "expirydetails"

    expiredid = Column(Integer, primary_key=True, index=True)
    assetid = Column(Integer, ForeignKey("assets.assetid", ondelete="CASCADE"), nullable=False)

    expireddate = Column(Date, nullable=False)
    daysexpired = Column(Integer, nullable=False)
    expirystatus = Column(Enum("Expired", "Active"), default="Expired")
    approvedby = Column(String(100))

    created_at = Column(TIMESTAMP, server_default=func.now())
