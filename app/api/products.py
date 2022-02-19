import logging

from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi_versioning import version

from sqlmodel import Session, select, or_, func

from ..database import get_session
from ..models.products import Product, ProductRead, ProductCreate, ProductUpdate

router = APIRouter(
    prefix = '/products',
    tags=["Products"]
)
logger = logging.getLogger('baseproject')

@router.get('', response_model=List[ProductRead])
@version(1, 0)
async def get_all_products(
    *,
    session: Session = Depends(get_session),
    offset:int = 0,
    limit:int = Query(default=100, lte=100),
    query_string: str | None = Query(None, max_lenght=100)
):
    if query_string:
        query = select(Product).where(
            or_(
                func.lower(Product.name).contains(query_string.lower()),
                func.lower(Product.description).contains(query_string.lower())
            ))
    else:
        query = select(Product)

    result = await session.execute(query.offset(offset).limit(limit))
    
    products = result.scalars().all()
    return products


@router.get('/{product_id}', response_model=ProductRead)
@version(1, 0)
async def get_one_product(
    *,
    session: Session = Depends(get_session),
    product_id: int
):
    product = await session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail='Product not found')
    return product


@router.post('', response_model=ProductRead, status_code=201)
@version(1, 0)
async def create_product(
    *,
    session: Session = Depends(get_session),
    product: ProductCreate
):
    """Create a new Product

    Returns:
    ProductRead: Product created
    """

    db_product = Product.from_orm(product)
    session.add(db_product)
    await session.commit()
    await session.refresh(db_product)
    return db_product


@router.patch('/{product_id}', response_model=ProductRead)
@version(1, 0)
async def update_product(
    *,
    session: Session = Depends(get_session),
    product_id: int,
    product: ProductUpdate
):
    db_product = await session.get(Product, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail='Product not found')

    product_data = product.dict(exclude_unset=True)
    for key, value in product_data.items():
        setattr(db_product, key, value)

    session.add(db_product)
    await session.commit()
    await session.refresh(db_product)
    return db_product


@router.delete('/{product_id}')
async def delete_product(
    *,
    session: Session = Depends(get_session),
    product_id: int
):
    product = await session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail='Product not found')

    await session.delete(product)
    await session.commit()
    return {'ok': True}
