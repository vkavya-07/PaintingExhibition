from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime, timezone

def now_utc():
    return datetime.now(timezone.utc)

class Painting(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    createdDate: datetime = Field(default_factory=now_utc)
    createdBy: str
    size: str
    isAvailableForSale: bool = True
    price: float
    soldTo: Optional[str] = None
    soldDate: Optional[datetime] = None

class PaintingCreate(SQLModel):
    createdBy: str
    size: str
    isAvailableForSale: bool = True
    price: float

class PaintingRead(SQLModel):
    id: int
    createdDate: datetime
    createdBy: str
    size: str
    isAvailableForSale: bool
    price: float
    soldTo: Optional[str]
    soldDate: Optional[datetime]

class PaintingUpdate(SQLModel):
    createdBy: Optional[str] = None
    size: Optional[str] = None
    isAvailableForSale: Optional[bool] = None
    price: Optional[float] = None
    soldTo: Optional[str] = None
    soldDate: Optional[datetime] = None

class PaintingSale(SQLModel):
    soldTo: str
    soldDate: datetime