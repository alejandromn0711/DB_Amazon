from typing import List, Optional
from pydantic import BaseModel

from DB_Amazon.PGDatabase_Connection import PostgresDatabaseConnection

class ReturnsData(BaseModel):
    """Data structure for Returns."""
    return_date: str      # ISO 8601 format is recommended (YYYY-MM-DD)
    return_reason: Optional[str] = None
    return_status: Optional[str] = None
    order_item_id: int        # Foreign key

class ReturnsCRUD:

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

    def create(self, data: ReturnsData) -> Optional[int]:
        """Creates a new return."""
        query = """
            INSERT INTO Returns (return_date, return_reason, return_status, order_item_id)
            VALUES (%s, %s, %s, %s)
            RETURNING returns_id;
        """
        values = (data.return_date, data.return_reason, data.return_status, data.order_item_id)
        try:
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, values)
            returns_id = cursor.fetchone()[0]
            self.db_connection.connection.commit()
            cursor.close()
            return returns_id
        except Exception as e:
            self.db_connection.connection.rollback()
            print(f"Error creating return: {e}")
            return None

    def get_by_id(self, returns_id: int) -> Optional[ReturnsData]:
        """Gets a return by ID."""
        query = """
            SELECT return_date, return_reason, return_status, order_item_id
            FROM Returns
            WHERE returns_id = %s;
        """
        try:
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, (returns_id,))
            return_data = cursor.fetchone()
            cursor.close()
            if return_data:
                return ReturnsData(*return_data)
            return None
        except Exception as e:
            print(f"Error getting return by ID: {e}")
            return None

    def get_all(self) -> List[ReturnsData]:
        """Gets all returns."""
        query = """
            SELECT return_date, return_reason, return_status, order_item_id
            FROM Returns;
        """
        returns = []
        try:
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query)
            return_list = cursor.fetchall()
            cursor.close()
            for return_item in return_list:
                returns.append(ReturnsData(*return_item))
            return returns
        except Exception as e:
            print(f"Error getting all returns: {e}")
            return []

    def update(self, returns_id: int, data: ReturnsData) -> bool:
        """Updates a return."""
        query = """
            UPDATE Returns
            SET return_date = %s, return_reason = %s, return_status = %s, order_item_id = %s
            WHERE returns_id = %s;
        """
        values = (data.return_date, data.return_reason, data.return_status, data.order_item_id, returns_id)
        return self._execute_query(query, values)

    def delete(self, returns_id: int) -> bool:
        """Deletes a return."""
        query = """
            DELETE FROM Returns
            WHERE returns_id = %s;
        """
        return self._execute_query(query, (returns_id,))