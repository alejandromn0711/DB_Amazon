from typing import List

from fastapi import APIRouter

from crud.product import ProductData, ProductCRUD  # Import your Product classes

router = APIRouter()
crud = ProductCRUD()

@router.post("/product/create", response_model=int)
def create_product(data: ProductData):
    """Creates a new product."""
    return crud.create(data)

@router.put("/product/update/{product_id}")
def update_product(product_id: int, data: ProductData):
    """Updates an existing product."""
    return crud.update(product_id, data)

@router.delete("/product/delete/{product_id}")
def delete_product(product_id: int):
    """Deletes a product."""
    return crud.delete(product_id)

@router.get("/product/get_by_id/{product_id}", response_model=ProductData)
def get_product_by_id(product_id: int):
    """Gets a product by ID."""
    return crud.get_by_id(product_id)

@router.get("/product/get_all", response_model=List[ProductData])
def get_all_products():
    """Gets all products."""
    return crud.get_all()

@router.get("/product/get_by_name/{product_name}", response_model=List[ProductData])
def get_product_by_name(product_name: str):
    """Gets products by name."""
    return crud.get_by_name(product_name)

@router.get("/product/get_by_category/{category_id}", response_model=List[ProductData])
def get_product_by_category(category_id: int):
    """Gets products by category."""
    return crud.get_by_category(category_id)