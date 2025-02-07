from typing import List, Optional
from pydantic import BaseModel, EmailStr, validator

from database_connection import PostgresDatabaseConnection

class CustomerData(BaseModel):
    """Data structure for Customer."""
    full_name: str
    email: EmailStr  # Usa EmailStr para validación de emails
    shipping_address: str
    phone: str
    registration_date: str  # YYYY-MM-DD format is recommended
    
    @validator("phone")
    def validate_phone(cls, phone):
        # Add your phone number validation logic here if needed.
        # For example, you could check the length or format.
        # Raise ValueError if the phone number is invalid.
        return phone


class CustomerCRUD:

    def __init__(self):
        self.db_connection = PostgresDatabaseConnection()
        self.db_connection.connect()

    def _execute_query(self, query: str, values: tuple = None) -> bool: # Better name for the function
        try:
            cursor = self.db_connection.connection.cursor()
            if values:
                cursor.execute(query, values)
            else:
                cursor.execute(query) #For queries without values.
            self.db_connection.connection.commit()
            cursor.close()
            return True #Indicate that the operation was successful.
        except Exception as e:
            print(f"Error in database operation: {e}")
            self.db_connection.connection.rollback() #Revert changes in case of error.
            return False

    def create(self, data: CustomerData) -> Optional[int]:
        """Creates a new customer."""
        query = """
            INSERT INTO Customer (full_name, email, shipping_address, phone, registration_date)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING customer_id;
        """
        values = (data.full_name, data.email, data.shipping_address, data.phone, data.registration_date)

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
                return CustomerData(*customer_data)
            return None
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
            for customer in customer_list:
                customers.append(CustomerData(*customer))
            return customers
        except Exception as e:
            print(f"Error getting all customers: {e}")
            return []

    def update(self, customer_id: int, data: CustomerData) -> bool:
        """Updates a customer."""
        query = """
            UPDATE Customer
            SET full_name = %s, email = %s, shipping_address = %s, phone = %s, registration_date = %s
            WHERE customer_id = %s;
        """
        values = (data.full_name, data.email, data.shipping_address, data.phone, data.registration_date, customer_id)
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
                return CustomerData(*customer_data)
            return None
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
            for customer in customer_list:
                customers.append(CustomerData(*customer))
            return customers
        except Exception as e:
            print(f"Error getting customers by name: {e}")
            return []