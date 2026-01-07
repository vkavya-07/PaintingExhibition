from fastapi import APIRouter, Depends, HTTPException, Header, Query
from typing import List, Optional
from sqlmodel import Session
from app.db import get_session
from app.models import Painting, PaintingCreate, PaintingRead, PaintingUpdate, PaintingSale
from app.api.paintings import crud
from datetime import datetime

router = APIRouter(prefix="/paintings", tags=["paintings"])

def require_role(role: str, x_role: Optional[str] = Header(None)):
    if x_role != role:
        raise HTTPException(status_code=403, detail="Forbidden")

@router.get("/", response_model=List[PaintingRead])
def list_paintings(x_role: Optional[str] = Header(None), session: Session = Depends(get_session)):
    if x_role != "user" and x_role != "admin":
        raise HTTPException(status_code=403, detail="Forbidden")
    return crud.get_all_paintings(session)

@router.post("/", response_model=PaintingRead)
def add_painting(p: PaintingCreate, x_role: Optional[str] = Header(None), session: Session = Depends(get_session)):
    if x_role != "admin":
        raise HTTPException(status_code=403, detail="Forbidden")
    # Create Painting from the create schema in a pydantic/SQLModel-compatible way
    painting = Painting.model_validate(p.model_dump())
    return crud.create_painting(session, painting)

@router.put("/{painting_id}", response_model=PaintingRead)
def put_painting(painting_id: int, p: PaintingCreate, x_role: Optional[str] = Header(None), session: Session = Depends(get_session)):
    if x_role != "admin":
        raise HTTPException(status_code=403, detail="Forbidden")
    painting = crud.get_painting(session, painting_id)
    if not painting:
        raise HTTPException(status_code=404, detail="Not found")
    data = p.model_dump()
    return crud.update_painting(session, painting, data)

@router.patch("/{painting_id}", response_model=PaintingRead)
def patch_painting(painting_id: int, p: PaintingUpdate, x_role: Optional[str] = Header(None), session: Session = Depends(get_session)):
    if x_role != "admin":
        raise HTTPException(status_code=403, detail="Forbidden")
    painting = crud.get_painting(session, painting_id)
    if not painting:
        raise HTTPException(status_code=404, detail="Not found")
    data = p.model_dump(exclude_unset=True)
    return crud.update_painting(session, painting, data)

@router.patch("/{painting_id}/buy", response_model=PaintingRead)
def buy_painting(painting_id: int, sale: PaintingSale, x_role: Optional[str] = Header(None), session: Session = Depends(get_session)):
    if x_role != "user":
        raise HTTPException(status_code=403, detail="Forbidden")
    painting = crud.get_painting(session, painting_id)
    if not painting:
        raise HTTPException(status_code=404, detail="Not found")
    if not painting.isAvailableForSale:
        raise HTTPException(status_code=400, detail="Painting not available for sale")
    data = {"soldTo": sale.soldTo, "soldDate": sale.soldDate, "isAvailableForSale": False}
    return crud.update_painting(session, painting, data)

@router.get("/sold", response_model=List[PaintingRead])
def sold_paintings(createdBy: Optional[str] = Query(None), min_price: Optional[float] = Query(None), max_price: Optional[float] = Query(None), sold_from: Optional[datetime] = Query(None), sold_to: Optional[datetime] = Query(None), sort_by: Optional[str] = Query(None), x_role: Optional[str] = Header(None), session: Session = Depends(get_session)):
    if x_role != "admin":
        raise HTTPException(status_code=403, detail="Forbidden")
    return crud.get_sold_paintings(session, createdBy, min_price, max_price, sold_from, sold_to, sort_by)