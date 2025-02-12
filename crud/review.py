from typing import List, Optional
from pydantic import BaseModel

from database_connection import PostgresDatabaseConnection

class ReviewData(BaseModel):
    """Data structure for Review."""
    rating: int
    comment: Optional[str] = None
    review_date: str  # ISO 8601 format is recommended (YYYY-MM-DD)
    customer_id: int    # Foreign key
    product_id: int     # Foreign key

class ReviewCRUD:

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

    def create(self, data: ReviewData) -> Optional[int]:
        """Creates a new review."""
        query = """
            INSERT INTO Review (rating, comment, review_date, customer_id, product_id)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING review_id;
        """
        values = (data.rating, data.comment, data.review_date, data.customer_id, data.product_id)
        try:
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, values)
            review_id = cursor.fetchone()[0]
            self.db_connection.connection.commit()
            cursor.close()
            return review_id
        except Exception as e:
            self.db_connection.connection.rollback()
            print(f"Error creating review: {e}")
            return None

    def get_by_id(self, review_id: int) -> Optional[ReviewData]:
        """Gets a review by ID."""
        query = """
            SELECT rating, comment, review_date, customer_id, product_id
            FROM Review
            WHERE review_id = %s;
        """
        try:
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, (review_id,))
            review_data = cursor.fetchone()
            cursor.close()
            if review_data:
                return ReviewData(*review_data)
            return None
        except Exception as e:
            print(f"Error getting review by ID: {e}")
            return None

    def get_all(self) -> List[ReviewData]:
        """Gets all reviews."""
        query = """
            SELECT rating, comment, review_date, customer_id, product_id
            FROM Review;
        """
        reviews = []
        try:
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query)
            review_list = cursor.fetchall()
            cursor.close()
            for review in review_list:
                reviews.append(ReviewData(*review))
            return reviews
        except Exception as e:
            print(f"Error getting all reviews: {e}")
            return []

    def update(self, review_id: int, data: ReviewData) -> bool:
        """Updates a review."""
        query = """
            UPDATE Review
            SET rating = %s, comment = %s, review_date = %s, customer_id = %s, product_id = %s
            WHERE review_id = %s;
        """
        values = (data.rating, data.comment, data.review_date, data.customer_id, data.product_id, review_id)
        return self._execute_query(query, values)

    def delete(self, review_id: int) -> bool:
        """Deletes a review."""
        query = """
            DELETE FROM Review
            WHERE review_id = %s;
        """
        return self._execute_query(query, (review_id,))

    # Puedes agregar métodos adicionales según sea necesario, por ejemplo:
    # get_by_customer, get_by_product, etc.