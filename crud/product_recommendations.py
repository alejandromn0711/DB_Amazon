from typing import List, Optional
from pydantic import BaseModel

from DB_Amazon.PGDatabase_Connection import PostgresDatabaseConnection

class ProductRecommendationsData(BaseModel):
    """Data structure for ProductRecommendations."""
    customer_id: int             # Foreign key
    recommended_product_id: int  # Foreign key

class ProductRecommendationsCRUD:

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

    def create(self, data: ProductRecommendationsData) -> Optional[int]:
        """Creates a new product recommendation."""
        query = """
            INSERT INTO ProductRecommendations (customer_id, recommended_product_id)
            VALUES (%s, %s)
            RETURNING productRecommendation_id;
        """
        values = (data.customer_id, data.recommended_product_id)
        try:
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, values)
            product_recommendation_id = cursor.fetchone()[0]
            self.db_connection.connection.commit()
            cursor.close()
            return product_recommendation_id
        except Exception as e:
            self.db_connection.connection.rollback()
            print(f"Error creating product recommendation: {e}")
            return None

    def get_by_id(self, product_recommendation_id: int) -> Optional[ProductRecommendationsData]:
        """Gets a product recommendation by ID."""
        query = """
            SELECT customer_id, recommended_product_id
            FROM ProductRecommendations
            WHERE productRecommendation_id = %s;
        """
        try:
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, (product_recommendation_id,))
            product_recommendation_data = cursor.fetchone()
            cursor.close()
            if product_recommendation_data:
                return ProductRecommendationsData(*product_recommendation_data)
            return None
        except Exception as e:
            print(f"Error getting product recommendation by ID: {e}")
            return None

    def get_all(self) -> List[ProductRecommendationsData]:
        """Gets all product recommendations."""
        query = """
            SELECT customer_id, recommended_product_id
            FROM ProductRecommendations;
        """
        product_recommendations = []
        try:
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query)
            product_recommendation_list = cursor.fetchall()
            cursor.close()
            for product_recommendation in product_recommendation_list:
                product_recommendations.append(ProductRecommendationsData(*product_recommendation))
            return product_recommendations
        except Exception as e:
            print(f"Error getting all product recommendations: {e}")
            return []

    def update(self, product_recommendation_id: int, data: ProductRecommendationsData) -> bool:
        """Updates a product recommendation."""
        query = """
            UPDATE ProductRecommendations
            SET customer_id = %s, recommended_product_id = %s
            WHERE productRecommendation_id = %s;
        """
        values = (data.customer_id, data.recommended_product_id, product_recommendation_id)
        return self._execute_query(query, values)

    def delete(self, product_recommendation_id: int) -> bool:
        """Deletes a product recommendation."""
        query = """
            DELETE FROM ProductRecommendations
            WHERE productRecommendation_id = %s;
        """
        return self._execute_query(query, (product_recommendation_id,))