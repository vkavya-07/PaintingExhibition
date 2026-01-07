from fastapi import APIRouter, Depends, HTTPException, Header, Query
from typing import List, Optional
from sqlmodel import Session
from app.db import get_session
from app.models import Painting, PaintingCreate, PaintingRead, PaintingUpdate, PaintingSale
from app.api.paintings import crud
from datetime import datetime
import logging

router = APIRouter(prefix="/paintings", tags=["paintings"])

def require_role(role: str, x_role: Optional[str] = Header(None)):
    if x_role != role:
        raise HTTPException(status_code=403, detail="Forbidden")

@router.get("/", response_model=List[PaintingRead], summary="List paintings", description="Return an array of paintings. Roles allowed: user, admin.")
def list_paintings(x_role: Optional[str] = Header(None), session: Session = Depends(get_session)):
    logger = logging.getLogger("paintingexhibition.routes")
    logger.info("List paintings requested by role=%s", x_role)
    if x_role != "user" and x_role != "admin":
        raise HTTPException(status_code=403, detail="Forbidden")
    try:
        paintings = crud.get_all_paintings(session)
        logger.info("Returning %s paintings to role=%s", len(paintings), x_role)
        return paintings
    except Exception as e:
        logger.exception("Failed to list paintings: %s", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.post("/", response_model=PaintingRead, summary="Add a painting", description="Admin-only: create a new painting record.")
def add_painting(p: PaintingCreate, x_role: Optional[str] = Header(None), session: Session = Depends(get_session)):
    if x_role != "admin":
        raise HTTPException(status_code=403, detail="Forbidden")
    # Create Painting from the create schema in a pydantic/SQLModel-compatible way
    painting = Painting.model_validate(p.model_dump())
    return crud.create_painting(session, painting)

@router.put("/{painting_id}", response_model=PaintingRead, summary="Replace painting", description="Admin-only: replace all mutable properties of a painting.")
def put_painting(painting_id: int, p: PaintingCreate, x_role: Optional[str] = Header(None), session: Session = Depends(get_session)):
    if x_role != "admin":
        raise HTTPException(status_code=403, detail="Forbidden")
    painting = crud.get_painting(session, painting_id)
    if not painting:
        raise HTTPException(status_code=404, detail="Not found")
    data = p.model_dump()
    return crud.update_painting(session, painting, data)

@router.patch("/{painting_id}", response_model=PaintingRead, summary="Update painting partially", description="Admin-only: patch provided fields.")
def patch_painting(painting_id: int, p: PaintingUpdate, x_role: Optional[str] = Header(None), session: Session = Depends(get_session)):
    if x_role != "admin":
        raise HTTPException(status_code=403, detail="Forbidden")
    painting = crud.get_painting(session, painting_id)
    if not painting:
        raise HTTPException(status_code=404, detail="Not found")
    data = p.model_dump(exclude_unset=True)
    return crud.update_painting(session, painting, data)

@router.patch("/{painting_id}/buy", response_model=PaintingRead, summary="Buy a painting", description="User-only: mark a painting as sold by setting soldTo and soldDate.")
def buy_painting(painting_id: int, sale: PaintingSale, x_role: Optional[str] = Header(None), session: Session = Depends(get_session)):
    logger = logging.getLogger("paintingexhibition.routes")
    logger.info("Buy painting requested id=%s by role=%s", painting_id, x_role)
    if x_role != "user":
        raise HTTPException(status_code=403, detail="Forbidden")
    painting = crud.get_painting(session, painting_id)
    if not painting:
        raise HTTPException(status_code=404, detail="Not found")
    if not painting.isAvailableForSale:
        raise HTTPException(status_code=400, detail="Painting not available for sale")
    data = {"soldTo": sale.soldTo, "soldDate": sale.soldDate, "isAvailableForSale": False}
    updated = crud.update_painting(session, painting, data)
    logger.info("Painting id=%s sold to=%s", painting_id, sale.soldTo)
    return updated

@router.get("/sold", response_model=List[PaintingRead], summary="List sold paintings", description="Admin-only: return sold paintings; supports filtering and sorting by createdBy, price and soldDate.")
def sold_paintings(createdBy: Optional[str] = Query(None), min_price: Optional[float] = Query(None), max_price: Optional[float] = Query(None), sold_from: Optional[datetime] = Query(None), sold_to: Optional[datetime] = Query(None), sort_by: Optional[str] = Query(None), x_role: Optional[str] = Header(None), session: Session = Depends(get_session)):
    if x_role != "admin":
        raise HTTPException(status_code=403, detail="Forbidden")
    return crud.get_sold_paintings(session, createdBy, min_price, max_price, sold_from, sold_to, sort_by)