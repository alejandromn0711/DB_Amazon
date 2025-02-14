from typing import List

from fastapi import APIRouter

from crud.shopping_cart import ShoppingCartData, ShoppingCartCRUD

router = APIRouter()
crud = ShoppingCartCRUD()

@router.post("/shopping_cart/create", response_model=int)
def create_shopping_cart(data: ShoppingCartData):
    """Creates a new shopping cart."""
    return crud.create(data)

@router.put("/shopping_cart/update/{shopping_cart_id}")
def update_shopping_cart(shopping_cart_id: int, data: ShoppingCartData):
    """Updates an existing shopping cart."""
    return crud.update(shopping_cart_id, data)

@router.delete("/shopping_cart/delete/{shopping_cart_id}")
def delete_shopping_cart(shopping_cart_id: int):
    """Deletes a shopping cart."""
    return crud.delete(shopping_cart_id)

@router.get("/shopping_cart/get_by_id/{shopping_cart_id}", response_model=ShoppingCartData)
def get_shopping_cart_by_id(shopping_cart_id: int):
    """Gets a shopping cart by ID."""
    return crud.get_by_id(shopping_cart_id)

@router.get("/shopping_cart/get_all", response_model=List[ShoppingCartData])
def get_all_shopping_carts():
    """Gets all shopping carts."""
    return crud.get_all()