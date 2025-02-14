from typing import List

from fastapi import APIRouter

from crud.review import ReviewData, ReviewCRUD

router = APIRouter()
crud = ReviewCRUD()

@router.post("/review/create", response_model=int)
def create_review(data: ReviewData):
    """Creates a new review."""
    return crud.create(data)

@router.put("/review/update/{review_id}")
def update_review(review_id: int, data: ReviewData):
    """Updates an existing review."""
    return crud.update(review_id, data)

@router.delete("/review/delete/{review_id}")
def delete_review(review_id: int):
    """Deletes a review."""
    return crud.delete(review_id)

@router.get("/review/get_by_id/{review_id}", response_model=ReviewData)
def get_review_by_id(review_id: int):
    """Gets a review by ID."""
    return crud.get_by_id(review_id)

@router.get("/review/get_all", response_model=List[ReviewData])
def get_all_reviews():
    """Gets all reviews."""
    return crud.get_all()