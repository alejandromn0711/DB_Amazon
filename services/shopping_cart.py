from typing import List

from fastapi import APIRouter

from crud.shopping_cart import ShoppingCartData, ShoppingCartCRUD

router = APIRouter()
crud = ShoppingCartCRUD()

@router.post("/shopping_cart/create", response_model=int)
def create_shopping_cart(data: ShoppingCartData):
    return crud.create(data)

@router.put("/shopping_cart/update/{shopping_cart_id}")
def update_shopping_cart(shopping_cart_id: int, data: ShoppingCartData):
    return crud.update(shopping_cart_id, data)

@router.delete("/shopping_cart/delete/{shopping_cart_id}")
def delete_shopping_cart(shopping_cart_id: int):
    return crud.delete(shopping_cart_id)

@router.get("/shopping_cart/get_by_id/{shopping_cart_id}", response_model=ShoppingCartData)
def get_shopping_cart_by_id(shopping_cart_id: int):
    return crud.get_by_id(shopping_cart_id)

@router.get("/shopping_cart/get_all", response_model=List[ShoppingCartData])
def get_all_shopping_carts():
    return crud.get_all()

# Puedes agregar rutas adicionales según sea necesario, por ejemplo:
# @router.get("/shopping_cart/customer/{customer_id}", response_model=List[ShoppingCartData])
# def get_shopping_carts_by_customer(customer_id: int):
#     return crud.get_shopping_carts_by_customer(customer_id)