from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr


class ReservationBase(BaseModel):
    party_size: int
    reserved_for: datetime
    guest_name: Optional[str] = None
    guest_email: Optional[EmailStr] = None
    guest_phone: Optional[str] = None


class ReservationCreate(ReservationBase):
    pass


class ReservationUpdate(BaseModel):
    status: str


class ReservationRead(ReservationBase):
    id: int
    status: str
    user_id: Optional[int] = None
    created_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)
