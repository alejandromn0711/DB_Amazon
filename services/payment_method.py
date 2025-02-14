from typing import List

from fastapi import APIRouter

from crud.payment_method import PaymentMethodData, PaymentMethodCRUD

router = APIRouter()
crud = PaymentMethodCRUD()

@router.post("/payment_method/create", response_model=int)
def create_payment_method(data: PaymentMethodData):
    """Creates a new payment method."""
    return crud.create(data)

@router.put("/payment_method/update/{payment_method_id}")
def update_payment_method(payment_method_id: int, data: PaymentMethodData):
    """Updates an existing payment method."""
    return crud.update(payment_method_id, data)

@router.delete("/payment_method/delete/{payment_method_id}")
def delete_payment_method(payment_method_id: int):
    """Deletes a payment method."""
    return crud.delete(payment_method_id)

@router.get("/payment_method/get_by_id/{payment_method_id}", response_model=PaymentMethodData)
def get_payment_method_by_id(payment_method_id: int):
    """Gets a payment method by ID."""
    return crud.get_by_id(payment_method_id)

@router.get("/payment_method/get_all", response_model=List[PaymentMethodData])
def get_all_payment_methods():
    """Gets all payment methods."""
    return crud.get_all()