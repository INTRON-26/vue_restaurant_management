from datetime import datetime, timedelta
from datetime import timezone
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.crud.menu_item import create_menu_item
from app.crud.reservation import create_reservation
from app.crud.user import create_user, get_user_by_email
from app.db.session import SessionLocal
from app.models.menu_item import MenuItem
from app.models.reservation import Reservation
from app.models.user import User
from app.schemas.menu_item import MenuItemCreate
from app.schemas.reservation import ReservationCreate
from app.schemas.user import UserCreate


MENU_ITEMS = [
    MenuItemCreate(name="Margherita Pizza", description="Classic tomato and basil", price=10.5),
    MenuItemCreate(name="Chicken Alfredo", description="Creamy pasta with grilled chicken", price=13.75),
    MenuItemCreate(name="Garden Salad", description="Mixed greens with vinaigrette", price=7.25),
    MenuItemCreate(name="Tomato Soup", description="Roasted tomato soup", price=6.0),
    MenuItemCreate(name="Chocolate Cake", description="Rich chocolate slice", price=5.5),
]

GUEST_RESERVATIONS = [
    ReservationCreate(
        party_size=2,
        reserved_for=datetime.now(timezone.utc) + timedelta(days=1, hours=2),
        guest_name="Alex Guest",
        guest_email="guest1@example.com",
        guest_phone="555-0101",
    ),
    ReservationCreate(
        party_size=4,
        reserved_for=datetime.now(timezone.utc) + timedelta(days=2, hours=1),
        guest_name="Jamie Guest",
        guest_email="guest2@example.com",
        guest_phone="555-0102",
    ),
    ReservationCreate(
        party_size=3,
        reserved_for=datetime.now(timezone.utc) + timedelta(days=3, hours=3),
        guest_name="Taylor Guest",
        guest_email="guest3@example.com",
        guest_phone="555-0103",
    ),
]


def seed() -> None:
    db = SessionLocal()
    try:
        has_users = db.query(User).first() is not None
        has_menu = db.query(MenuItem).first() is not None
        has_reservations = db.query(Reservation).first() is not None
        if has_users or has_menu or has_reservations:
            print("Seed skipped: data already exists.")
            return

        if not get_user_by_email(db, "admin@example.com"):
            create_user(
                db,
                UserCreate(name="Admin User", email="admin@example.com", password="Admin123!"),
                role="admin",
            )
        if not get_user_by_email(db, "staff@example.com"):
            create_user(
                db,
                UserCreate(name="Staff User", email="staff@example.com", password="Staff123!"),
                role="staff",
            )

        for item in MENU_ITEMS:
            create_menu_item(db, item)

        for reservation in GUEST_RESERVATIONS:
            create_reservation(db, reservation, user_id=None)

        print("Seed completed.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
