from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.reservation import Reservation
from app.schemas.reservation import ReservationCreate, ReservationUpdate


def create_reservation(
    db: Session, reservation_in: ReservationCreate, user_id: Optional[int]
) -> Reservation:
    db_item = Reservation(**reservation_in.dict(), user_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def list_reservations(db: Session) -> List[Reservation]:
    return db.query(Reservation).order_by(Reservation.created_at.desc()).all()


def list_reservations_for_user(db: Session, user_id: int) -> List[Reservation]:
    return (
        db.query(Reservation)
        .filter(Reservation.user_id == user_id)
        .order_by(Reservation.created_at.desc())
        .all()
    )


def get_reservation(db: Session, reservation_id: int) -> Optional[Reservation]:
    return db.query(Reservation).filter(Reservation.id == reservation_id).first()


def update_reservation_status(
    db: Session, reservation: Reservation, update_in: ReservationUpdate
) -> Reservation:
    reservation.status = update_in.status
    db.commit()
    db.refresh(reservation)
    return reservation
