from sqlalchemy import Column, Integer, String, Date, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from db.base import Base

class Renewal(Base):
    __tablename__ = "renewal"

    renewalid = Column(Integer, primary_key=True, index=True)
    assetid = Column(Integer, ForeignKey("assets.assetid", ondelete="CASCADE"), nullable=False)
    expiryid = Column(Integer, ForeignKey("expirydetails.expiredid", ondelete="CASCADE"), nullable=False)

    renewaltype = Column(String(100), nullable=False)
    reneweddate = Column(Date, nullable=False)

    created_at = Column(TIMESTAMP, server_default=func.now())
