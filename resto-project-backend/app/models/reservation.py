from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True)
    party_size = Column(Integer, nullable=False)
    reserved_for = Column(DateTime(timezone=True), nullable=False)
    guest_name = Column(String(120), nullable=True)
    guest_email = Column(String(255), nullable=True)
    guest_phone = Column(String(40), nullable=True)
    status = Column(String(50), default="pending", nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="reservations")
