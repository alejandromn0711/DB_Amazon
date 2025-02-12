from typing import List, Optional
from pydantic import BaseModel

from database_connection import PostgresDatabaseConnection

class OrderItemData(BaseModel):
    """Data structure for Order_Items."""
    orders_id: int
    product_id: int
    quantity: int
    price_at_purchase: float
    coupon_id: Optional[int] = None
    offer_id: Optional[int] = None


class OrderItemCRUD:

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

    def create(self, data: OrderItemData) -> Optional[int]:
        """Creates a new order item."""
        query = """
            INSERT INTO Order_Items (orders_id, product_id, quantity, price_at_purchase, coupon_id, offer_id)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING order_item_id;
        """
        values = (data.orders_id, data.product_id, data.quantity, data.price_at_purchase, data.coupon_id, data.offer_id)
        try:
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, values)
            order_item_id = cursor.fetchone()[0]
            self.db_connection.connection.commit()
            cursor.close()
            return order_item_id
        except Exception as e:
            self.db_connection.connection.rollback()
            print(f"Error creating order item: {e}")
            return None

    def get_by_id(self, order_item_id: int) -> Optional[OrderItemData]:
        """Gets an order item by ID."""
        query = """
            SELECT orders_id, product_id, quantity, price_at_purchase, coupon_id, offer_id
            FROM Order_Items
            WHERE order_item_id = %s;
        """
        try:
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, (order_item_id,))
            order_item_data = cursor.fetchone()
            cursor.close()
            if order_item_data:
                return OrderItemData(*order_item_data)
            return None
        except Exception as e:
            print(f"Error getting order item by ID: {e}")
            return None

    def get_all(self) -> List[OrderItemData]:
        """Gets all order items."""
        query = """
            SELECT orders_id, product_id, quantity, price_at_purchase, coupon_id, offer_id
            FROM Order_Items;
        """
        order_items = []
        try:
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query)
            order_item_list = cursor.fetchall()
            cursor.close()
            for order_item in order_item_list:
                order_items.append(OrderItemData(*order_item))
            return order_items
        except Exception as e:
            print(f"Error getting all order items: {e}")
            return []

    def update(self, order_item_id: int, data: OrderItemData) -> bool:
        """Updates an order item."""
        query = """
            UPDATE Order_Items
            SET orders_id = %s, product_id = %s, quantity = %s, price_at_purchase = %s, coupon_id = %s, offer_id = %s
            WHERE order_item_id = %s;
        """
        values = (data.orders_id, data.product_id, data.quantity, data.price_at_purchase, data.coupon_id, data.offer_id, order_item_id)
        return self._execute_query(query, values)

    def delete(self, order_item_id: int) -> bool:
        """Deletes an order item."""
        query = """
            DELETE FROM Order_Items
            WHERE order_item_id = %s;
        """
        return self._execute_query(query, (order_item_id,))

    # Puedes agregar métodos adicionales según sea necesario, por ejemplo:
    # get_by_order, etc.