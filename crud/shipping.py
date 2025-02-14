from typing import List, Optional
from pydantic import BaseModel

from DB_Amazon.PGDatabase_Connection import PostgresDatabaseConnection

class ShippingData(BaseModel):
    """Data structure for Shipping."""
    shipping_company: str
    shipping_date: Optional[str] = None  # ISO 8601 format is recommended (YYYY-MM-DD)
    estimated_delivery: Optional[str] = None  # ISO 8601 format is recommended (YYYY-MM-DD)
    shipping_cost: Optional[float] = None

class ShippingCRUD:

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

    def create(self, data: ShippingData) -> Optional[int]:
        """Creates a new shipping entry."""
        query = """
            INSERT INTO Shipping (shipping_company, shipping_date, estimated_delivery, shipping_cost)
            VALUES (%s, %s, %s, %s)
            RETURNING shipping_id;
        """
        values = (data.shipping_company, data.shipping_date, data.estimated_delivery, data.shipping_cost)
        try:
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, values)
            shipping_id = cursor.fetchone()[0]
            self.db_connection.connection.commit()
            cursor.close()
            return shipping_id
        except Exception as e:
            self.db_connection.connection.rollback()
            print(f"Error creating shipping entry: {e}")
            return None

    def get_by_id(self, shipping_id: int) -> Optional[ShippingData]:
        """Gets a shipping entry by ID."""
        query = """
            SELECT shipping_company, shipping_date, estimated_delivery, shipping_cost
            FROM Shipping
            WHERE shipping_id = %s;
        """
        try:
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, (shipping_id,))
            shipping_data = cursor.fetchone()
            cursor.close()
            if shipping_data:
                return ShippingData(*shipping_data)
            return None
        except Exception as e:
            print(f"Error getting shipping entry by ID: {e}")
            return None

    def get_all(self) -> List[ShippingData]:
        """Gets all shipping entries."""
        query = """
            SELECT shipping_company, shipping_date, estimated_delivery, shipping_cost
            FROM Shipping;
        """
        shipping_entries = []
        try:
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query)
            shipping_list = cursor.fetchall()
            cursor.close()
            for shipping_entry in shipping_list:
                shipping_entries.append(ShippingData(*shipping_entry))
            return shipping_entries
        except Exception as e:
            print(f"Error getting all shipping entries: {e}")
            return []

    def update(self, shipping_id: int, data: ShippingData) -> bool:
        """Updates a shipping entry."""
        query = """
            UPDATE Shipping
            SET shipping_company = %s, shipping_date = %s, estimated_delivery = %s, shipping_cost = %s
            WHERE shipping_id = %s;
        """
        values = (data.shipping_company, data.shipping_date, data.estimated_delivery, data.shipping_cost, shipping_id)
        return self._execute_query(query, values)

    def delete(self, shipping_id: int) -> bool:
        """Deletes a shipping entry."""
        query = """
            DELETE FROM Shipping
            WHERE shipping_id = %s;
        """
        return self._execute_query(query, (shipping_id,))