from typing import List, Optional
from pydantic import BaseModel

from database_connection import PostgresDatabaseConnection

class PaymentMethodData(BaseModel):
    """Data structure for PaymentMethod."""
    payment_type: str
    customer_id: Optional[int] = None  # Foreign key (puede ser nulo)


class PaymentMethodCRUD:

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

    def create(self, data: PaymentMethodData) -> Optional[int]:
        """Creates a new payment method."""
        query = """
            INSERT INTO PaymentMethod (payment_type, customer_id)
            VALUES (%s, %s)
            RETURNING payment_method_id;
        """
        values = (data.payment_type, data.customer_id)
        try:
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, values)
            payment_method_id = cursor.fetchone()[0]
            self.db_connection.connection.commit()
            cursor.close()
            return payment_method_id
        except Exception as e:
            self.db_connection.connection.rollback()
            print(f"Error creating payment method: {e}")
            return None

    def get_by_id(self, payment_method_id: int) -> Optional[PaymentMethodData]:
        """Gets a payment method by ID."""
        query = """
            SELECT payment_type, customer_id
            FROM PaymentMethod
            WHERE payment_method_id = %s;
        """
        try:
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, (payment_method_id,))
            payment_method_data = cursor.fetchone()
            cursor.close()
            if payment_method_data:
                return PaymentMethodData(*payment_method_data)
            return None
        except Exception as e:
            print(f"Error getting payment method by ID: {e}")
            return None

    def get_all(self) -> List[PaymentMethodData]:
        """Gets all payment methods."""
        query = """
            SELECT payment_type, customer_id
            FROM PaymentMethod;
        """
        payment_methods = []
        try:
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query)
            payment_method_list = cursor.fetchall()
            cursor.close()
            for payment_method in payment_method_list:
                payment_methods.append(PaymentMethodData(*payment_method))
            return payment_methods
        except Exception as e:
            print(f"Error getting all payment methods: {e}")
            return []

    def update(self, payment_method_id: int, data: PaymentMethodData) -> bool:
        """Updates a payment method."""
        query = """
            UPDATE PaymentMethod
            SET payment_type = %s, customer_id = %s
            WHERE payment_method_id = %s;
        """
        values = (data.payment_type, data.customer_id, payment_method_id)
        return self._execute_query(query, values)

    def delete(self, payment_method_id: int) -> bool:
        """Deletes a payment method."""
        query = """
            DELETE FROM PaymentMethod
            WHERE payment_method_id = %s;
        """
        return self._execute_query(query, (payment_method_id,))

    # Puedes agregar métodos adicionales según sea necesario, por ejemplo:
    # get_by_customer, etc.