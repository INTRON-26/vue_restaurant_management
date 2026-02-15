from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user_optional, get_db, require_role
from app.crud.reservation import (
    create_reservation,
    get_reservation,
    list_reservations,
    list_reservations_for_user,
    update_reservation_status,
)
from app.schemas.reservation import ReservationCreate, ReservationRead, ReservationUpdate

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


@router.patch("/{reservation_id}/cancel", response_model=ReservationRead)
def cancel_my_reservation(
    reservation_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_role({"customer"})),
):
    reservation = get_reservation(db, reservation_id)
    if not reservation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reservation not found")
    if reservation.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed to cancel")
    if reservation.status == "cancelled":
        return reservation
    return update_reservation_status(db, reservation, ReservationUpdate(status="cancelled"))


@router.patch(
    "/{reservation_id}/status",
    response_model=ReservationRead,
    dependencies=[Depends(require_role({"admin", "staff"}))],
)
def set_reservation_status(
    reservation_id: int,
    payload: ReservationUpdate,
    db: Session = Depends(get_db),
):
    allowed = {"pending", "confirmed", "cancelled"}
    if payload.status not in allowed:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Status must be one of: {', '.join(sorted(allowed))}",
        )

    reservation = get_reservation(db, reservation_id)
    if not reservation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reservation not found")
    return update_reservation_status(db, reservation, payload)
