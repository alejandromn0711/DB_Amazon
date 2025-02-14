from typing import List

from fastapi import APIRouter

from crud.search_history import SearchHistoryData, SearchHistoryCRUD

router = APIRouter()
crud = SearchHistoryCRUD()

@router.post("/search_history/create", response_model=int)
def create_search_history(data: SearchHistoryData):
    """Creates a new search history entry."""
    return crud.create(data)

@router.put("/search_history/update/{search_history_id}")
def update_search_history(search_history_id: int, data: SearchHistoryData):
    """Updates an existing search history entry."""
    return crud.update(search_history_id, data)

@router.delete("/search_history/delete/{search_history_id}")
def delete_search_history(search_history_id: int):
    """Deletes a search history entry."""
    return crud.delete(search_history_id)

@router.get("/search_history/get_by_id/{search_history_id}", response_model=SearchHistoryData)
def get_search_history_by_id(search_history_id: int):
    """Gets a search history entry by ID."""
    return crud.get_by_id(search_history_id)

@router.get("/search_history/get_all", response_model=List[SearchHistoryData])
def get_all_search_history():
    """Gets all search history entries."""
    return crud.get_all()