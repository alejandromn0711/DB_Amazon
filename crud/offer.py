from typing import List, Optional
from pydantic import BaseModel

from database_connection import PostgresDatabaseConnection

class OfferData(BaseModel):
    """Data structure for Offer."""
    discount: float
    start_date: str  # YYYY-MM-DD format is recommended
    end_date: str    # YYYY-MM-DD format is recommended


class OfferCRUD:

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

    def create(self, data: OfferData) -> Optional[int]:
        """Creates a new offer."""
        query = """
            INSERT INTO Offer (discount, start_date, end_date)  -- product_id eliminado
            VALUES (%s, %s, %s)
            RETURNING offer_id;
        """
        values = (data.discount, data.start_date, data.end_date) # product_id eliminado
        try:
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, values)
            offer_id = cursor.fetchone()[0]
            self.db_connection.connection.commit()
            cursor.close()
            return offer_id
        except Exception as e:
            self.db_connection.connection.rollback()
            print(f"Error creating offer: {e}")
            return None

    def get_by_id(self, offer_id: int) -> Optional[OfferData]:
        """Gets an offer by ID."""
        query = """
            SELECT discount, start_date, end_date  -- product_id eliminado
            FROM Offer
            WHERE offer_id = %s;
        """
        try:
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, (offer_id,))
            offer_data = cursor.fetchone()
            cursor.close()
            if offer_data:
                return OfferData(*offer_data)
            return None
        except Exception as e:
            print(f"Error getting offer by ID: {e}")
            return None

    def get_all(self) -> List[OfferData]:
        """Gets all offers."""
        query = """
            SELECT discount, start_date, end_date  -- product_id eliminado
            FROM Offer;
        """
        offers = []
        try:
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query)
            offer_list = cursor.fetchall()
            cursor.close()
            for offer in offer_list:
                offers.append(OfferData(*offer))
            return offers
        except Exception as e:
            print(f"Error getting all offers: {e}")
            return []

    def update(self, offer_id: int, data: OfferData) -> bool:
        """Updates an offer."""
        query = """
            UPDATE Offer
            SET discount = %s, start_date = %s, end_date = %s  -- product_id eliminado
            WHERE offer_id = %s;
        """
        values = (data.discount, data.start_date, data.end_date, offer_id)  # product_id eliminado
        return self._execute_query(query, values)

    def delete(self, offer_id: int) -> bool:
        """Deletes an offer."""
        query = """
            DELETE FROM Offer
            WHERE offer_id = %s;
        """
        return self._execute_query(query, (offer_id,))

    def get_by_product(self, product_id: int) -> List[OfferData]:
        """Gets offers by product."""
        # Esta función ya no es necesaria, ya que product_id no está en la tabla Offer
        raise NotImplementedError("This method is no longer applicable to the Offer table.")