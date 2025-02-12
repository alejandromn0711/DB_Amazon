from typing import List

from fastapi import APIRouter

from crud.seller import SellerData, SellerCRUD

router = APIRouter()
crud = SellerCRUD()

@router.post("/seller/create", response_model=int)
def create_seller(data: SellerData):
    return crud.create(data)

@router.put("/seller/update/{seller_id}")
def update_seller(seller_id: int, data: SellerData):
    return crud.update(seller_id, data)

@router.delete("/seller/delete/{seller_id}")
def delete_seller(seller_id: int):
    return crud.delete(seller_id)

@router.get("/seller/get_by_id/{seller_id}", response_model=SellerData)
def get_seller_by_id(seller_id: int):
    return crud.get_by_id(seller_id)

@router.get("/seller/get_all", response_model=List[SellerData])
def get_all_sellers():
    return crud.get_all()

@router.get("/seller/get_by_name/{seller_name}", response_model=List[SellerData])
def get_seller_by_name(seller_name: str):
    return crud.get_by_name(seller_name)