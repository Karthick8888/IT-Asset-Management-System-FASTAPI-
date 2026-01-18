from sqlalchemy import Column, Integer, String, Text, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from app.db.base import Base

class Compliance(Base):
    __tablename__ = "compliance"

    complianceid = Column(Integer, primary_key=True, index=True)
    assetid = Column(Integer, ForeignKey("assets.assetid", ondelete="CASCADE"), nullable=False)
    complianttype = Column(String(100), nullable=False)
    recommendaction = Column(Text)
    notes = Column(Text)

    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(
        TIMESTAMP,
        server_default=func.now(),
        onupdate=func.now()
    )
