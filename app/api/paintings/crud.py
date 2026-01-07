import logging
from typing import List, Optional
from sqlmodel import select, Session
from app.models import Painting
from datetime import datetime

logger = logging.getLogger("paintingexhibition.crud")

def get_all_paintings(session: Session) -> List[Painting]:
    stmt = select(Painting)
    try:
        res = session.exec(stmt).all()
        logger.debug(f"Fetched {len(res)} paintings from DB")
        return res
    except Exception as e:
        logger.exception("Error fetching all paintings")
        raise

def create_painting(session: Session, painting: Painting) -> Painting:
    try:
        session.add(painting)
        session.commit()
        session.refresh(painting)
        logger.info(f"Created painting id={painting.id} by={painting.createdBy}")
        return painting
    except Exception:
        logger.exception("Error creating painting")
        session.rollback()
        raise

def get_painting(session: Session, painting_id: int) -> Optional[Painting]:
    try:
        p = session.get(Painting, painting_id)
        logger.debug(f"get_painting({painting_id}) -> {p}")
        return p
    except Exception:
        logger.exception("Error retrieving painting %s", painting_id)
        raise

def update_painting(session: Session, painting: Painting, data: dict) -> Painting:
    try:
        for k, v in data.items():
            setattr(painting, k, v)
        session.add(painting)
        session.commit()
        session.refresh(painting)
        logger.info(f"Updated painting id={painting.id} fields={list(data.keys())}")
        return painting
    except Exception:
        logger.exception("Error updating painting %s", painting.id)
        session.rollback()
        raise

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
    try:
        res = session.exec(stmt).all()
        logger.debug(f"Fetched {len(res)} sold paintings from DB")
        return res
    except Exception:
        logger.exception("Error fetching sold paintings")
        raise