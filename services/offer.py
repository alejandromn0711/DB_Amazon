from typing import List

from fastapi import APIRouter

from crud.offer import OfferData, OfferCRUD

router = APIRouter()
crud = OfferCRUD()

@router.post("/offer/create", response_model=int)
def create_offer(data: OfferData):
    return crud.create(data)

@router.put("/offer/update/{offer_id}")
def update_offer(offer_id: int, data: OfferData):
    return crud.update(offer_id, data)

@router.delete("/offer/delete/{offer_id}")
def delete_offer(offer_id: int):
    return crud.delete(offer_id)

@router.get("/offer/get_by_id/{offer_id}", response_model=OfferData)
def get_offer_by_id(offer_id: int):
    return crud.get_by_id(offer_id)

@router.get("/offer/get_all", response_model=List[OfferData])
def get_all_offers():
    return crud.get_all()

@router.get("/offer/get_by_product/{product_id}", response_model=List[OfferData])
def get_offers_by_product(product_id: int):
    return crud.get_by_product(product_id)