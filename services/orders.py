from typing import List

from fastapi import APIRouter

from crud.orders import OrdersData, OrdersCRUD

router = APIRouter()
crud = OrdersCRUD()

@router.post("/orders/create", response_model=int)
def create_order(data: OrdersData):
    return crud.create(data)

@router.put("/orders/update/{orders_id}")
def update_order(orders_id: int, data: OrdersData):
    return crud.update(orders_id, data)

@router.delete("/orders/delete/{orders_id}")
def delete_order(orders_id: int):
    return crud.delete(orders_id)

@router.get("/orders/get_by_id/{orders_id}", response_model=OrdersData)
def get_order_by_id(orders_id: int):
    return crud.get_by_id(orders_id)

@router.get("/orders/get_all", response_model=List[OrdersData])
def get_all_orders():
    return crud.get_all()

# Puedes agregar rutas adicionales según sea necesario, por ejemplo:
# @router.get("/orders/customer/{customer_id}", response_model=List[OrdersData])
# def get_orders_by_customer(customer_id: int):
#     return crud.get_by_customer(customer_id)