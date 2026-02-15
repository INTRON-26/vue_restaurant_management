from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.menu_item import MenuItem
from app.schemas.menu_item import MenuItemCreate, MenuItemUpdate


def list_menu_items(db: Session) -> List[MenuItem]:
    return db.query(MenuItem).order_by(MenuItem.created_at.desc()).all()


def get_menu_item(db: Session, item_id: int) -> Optional[MenuItem]:
    return db.query(MenuItem).filter(MenuItem.id == item_id).first()


def create_menu_item(db: Session, item_in: MenuItemCreate) -> MenuItem:
    db_item = MenuItem(**item_in.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update_menu_item(db: Session, item: MenuItem, item_in: MenuItemUpdate) -> MenuItem:
    data = item_in.dict(exclude_unset=True)
    for key, value in data.items():
        setattr(item, key, value)
    db.commit()
    db.refresh(item)
    return item


def delete_menu_item(db: Session, item: MenuItem) -> None:
    db.delete(item)
    db.commit()
