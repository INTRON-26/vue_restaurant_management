from pathlib import Path
from typing import List
from uuid import uuid4

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, require_role
from app.crud.menu_item import create_menu_item, delete_menu_item, get_menu_item, list_menu_items, update_menu_item
from app.schemas.menu_item import MenuItemCreate, MenuItemRead, MenuItemUpdate

router = APIRouter(prefix="/menu", tags=["menu"])

UPLOAD_DIR = Path("uploads/menu")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.get("/", response_model=List[MenuItemRead])
def get_menu(db: Session = Depends(get_db)):
    return list_menu_items(db)


@router.post("/", response_model=MenuItemRead, dependencies=[Depends(require_role({"admin", "staff"}))])
def add_menu_item(item_in: MenuItemCreate, db: Session = Depends(get_db)):
    return create_menu_item(db, item_in)


@router.post("/upload", dependencies=[Depends(require_role({"admin", "staff"}))])
def upload_menu_image(file: UploadFile = File(...)):
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid image type")

    extension = Path(file.filename).suffix or ".jpg"
    file_name = f"{uuid4().hex}{extension}"
    target = UPLOAD_DIR / file_name
    with target.open("wb") as buffer:
        buffer.write(file.file.read())

    return {"url": f"/uploads/menu/{file_name}"}


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
