from typing import List

from fastapi import APIRouter

from crud.returns import ReturnsData, ReturnsCRUD

router = APIRouter()
crud = ReturnsCRUD()

@router.post("/returns/create", response_model=int)
def create_return(data: ReturnsData):
    """Creates a new return."""
    return crud.create(data)

@router.put("/returns/update/{returns_id}")
def update_return(returns_id: int, data: ReturnsData):
    """Updates an existing return."""
    return crud.update(returns_id, data)

@router.delete("/returns/delete/{returns_id}")
def delete_return(returns_id: int):
    """Deletes a return."""
    return crud.delete(returns_id)

@router.get("/returns/get_by_id/{returns_id}", response_model=ReturnsData)
def get_return_by_id(returns_id: int):
    """Gets a return by ID."""
    return crud.get_by_id(returns_id)

@router.get("/returns/get_all", response_model=List[ReturnsData])
def get_all_returns():
    """Gets all returns."""
    return crud.get_all()