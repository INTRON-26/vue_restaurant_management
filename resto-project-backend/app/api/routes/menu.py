from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, require_role
from app.crud.menu_item import create_menu_item, delete_menu_item, get_menu_item, list_menu_items, update_menu_item
from app.schemas.menu_item import MenuItemCreate, MenuItemRead, MenuItemUpdate

router = APIRouter(prefix="/menu", tags=["menu"])


@router.get("/", response_model=List[MenuItemRead])
def get_menu(db: Session = Depends(get_db)):
    return list_menu_items(db)


@router.post("/", response_model=MenuItemRead, dependencies=[Depends(require_role({"admin", "staff"}))])
def add_menu_item(item_in: MenuItemCreate, db: Session = Depends(get_db)):
    return create_menu_item(db, item_in)


@router.put("/{item_id}", response_model=MenuItemRead, dependencies=[Depends(require_role({"admin", "staff"}))])
def update_item(item_id: int, item_in: MenuItemUpdate, db: Session = Depends(get_db)):
    item = get_menu_item(db, item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menu item not found")
    return update_menu_item(db, item, item_in)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_role({"admin", "staff"}))])
def remove_item(item_id: int, db: Session = Depends(get_db)):
    item = get_menu_item(db, item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menu item not found")
    delete_menu_item(db, item)
