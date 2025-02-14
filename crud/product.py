from typing import List, Optional
from pydantic import BaseModel

from DB_Amazon.PGDatabase_Connection import PostgresDatabaseConnection  # Make sure you have this connection

class ProductData(BaseModel):
    """Data structure for Product."""
    product_name: str
    description: Optional[str] = None  # Description is optional
    price: float  # Use float for prices
    quantity_available: int
    category_id: int  # Foreign key
    seller_id: int    # Foreign key

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "product_name": "Example Product",
                    "description": "A sample product",
                    "price": 19.99,
                    "quantity_available": 100,
                    "category_id": 1,
                    "seller_id": 1,
                }
            ]
        }
    }

class ProductCRUD:

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

    def create(self, data: ProductData) -> Optional[int]:
        """Creates a new product."""
        query = """
            INSERT INTO Product (product_name, description, price, quantity_available, category_id, seller_id)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING product_id;
        """
        values = (data.product_name, data.description, data.price, data.quantity_available, data.category_id, data.seller_id)
        try:
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, values)
            product_id = cursor.fetchone()[0]
            self.db_connection.connection.commit()
            cursor.close()
            return product_id
        except Exception as e:
            self.db_connection.connection.rollback()
            print(f"Error creating product: {e}")
            return None

    def update(self, product_id: int, data: ProductData) -> bool:
        """Updates a product."""
        query = """
            UPDATE Product
            SET product_name = %s, description = %s, price = %s, quantity_available = %s, category_id = %s, seller_id = %s
            WHERE product_id = %s;
        """
        values = (data.product_name, data.description, data.price, data.quantity_available, data.category_id, data.seller_id, product_id)
        return self._execute_query(query, values)

    def delete(self, product_id: int) -> bool:
        """Deletes a product."""
        query = """
            DELETE FROM Product
            WHERE product_id = %s;
        """
        return self._execute_query(query, (product_id,))

    def _get_products_from_query(self, query: str, values: tuple = None) -> List[ProductData]:
        """Helper function to fetch and process product data from a query."""
        products = []
        try:
            cursor = self.db_connection.connection.cursor()
            if values:
                cursor.execute(query, values)
            else:
                cursor.execute(query)
            product_list = cursor.fetchall()
            cursor.close()
            for product in product_list:
                products.append(ProductData(*product))
            return products
        except Exception as e:
            print(f"Error fetching products: {e}")
            return []

    def get_by_id(self, product_id: int) -> Optional[ProductData]:
        """Gets a product by ID."""
        query = """
            SELECT product_name, description, price, quantity_available, category_id, seller_id
            FROM Product
            WHERE product_id = %s;
        """
        products = self._get_products_from_query(query, (product_id,))
        return products[0] if products else None  # Return None if no products found

    def get_all(self) -> List[ProductData]:
        """Gets all products."""
        query = """
            SELECT product_name, description, price, quantity_available, category_id, seller_id
            FROM Product;
        """
        return self._get_products_from_query(query)

    def get_by_name(self, product_name: str) -> List[ProductData]:
        """Gets products by name (case-insensitive search)."""
        query = """
            SELECT product_name, description, price, quantity_available, category_id, seller_id
            FROM Product
            WHERE LOWER(product_name) LIKE LOWER(%s);  -- Case-insensitive comparison
        """
        return self._get_products_from_query(query, ("%" + product_name + "%",))

    def get_by_category(self, category_id: int) -> List[ProductData]:
        """Gets products by category."""
        query = """
            SELECT product_name, description, price, quantity_available, category_id, seller_id
            FROM Product
            WHERE category_id = %s;
        """
        return self._get_products_from_query(query, (category_id,))