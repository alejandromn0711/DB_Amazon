from typing import List, Optional
from pydantic import BaseModel

from PGDatabase_Connection import PostgresDatabaseConnection

class ShoppingCartData(BaseModel):
    """Data structure for ShoppingCart."""
    customer_id: int    # Foreign key

class ShoppingCartCRUD:

    def __init__(self):
        """Initialize the database connection."""
        self.db_connection = PostgresDatabaseConnection()
        self.db_connection.connect()

    def _execute_query(self, query: str, values: tuple = None) -> bool:
        """Execute a query on the database."""
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
            print(f"Error in database operation: {e}")
            self.db_connection.connection.rollback()
            return False

    def create(self, data: ShoppingCartData) -> Optional[int]:
        """Creates a new shopping cart."""
        query = """
            INSERT INTO ShoppingCart (customer_id)
            VALUES (%s)
            RETURNING shoppingCart_id;
        """
        values = (data.customer_id,)
        try:
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, values)
            shopping_cart_id = cursor.fetchone()[0]
            self.db_connection.connection.commit()
            cursor.close()
            return shopping_cart_id
        except Exception as e:
            self.db_connection.connection.rollback()
            print(f"Error creating shopping cart: {e}")
            return None

    def get_by_id(self, shopping_cart_id: int) -> Optional[ShoppingCartData]:
        """Gets a shopping cart by ID."""
        query = """
            SELECT customer_id
            FROM ShoppingCart
            WHERE shoppingCart_id = %s;
        """
        try:
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, (shopping_cart_id,))
            shopping_cart_data = cursor.fetchone()
            cursor.close()
            if shopping_cart_data:
                return ShoppingCartData(*shopping_cart_data)
            return None
        except Exception as e:
            print(f"Error getting shopping cart by ID: {e}")
            return None

    def get_all(self) -> List[ShoppingCartData]:
        """Gets all shopping carts."""
        query = """
            SELECT customer_id
            FROM ShoppingCart;
        """
        shopping_carts = []
        try:
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query)
            shopping_cart_list = cursor.fetchall()
            cursor.close()
            for shopping_cart in shopping_cart_list:
                shopping_carts.append(ShoppingCartData(*shopping_cart))
            return shopping_carts
        except Exception as e:
            print(f"Error getting all shopping carts: {e}")
            return []

    def update(self, shopping_cart_id: int, data: ShoppingCartData) -> bool:
        """Updates a shopping cart."""
        query = """
            UPDATE ShoppingCart
            SET customer_id = %s
            WHERE shoppingCart_id = %s;
        """
        values = (data.customer_id, shopping_cart_id)
        return self._execute_query(query, values)

    def delete(self, shopping_cart_id: int) -> bool:
        """Deletes a shopping cart."""
        query = """
            DELETE FROM ShoppingCart
            WHERE shoppingCart_id = %s;
        """
        return self._execute_query(query, (shopping_cart_id,))