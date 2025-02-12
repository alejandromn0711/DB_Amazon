from typing import List, Optional
from pydantic import BaseModel

from database_connection import PostgresDatabaseConnection

class SearchHistoryData(BaseModel):
    """Data structure for SearchHistory."""
    search_term: str
    search_date: str  # ISO 8601 format is recommended (YYYY-MM-DD)
    customer_id: int    # Foreign key

class SearchHistoryCRUD:

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

    def create(self, data: SearchHistoryData) -> Optional[int]:
        """Creates a new search history entry."""
        query = """
            INSERT INTO SearchHistory (search_term, search_date, customer_id)
            VALUES (%s, %s, %s)
            RETURNING searchHistory_id;
        """
        values = (data.search_term, data.search_date, data.customer_id)
        try:
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, values)
            search_history_id = cursor.fetchone()[0]
            self.db_connection.connection.commit()
            cursor.close()
            return search_history_id
        except Exception as e:
            self.db_connection.connection.rollback()
            print(f"Error creating search history entry: {e}")
            return None

    def get_by_id(self, search_history_id: int) -> Optional[SearchHistoryData]:
        """Gets a search history entry by ID."""
        query = """
            SELECT search_term, search_date, customer_id
            FROM SearchHistory
            WHERE searchHistory_id = %s;
        """
        try:
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, (search_history_id,))
            search_history_data = cursor.fetchone()
            cursor.close()
            if search_history_data:
                return SearchHistoryData(*search_history_data)
            return None
        except Exception as e:
            print(f"Error getting search history entry by ID: {e}")
            return None

    def get_all(self) -> List[SearchHistoryData]:
        """Gets all search history entries."""
        query = """
            SELECT search_term, search_date, customer_id
            FROM SearchHistory;
        """
        search_history_entries = []
        try:
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query)
            search_history_list = cursor.fetchall()
            cursor.close()
            for search_history_entry in search_history_list:
                search_history_entries.append(SearchHistoryData(*search_history_entry))
            return search_history_entries
        except Exception as e:
            print(f"Error getting all search history entries: {e}")
            return []

    def update(self, search_history_id: int, data: SearchHistoryData) -> bool:
        """Updates a search history entry."""
        query = """
            UPDATE SearchHistory
            SET search_term = %s, search_date = %s, customer_id = %s
            WHERE searchHistory_id = %s;
        """
        values = (data.search_term, data.search_date, data.customer_id, search_history_id)
        return self._execute_query(query, values)

    def delete(self, search_history_id: int) -> bool:
        """Deletes a search history entry."""
        query = """
            DELETE FROM SearchHistory
            WHERE searchHistory_id = %s;
        """
        return self._execute_query(query, (search_history_id,))

    # Puedes agregar métodos adicionales según sea necesario, por ejemplo:
    # get_by_customer, get_by_term, etc.
