from typing import List, Optional
from pydantic import BaseModel

from database_connection import PostgresDatabaseConnection

class ShoppingCartProductData(BaseModel):
    """Data structure for ShoppingCart_Product."""
    cart_id: int       # Foreign key (ShoppingCart)
    product_id: int    # Foreign key (Product)
    quantity: int

class ShoppingCartProductCRUD:

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

    def create(self, data: ShoppingCartProductData) -> bool:  # Retorna True o False
        """Adds a product to the shopping cart."""
        query = """
            INSERT INTO ShoppingCart_Product (cart_id, product_id, quantity)
            VALUES (%s, %s, %s);
        """
        values = (data.cart_id, data.product_id, data.quantity)
        return self._execute_query(query, values)

    def get_by_cart_id(self, cart_id: int) -> List[ShoppingCartProductData]:
        """Gets products in a shopping cart."""
        query = """
            SELECT product_id, quantity
            FROM ShoppingCart_Product
            WHERE cart_id = %s;
        """
        products = []
        try:
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, (cart_id,))
            product_list = cursor.fetchall()
            cursor.close()
            for product in product_list:
                products.append(ShoppingCartProductData(cart_id=cart_id, product_id=product[0], quantity=product[1])) #Incluir cart_id
            return products
        except Exception as e:
            print(f"Error getting products in shopping cart: {e}")
            return []

    def update(self, cart_id: int, product_id: int, data: ShoppingCartProductData) -> bool:
        """Updates the quantity of a product in the shopping cart."""
        query = """
            UPDATE ShoppingCart_Product
            SET quantity = %s
            WHERE cart_id = %s AND product_id = %s;
        """
        values = (data.quantity, cart_id, product_id)
        return self._execute_query(query, values)

    def delete(self, cart_id: int, product_id: int) -> bool:
        """Removes a product from the shopping cart."""
        query = """
            DELETE FROM ShoppingCart_Product
            WHERE cart_id = %s AND product_id = %s;
        """
        return self._execute_query(query, (cart_id, product_id))

    def delete_by_cart_id(self, cart_id: int) -> bool:
        """Removes all products from the shopping cart."""
        query = """
            DELETE FROM ShoppingCart_Product
            WHERE cart_id = %s;
        """
        return self._execute_query(query, (cart_id,))

    # No se incluye get_by_id porque la clave primaria es compuesta (cart_id, product_id)