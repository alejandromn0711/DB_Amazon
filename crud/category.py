from typing import List, Optional
from pydantic import BaseModel, EmailStr, validator

from database_connection import PostgresDatabaseConnection

class CategoryData(BaseModel):
    """Data structure for Category."""
    categoryname: str
    description: Optional[str] = None  # Descripción opcional

class CategoryCRUD:

    def __init__(self):
        self.db_connection = PostgresDatabaseConnection()
        self.db_connection.connect()

    def _execute_query(self, query: str, values: tuple = None) -> bool:
        try:
            cursor = self.db_connection.connection.cursor()
            if values:
                cursor.execute(query, values)
            else:
                cursor.execute(query) #For queries without values.
            self.db_connection.connection.commit()
            cursor.close()
            return True #Indicate that the operation was successful.
        except Exception as e:
            print(f"Error in database operation: {e}")
            self.db_connection.connection.rollback() #Revert changes in case of error.
            return False

    def create(self, data: CategoryData) -> Optional[int]:
        """Creates a new category."""
        query = """
            INSERT INTO Category (categoryname, description)
            VALUES (%s, %s)
            RETURNING category_id;
        """
        values = (data.categoryname, data.description)
        try:
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, values)
            category_id = cursor.fetchone()[0]
            self.db_connection.connection.commit()
            cursor.close()
            return category_id
        except Exception as e:
            self.db_connection.connection.rollback()
            print(f"Error creating category: {e}")
            return None

    def get_by_id(self, category_id: int) -> Optional[CategoryData]:
        """Gets a category by ID."""
        query = """
            SELECT categoryname, description
            FROM Category
            WHERE category_id = %s;
        """
        try:
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, (category_id,))
            category_data = cursor.fetchone()
            cursor.close()
            if category_data:
                # La corrección está aquí: Crear un diccionario
                category_dict = {
                    "categoryname": category_data[0],
                    "description": category_data[1]
                }
                return CategoryData(**category_dict) #Doble ** para diccionario
            return None
        except Exception as e:
            print(f"Error getting category by ID: {e}")
            return None

    def get_all(self) -> List[CategoryData]:
        """Gets all categories."""
        query = """
            SELECT categoryname, description
            FROM Category;
        """
        categories = []
        try:
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query)
            category_list = cursor.fetchall()
            cursor.close()
            for category_data in category_list:  # Iteramos sobre las tuplas
                # La corrección está aquí: Crear un diccionario para cada tupla
                category_dict = {
                    "categoryname": category_data[0],
                    "description": category_data[1]
                }
                categories.append(CategoryData(**category_dict)) #Doble ** para diccionario
            return categories
        except Exception as e:
            print(f"Error getting all categories: {e}")
            return []

    def update(self, category_id: int, data: CategoryData) -> bool:
        """Updates a category."""
        query = """
            UPDATE Category
            SET categoryname = %s, description = %s
            WHERE category_id = %s;
        """
        values = (data.categoryname, data.description, category_id)
        return self._execute_query(query, values)

    def delete(self, category_id: int) -> bool:
        """Deletes a category."""
        query = """
            DELETE FROM Category
            WHERE category_id = %s;
        """
        return self._execute_query(query, (category_id,))

    def get_by_name(self, categoryname: str) -> List[CategoryData]:
        """Gets categories by name (case-insensitive search)."""
        query = """
            SELECT categoryname, description
            FROM Category
            WHERE LOWER(categoryname) LIKE LOWER(%s);
        """
        categories = []
        try:
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, ("%" + categoryname + "%",))  # Wildcard para búsqueda parcial
            category_list = cursor.fetchall()
            cursor.close()
            for category_data in category_list:
                category_dict = {
                    "categoryname": category_data[0],  # Usar "name" si es el nombre de la columna
                    "description": category_data[1]
                }
                categories.append(CategoryData(**category_dict))  # Corrección importante
            return categories
        except Exception as e:
            print(f"Error getting categories by name: {e}")
            return []