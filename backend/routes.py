from fastapi import APIRouter, HTTPException
from backend.models import Item

router = APIRouter()

@router.get("/health")
def health_check():
    return {"status": "OK"}

@router.post("/items/")
def create_item(item: Item):
    # Here you can insert into DB
    return {"item_id": item.id, "name": item.name, "description": item.description}
