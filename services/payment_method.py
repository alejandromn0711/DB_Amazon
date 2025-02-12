from typing import List

from fastapi import APIRouter

from crud.payment_method import PaymentMethodData, PaymentMethodCRUD

router = APIRouter()
crud = PaymentMethodCRUD()

@router.post("/payment_method/create", response_model=int)
def create_payment_method(data: PaymentMethodData):
    return crud.create(data)

@router.put("/payment_method/update/{payment_method_id}")
def update_payment_method(payment_method_id: int, data: PaymentMethodData):
    return crud.update(payment_method_id, data)

@router.delete("/payment_method/delete/{payment_method_id}")
def delete_payment_method(payment_method_id: int):
    return crud.delete(payment_method_id)

@router.get("/payment_method/get_by_id/{payment_method_id}", response_model=PaymentMethodData)
def get_payment_method_by_id(payment_method_id: int):
    return crud.get_by_id(payment_method_id)

@router.get("/payment_method/get_all", response_model=List[PaymentMethodData])
def get_all_payment_methods():
    return crud.get_all()

# Puedes agregar rutas adicionales según sea necesario, por ejemplo:
# @router.get("/payment_method/customer/{customer_id}", response_model=List[PaymentMethodData])
# def get_payment_methods_by_customer(customer_id: int):
#     return crud.get_payment_methods_by_customer(customer_id)