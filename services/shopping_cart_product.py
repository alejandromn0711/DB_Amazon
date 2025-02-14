from typing import List

from fastapi import APIRouter

from crud.shopping_cart_product import ShoppingCartProductData, ShoppingCartProductCRUD

router = APIRouter()
crud = ShoppingCartProductCRUD()

@router.post("/shopping_cart_product/add", status_code=201)
def add_product_to_cart(data: ShoppingCartProductData):
    """Adds a product to the shopping cart."""
    if crud.create(data):
        return {"message": "Product added to cart successfully"}
    else:
        return {"message": "Failed to add product to cart"}

@router.get("/shopping_cart_product/cart/{cart_id}", response_model=List[ShoppingCartProductData])
def get_products_in_cart(cart_id: int):
    """Gets products in a shopping cart."""
    return crud.get_by_cart_id(cart_id)

@router.put("/shopping_cart_product/update/{cart_id}/{product_id}")
def update_product_quantity(cart_id: int, product_id: int, data: ShoppingCartProductData):
    """Updates the quantity of a product in the shopping cart."""
    if crud.update(cart_id, product_id, data):
        return {"message": "Product quantity updated successfully"}
    else:
        return {"message": "Failed to update product quantity"}

@router.delete("/shopping_cart_product/remove/{cart_id}/{product_id}")
def remove_product_from_cart(cart_id: int, product_id: int):
    """Removes a product from the shopping cart."""
    if crud.delete(cart_id, product_id):
        return {"message": "Product removed from cart successfully"}
    else:
        return {"message": "Failed to remove product from cart"}

@router.delete("/shopping_cart_product/clear/{cart_id}")
def clear_shopping_cart(cart_id: int):
    """Clears all products from the shopping cart."""
    if crud.delete_by_cart_id(cart_id):
        return {"message": "Shopping cart cleared successfully"}
    else:
        return {"message": "Failed to clear shopping cart"}