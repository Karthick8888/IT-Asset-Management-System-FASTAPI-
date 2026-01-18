from sqlalchemy import Column, Integer, Date, Enum, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from app.db.base import Base

class ExpiryAlert(Base):
    __tablename__ = "expiry_alerts"

    alertid = Column(Integer, primary_key=True, index=True)
    assetid = Column(Integer, ForeignKey("assets.assetid", ondelete="CASCADE"), nullable=False)

    expirydate = Column(Date, nullable=False)
    days_remaining = Column(Integer, nullable=False)

    alert_status = Column(
        Enum("Pending", "Notified", "Resolved"),
        default="Pending"
    )

    created_at = Column(TIMESTAMP, server_default=func.now())
