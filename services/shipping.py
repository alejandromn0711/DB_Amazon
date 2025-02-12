from typing import List

from fastapi import APIRouter

from crud.shipping import ShippingData, ShippingCRUD

router = APIRouter()
crud = ShippingCRUD()

@router.post("/shipping/create", response_model=int)
def create_shipping(data: ShippingData):
    return crud.create(data)

@router.put("/shipping/update/{shipping_id}")
def update_shipping(shipping_id: int, data: ShippingData):
    return crud.update(shipping_id, data)

@router.delete("/shipping/delete/{shipping_id}")
def delete_shipping(shipping_id: int):
    return crud.delete(shipping_id)

@router.get("/shipping/get_by_id/{shipping_id}", response_model=ShippingData)
def get_shipping_by_id(shipping_id: int):
    return crud.get_by_id(shipping_id)

@router.get("/shipping/get_all", response_model=List[ShippingData])
def get_all_shipping():
    return crud.get_all()