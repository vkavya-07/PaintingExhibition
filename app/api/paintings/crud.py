from typing import List, Optional
from sqlmodel import select, Session
from app.models import Painting
from datetime import datetime

def get_all_paintings(session: Session) -> List[Painting]:
    stmt = select(Painting)
    return session.exec(stmt).all()

def create_painting(session: Session, painting: Painting) -> Painting:
    session.add(painting)
    session.commit()
    session.refresh(painting)
    return painting

def get_painting(session: Session, painting_id: int) -> Optional[Painting]:
    return session.get(Painting, painting_id)

def update_painting(session: Session, painting: Painting, data: dict) -> Painting:
    for k, v in data.items():
        setattr(painting, k, v)
    session.add(painting)
    session.commit()
    session.refresh(painting)
    return painting

def get_sold_paintings(session: Session, createdBy: Optional[str] = None, min_price: Optional[float] = None, max_price: Optional[float] = None, sold_from: Optional[datetime] = None, sold_to: Optional[datetime] = None, sort_by: Optional[str] = None) -> List[Painting]:
    stmt = select(Painting).where(Painting.soldTo != None)
    if createdBy:
        stmt = stmt.where(Painting.createdBy == createdBy)
    if min_price is not None:
        stmt = stmt.where(Painting.price >= min_price)
    if max_price is not None:
        stmt = stmt.where(Painting.price <= max_price)
    if sold_from is not None:
        stmt = stmt.where(Painting.soldDate >= sold_from)
    if sold_to is not None:
        stmt = stmt.where(Painting.soldDate <= sold_to)
    if sort_by in ("createdBy", "price", "soldDate"):
        stmt = stmt.order_by(getattr(Painting, sort_by))
    return session.exec(stmt).all()