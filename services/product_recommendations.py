from typing import List

from fastapi import APIRouter

from crud.product_recommendations import ProductRecommendationsData, ProductRecommendationsCRUD

router = APIRouter()
crud = ProductRecommendationsCRUD()

@router.post("/product_recommendations/create", response_model=int)
def create_product_recommendation(data: ProductRecommendationsData):
    return crud.create(data)

@router.put("/product_recommendations/update/{product_recommendation_id}")
def update_product_recommendation(product_recommendation_id: int, data: ProductRecommendationsData):
    return crud.update(product_recommendation_id, data)

@router.delete("/product_recommendations/delete/{product_recommendation_id}")
def delete_product_recommendation(product_recommendation_id: int):
    return crud.delete(product_recommendation_id)

@router.get("/product_recommendations/get_by_id/{product_recommendation_id}", response_model=ProductRecommendationsData)
def get_product_recommendation_by_id(product_recommendation_id: int):
    return crud.get_by_id(product_recommendation_id)

@router.get("/product_recommendations/get_all", response_model=List[ProductRecommendationsData])
def get_all_product_recommendations():
    return crud.get_all()

# Puedes agregar rutas adicionales según sea necesario, por ejemplo:
# @router.get("/product_recommendations/customer/{customer_id}", response_model=List[ProductRecommendationsData])
# def get_product_recommendations_by_customer(customer_id: int):
#     return crud.get_product_recommendations_by_customer(customer_id)