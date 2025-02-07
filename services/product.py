from typing import List

from fastapi import APIRouter

from crud.product import ProductData, ProductCRUD  # Import your Product classes

router = APIRouter()
crud = ProductCRUD()

@router.post("/product/create", response_model=int)
def create_product(data: ProductData):
    return crud.create(data)

@router.put("/product/update/{product_id}")
def update_product(product_id: int, data: ProductData):
    return crud.update(product_id, data)

@router.delete("/product/delete/{product_id}")
def delete_product(product_id: int):
    return crud.delete(product_id)

@router.get("/product/get_by_id/{product_id}", response_model=ProductData) # Response model added
def get_product_by_id(product_id: int):
    return crud.get_by_id(product_id)

@router.get("/product/get_all", response_model=List[ProductData]) # Response model added
def get_all_products():
    return crud.get_all()

@router.get("/product/get_by_name/{product_name}", response_model=List[ProductData]) # Response model added
def get_product_by_name(product_name: str):
    return crud.get_by_name(product_name)

@router.get("/product/get_by_category/{category_id}", response_model=List[ProductData]) # Response model added
def get_product_by_category(category_id: int):
    return crud.get_by_category(category_id)