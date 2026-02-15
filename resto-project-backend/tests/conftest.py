import os
import sys
import tempfile
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

sys.path.append(str(Path(__file__).resolve().parents[1]))

os.environ.setdefault("DATABASE_URL", f"sqlite:///{tempfile.mkdtemp()}/test.db")

from app.api.deps import get_db
from app.core.config import settings
from app.crud.menu_item import create_menu_item
from app.crud.user import create_user
from app.db.base import Base
from app.db.session import SessionLocal, engine
from app.main import create_app
from app.schemas.menu_item import MenuItemCreate
from app.schemas.user import UserCreate


def override_get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client():
    app = create_app()
    app.dependency_overrides[get_db] = override_get_db

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        create_user(
            db,
            UserCreate(name="Admin", email="admin@example.com", password="Admin123!"),
            role="admin",
        )
        create_user(
            db,
            UserCreate(name="Staff", email="staff@example.com", password="Staff123!"),
            role="staff",
        )
        create_user(
            db,
            UserCreate(name="Customer", email="customer@example.com", password="Cust123!"),
            role="customer",
        )
        create_menu_item(
            db,
            MenuItemCreate(name="Test Burger", description="Test", price=9.99),
        )
    finally:
        db.close()

    return TestClient(app)
