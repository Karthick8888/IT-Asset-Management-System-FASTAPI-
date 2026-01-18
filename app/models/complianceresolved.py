from sqlalchemy import Column, Integer, String, Date, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from db.base import Base

class ComplianceResolved(Base):
    __tablename__ = "complianceresolved"

    resolvedid = Column(Integer, primary_key=True, index=True)
    complianceid = Column(Integer, ForeignKey("compliance.complianceid", ondelete="CASCADE"), nullable=False)
    assetid = Column(Integer, ForeignKey("assets.assetid", ondelete="CASCADE"), nullable=False)

    checkby = Column(String(100), nullable=False)
    checkeddate = Column(Date, nullable=False)

    created_at = Column(TIMESTAMP, server_default=func.now())
