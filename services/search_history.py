from typing import List

from fastapi import APIRouter

from crud.search_history import SearchHistoryData, SearchHistoryCRUD

router = APIRouter()
crud = SearchHistoryCRUD()

@router.post("/search_history/create", response_model=int)
def create_search_history(data: SearchHistoryData):
    return crud.create(data)

@router.put("/search_history/update/{search_history_id}")
def update_search_history(search_history_id: int, data: SearchHistoryData):
    return crud.update(search_history_id, data)

@router.delete("/search_history/delete/{search_history_id}")
def delete_search_history(search_history_id: int):
    return crud.delete(search_history_id)

@router.get("/search_history/get_by_id/{search_history_id}", response_model=SearchHistoryData)
def get_search_history_by_id(search_history_id: int):
    return crud.get_by_id(search_history_id)

@router.get("/search_history/get_all", response_model=List[SearchHistoryData])
def get_all_search_history():
    return crud.get_all()

# Puedes agregar rutas adicionales según sea necesario, por ejemplo:
# @router.get("/search_history/customer/{customer_id}", response_model=List[SearchHistoryData])
# def get_search_history_by_customer(customer_id: int):
#     return crud.get_search_history_by_customer(customer_id)