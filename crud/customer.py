from typing import List, Optional
from pydantic import BaseModel, EmailStr, validator
from datetime import date

from database_connection import PostgresDatabaseConnection

class CustomerData(BaseModel):
    """Data structure for Customer."""
    full_name: str
    email: EmailStr
    shipping_address: str
    phone: str
    registration_date: date  # Tipo de dato date

    @validator("phone")
    def validate_phone(cls, phone):
        # Aquí puedes agregar validación más específica para el número de teléfono
        # Por ejemplo, longitud, formato, etc.
        return phone

class CustomerCRUD:

    def __init__(self):
        self.db_connection = PostgresDatabaseConnection()
        self.db_connection.connect()

    def _execute_query(self, query: str, values: tuple = None) -> bool:
        try:
            cursor = self.db_connection.connection.cursor()
            if values:
                cursor.execute(query, values)
            else:
                cursor.execute(query)
            self.db_connection.connection.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"Error en la operación de la base de datos: {e}")
            self.db_connection.connection.rollback()
            return False

    def create(self, data: CustomerData) -> Optional[int]:
        """Creates a new customer."""
        query = """
            INSERT INTO Customer (full_name, email, shipping_address, phone, registration_date)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING customer_id;
        """
        values = (data.full_name, data.email, data.shipping_address, data.phone, data.registration_date.strftime('%Y-%m-%d'))  # Formateo de fecha para la BD
        try:
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, values)
            customer_id = cursor.fetchone()[0]
            self.db_connection.connection.commit()
            cursor.close()
            return customer_id
        except Exception as e:
            self.db_connection.connection.rollback()
            print(f"Error creating customer: {e}")
            return None

    def get_by_id(self, customer_id: int) -> Optional[CustomerData]:
        """Gets a customer by ID."""
        query = """
            SELECT full_name, email, shipping_address, phone, registration_date
            FROM Customer
            WHERE customer_id = %s;
        """
        try:
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, (customer_id,))
            customer_data = cursor.fetchone()
            cursor.close()
            if customer_data:
                customer_dict = {
                    "full_name": customer_data[0],
                    "email": customer_data[1],
                    "shipping_address": customer_data[2],
                    "phone": customer_data[3],
                    "registration_date": customer_data[4] # No es necesario formatear, FastAPI lo hace automáticamente
                }
                return CustomerData(**customer_dict)
            return None  # Retorna None si no se encuentra el cliente
        except Exception as e:
            print(f"Error getting customer by ID: {e}")
            return None

    def get_all(self) -> List[CustomerData]:
        """Gets all customers."""
        query = """
            SELECT full_name, email, shipping_address, phone, registration_date
            FROM Customer;
        """
        customers = []
        try:
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query)
            customer_list = cursor.fetchall()
            cursor.close()
            for customer_data in customer_list:
                customer_dict = {
                    "full_name": customer_data[0],
                    "email": customer_data[1],
                    "shipping_address": customer_data[2],
                    "phone": customer_data[3],
                    "registration_date": customer_data[4] # No es necesario formatear, FastAPI lo hace automáticamente
                }
                customers.append(CustomerData(**customer_dict))
            return customers
        except Exception as e:
            print(f"Error getting all customers: {e}")
            return []  # Retorna una lista vacía en caso de error

    def update(self, customer_id: int, data: CustomerData) -> bool:
        """Updates a customer."""
        query = """
            UPDATE Customer
            SET full_name = %s, email = %s, shipping_address = %s, phone = %s, registration_date = %s
            WHERE customer_id = %s;
        """
        values = (data.full_name, data.email, data.shipping_address, data.phone, data.registration_date.strftime('%Y-%m-%d'), customer_id)  # Formateo de fecha para la BD
        return self._execute_query(query, values)

    def delete(self, customer_id: int) -> bool:
        """Deletes a customer."""
        query = """
            DELETE FROM Customer
            WHERE customer_id = %s;
        """
        return self._execute_query(query, (customer_id,))

    def get_by_email(self, email: str) -> Optional[CustomerData]:
        """Gets a customer by email."""
        query = """
            SELECT full_name, email, shipping_address, phone, registration_date
            FROM Customer
            WHERE email = %s;
        """
        try:
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, (email,))
            customer_data = cursor.fetchone()
            cursor.close()
            if customer_data:
                customer_dict = {
                    "full_name": customer_data[0],
                    "email": customer_data[1],
                    "shipping_address": customer_data[2],
                    "phone": customer_data[3],
                    "registration_date": customer_data[4] # No es necesario formatear, FastAPI lo hace automáticamente
                }
                return CustomerData(**customer_dict)
            return None  # Retorna None si no se encuentra el cliente
        except Exception as e:
            print(f"Error getting customer by email: {e}")
            return None

    def get_by_name(self, full_name: str) -> List[CustomerData]:
        """Gets customers by name (case-insensitive search)."""
        query = """
            SELECT full_name, email, shipping_address, phone, registration_date
            FROM Customer
            WHERE LOWER(full_name) LIKE LOWER(%s);
        """
        customers = []
        try:
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, ("%" + full_name + "%",))  # Wildcard for partial matches
            customer_list = cursor.fetchall()
            cursor.close()
            for customer_data in customer_list:
                customer_dict = {
                    "full_name": customer_data[0],
                    "email": customer_data[1],
                    "shipping_address": customer_data[2],
                    "phone": customer_data[3],
                    "registration_date": customer_data[4] # No es necesario formatear, FastAPI lo hace automáticamente
                }
                customers.append(CustomerData(**customer_dict))
            return customers
        except Exception as e:
            print(f"Error getting customers by name: {e}")
            return []  # Retorna una lista vacía en caso de error


# Ejemplo de uso en un endpoint de FastAPI:
from fastapi import FastAPI, APIRouter

app = FastAPI()
router = APIRouter()
customer_crud = CustomerCRUD()

@router.get("/customer/get_by_id/{customer_id}", response_model=CustomerData)
def get_customer_by_id(customer_id: int):
    customer = customer_crud.get_by_id(customer_id)
    return customer  # FastAPI serializa automáticamente el objeto date a ISO 8601

app.include_router(router)