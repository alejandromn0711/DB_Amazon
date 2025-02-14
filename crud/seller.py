from typing import List, Optional
from pydantic import BaseModel

from DB_Amazon.PGDatabase_Connection import PostgresDatabaseConnection

class SellerData(BaseModel):
    """Data structure for Seller."""
    seller_name: str
    seller_type: Optional[str] = None
    seller_rating: Optional[float] = None

class SellerCRUD:

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

    def create(self, data: SellerData) -> Optional[int]:
        """Creates a new seller."""
        query = """
            INSERT INTO Seller (seller_name, seller_type, seller_rating)
            VALUES (%s, %s, %s)
            RETURNING seller_id;
        """
        values = (data.seller_name, data.seller_type, data.seller_rating)
        try:
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, values)
            seller_id = cursor.fetchone()[0]
            self.db_connection.connection.commit()
            cursor.close()
            return seller_id
        except Exception as e:
            self.db_connection.connection.rollback()
            print(f"Error creating seller: {e}")
            return None

    def get_by_id(self, seller_id: int) -> Optional[SellerData]:
        """Gets a seller by ID."""
        query = """
            SELECT seller_name, seller_type, seller_rating
            FROM Seller
            WHERE seller_id = %s;
        """
        try:
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, (seller_id,))
            seller_data = cursor.fetchone()
            cursor.close()
            if seller_data:
                return SellerData(*seller_data)
            return None
        except Exception as e:
            print(f"Error getting seller by ID: {e}")
            return None

    def get_all(self) -> List[SellerData]:
        """Gets all sellers."""
        query = """
            SELECT seller_name, seller_type, seller_rating
            FROM Seller;
        """
        sellers = []
        try:
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query)
            seller_list = cursor.fetchall()
            cursor.close()
            for seller in seller_list:
                sellers.append(SellerData(*seller))
            return sellers
        except Exception as e:
            print(f"Error getting all sellers: {e}")
            return []

    def update(self, seller_id: int, data: SellerData) -> bool:
        """Updates a seller."""
        query = """
            UPDATE Seller
            SET seller_name = %s, seller_type = %s, seller_rating = %s
            WHERE seller_id = %s;
        """
        values = (data.seller_name, data.seller_type, data.seller_rating, seller_id)
        return self._execute_query(query, values)

    def delete(self, seller_id: int) -> bool:
        """Deletes a seller."""
        query = """
            DELETE FROM Seller
            WHERE seller_id = %s;
        """
        return self._execute_query(query, (seller_id,))

    def get_by_name(self, seller_name: str) -> List[SellerData]:
        """Gets sellers by name (case-insensitive search)."""
        query = """
            SELECT seller_name, seller_type, seller_rating
            FROM Seller
            WHERE LOWER(seller_name) LIKE LOWER(%s);
        """
        sellers = []
        try:
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, ("%" + seller_name + "%",))  # Wildcard for partial search
            seller_list = cursor.fetchall()
            cursor.close()
            for seller in seller_list:
                sellers.append(SellerData(*seller))
            return sellers
        except Exception as e:
            print(f"Error getting sellers by name: {e}")
            return []