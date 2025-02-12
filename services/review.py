from typing import List

from fastapi import APIRouter

from crud.review import ReviewData, ReviewCRUD

router = APIRouter()
crud = ReviewCRUD()

@router.post("/review/create", response_model=int)
def create_review(data: ReviewData):
    return crud.create(data)

@router.put("/review/update/{review_id}")
def update_review(review_id: int, data: ReviewData):
    return crud.update(review_id, data)

@router.delete("/review/delete/{review_id}")
def delete_review(review_id: int):
    return crud.delete(review_id)

@router.get("/review/get_by_id/{review_id}", response_model=ReviewData)
def get_review_by_id(review_id: int):
    return crud.get_by_id(review_id)

@router.get("/review/get_all", response_model=List[ReviewData])
def get_all_reviews():
    return crud.get_all()

# Puedes agregar rutas adicionales según sea necesario, por ejemplo:
# @router.get("/review/customer/{customer_id}", response_model=List[ReviewData])
# def get_reviews_by_customer(customer_id: int):
#     return crud.get_reviews_by_customer(customer_id)