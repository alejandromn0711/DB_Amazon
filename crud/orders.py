from typing import List, Optional
from pydantic import BaseModel

from database_connection import PostgresDatabaseConnection

class OrdersData(BaseModel):
    """Data structure for Orders."""
    total_amount: float
    order_status: str
    customer_id: int       # Foreign key
    payment_method_id: int  # Foreign key
    shipping_id: int       # Foreign key

class OrdersCRUD:

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

    def create(self, data: OrdersData) -> Optional[int]:
        """Creates a new order."""
        query = """
            INSERT INTO Orders (total_amount, order_status, customer_id, payment_method_id, shipping_id)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING orders_id;
        """
        values = (data.total_amount, data.order_status, data.customer_id, data.payment_method_id, data.shipping_id)
        try:
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, values)
            orders_id = cursor.fetchone()[0]
            self.db_connection.connection.commit()
            cursor.close()
            return orders_id
        except Exception as e:
            self.db_connection.connection.rollback()
            print(f"Error creating order: {e}")
            return None

    def get_by_id(self, orders_id: int) -> Optional[OrdersData]:
        """Gets an order by ID."""
        query = """
            SELECT total_amount, order_status, customer_id, payment_method_id, shipping_id
            FROM Orders
            WHERE orders_id = %s;
        """
        try:
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, (orders_id,))
            order_data = cursor.fetchone()
            cursor.close()
            if order_data:
                return OrdersData(*order_data)
            return None
        except Exception as e:
            print(f"Error getting order by ID: {e}")
            return None

    def get_all(self) -> List[OrdersData]:
        """Gets all orders."""
        query = """
            SELECT total_amount, order_status, customer_id, payment_method_id, shipping_id
            FROM Orders;
        """
        orders = []
        try:
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query)
            order_list = cursor.fetchall()
            cursor.close()
            for order in order_list:
                orders.append(OrdersData(*order))
            return orders
        except Exception as e:
            print(f"Error getting all orders: {e}")
            return []

    def update(self, orders_id: int, data: OrdersData) -> bool:
        """Updates an order."""
        query = """
            UPDATE Orders
            SET total_amount = %s, order_status = %s, customer_id = %s, payment_method_id = %s, shipping_id = %s
            WHERE orders_id = %s;
        """
        values = (data.total_amount, data.order_status, data.customer_id, data.payment_method_id, data.shipping_id, orders_id)
        return self._execute_query(query, values)

    def delete(self, orders_id: int) -> bool:
        """Deletes an order."""
        query = """
            DELETE FROM Orders
            WHERE orders_id = %s;
        """
        return self._execute_query(query, (orders_id,))

    # Puedes agregar métodos adicionales según sea necesario, por ejemplo:
    # get_by_customer, get_by_status, etc.