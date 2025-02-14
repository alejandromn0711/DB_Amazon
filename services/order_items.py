from typing import List

from fastapi import APIRouter

from crud.order_items import OrderItemData, OrderItemCRUD  # Import the CRUD and the model

router = APIRouter()
crud = OrderItemCRUD()

@router.post("/order_items/create", response_model=int)
def create_order_item(data: OrderItemData):
    """Creates a new order item."""
    return crud.create(data)

@router.put("/order_items/update/{order_item_id}")
def update_order_item(order_item_id: int, data: OrderItemData):
    """Updates an existing order item."""
    return crud.update(order_item_id, data)

@router.delete("/order_items/delete/{order_item_id}")
def delete_order_item(order_item_id: int):
    """Deletes an order item."""
    return crud.delete(order_item_id)

@router.get("/order_items/get_by_id/{order_item_id}", response_model=OrderItemData)
def get_order_item_by_id(order_item_id: int):
    """Gets an order item by ID."""
    return crud.get_by_id(order_item_id)

@router.get("/order_items/get_all", response_model=List[OrderItemData])
def get_all_order_items():
    """Gets all order items."""
    return crud.get_all()