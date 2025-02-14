from typing import List, Optional
from pydantic import BaseModel

from DB_Amazon.PGDatabase_Connection import PostgresDatabaseConnection

class CouponsData(BaseModel):
    """Data structure for Coupons."""
    discount_code: str
    discount_value: float
    expiration_date: str  # YYYY-MM-DD format is recommended

class CouponsCRUD:

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

    def create(self, data: CouponsData) -> Optional[int]:
        """Create a new coupon."""
        query = """
            INSERT INTO Coupons (discount_code, discount_value, expiration_date)
            VALUES (%s, %s, %s)
            RETURNING coupons_id;
        """
        values = (data.discount_code, data.discount_value, data.expiration_date)
        try:
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, values)
            coupons_id = cursor.fetchone()[0]
            self.db_connection.connection.commit()
            cursor.close()
            return coupons_id
        except Exception as e:
            self.db_connection.connection.rollback()
            print(f"Error creating coupon: {e}")
            return None

    def get_by_id(self, coupons_id: int) -> Optional[CouponsData]:
        """Get a coupon by ID."""
        query = """
            SELECT discount_code, discount_value, expiration_date
            FROM Coupons
            WHERE coupons_id = %s;
        """
        try:
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, (coupons_id,))
            coupon_data = cursor.fetchone()
            cursor.close()
            if coupon_data:
                return CouponsData(*coupon_data)
            return None
        except Exception as e:
            print(f"Error getting coupon by ID: {e}")
            return None

    def get_all(self) -> List[CouponsData]:
        """Get all coupons."""
        query = """
            SELECT discount_code, discount_value, expiration_date
            FROM Coupons;
        """
        coupons = []
        try:
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query)
            coupon_list = cursor.fetchall()
            cursor.close()
            for coupon in coupon_list:
                coupons.append(CouponsData(*coupon))
            return coupons
        except Exception as e:
            print(f"Error getting all coupons: {e}")
            return []

    def update(self, coupons_id: int, data: CouponsData) -> bool:
        """Update a coupon."""
        query = """
            UPDATE Coupons
            SET discount_code = %s, discount_value = %s, expiration_date = %s
            WHERE coupons_id = %s;
        """
        values = (data.discount_code, data.discount_value, data.expiration_date, coupons_id)
        return self._execute_query(query, values)

    def delete(self, coupons_id: int) -> bool:
        """Delete a coupon."""
        query = """
            DELETE FROM Coupons
            WHERE coupons_id = %s;
        """
        return self._execute_query(query, (coupons_id,))

    def get_by_code(self, discount_code: str) -> Optional[CouponsData]:
        """Get a coupon by discount code."""
        query = """
            SELECT discount_code, discount_value, expiration_date
            FROM Coupons
            WHERE discount_code = %s;
        """
        try:
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, (discount_code,))
            coupon_data = cursor.fetchone()
            cursor.close()
            if coupon_data:
                return CouponsData(*coupon_data)
            return None
        except Exception as e:
            print(f"Error getting coupon by code: {e}")
            return None