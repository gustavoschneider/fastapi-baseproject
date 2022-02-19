from typing import Optional
from sqlmodel import Field, SQLModel


class ProductBase(SQLModel):
    name: str = Field(index=True)
    description: Optional[str] = Field(default=None)

class Product(ProductBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, nullable=False)

class ProductCreate(ProductBase):
    pass

class ProductRead(ProductBase):
    id: int

class ProductUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None
