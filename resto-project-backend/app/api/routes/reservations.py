from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user_optional, get_db, require_role
from app.crud.reservation import create_reservation, list_reservations, list_reservations_for_user
from app.schemas.reservation import ReservationCreate, ReservationRead

router = APIRouter(prefix="/reservations", tags=["reservations"])


@router.post("/", response_model=ReservationRead)
def make_reservation(
    reservation_in: ReservationCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user_optional),
):
    if current_user is None:
        if not reservation_in.guest_name or not reservation_in.guest_email:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Guest name and email are required for guest reservations",
            )
        user_id = None
    else:
        user_id = current_user.id
    return create_reservation(db, reservation_in, user_id=user_id)


@router.get("/", response_model=List[ReservationRead], dependencies=[Depends(require_role({"admin", "staff"}))])
def list_all_reservations(db: Session = Depends(get_db)):
    return list_reservations(db)


@router.get("/me", response_model=List[ReservationRead])
def list_my_reservations(db: Session = Depends(get_db), current_user=Depends(require_role({"customer"}))):
    return list_reservations_for_user(db, current_user.id)
