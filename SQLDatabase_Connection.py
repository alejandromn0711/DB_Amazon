import mysql.connector

class MySQLDatabaseConnection:
    """This class is responsible for connecting to the MySQL database."""

    def __init__(self):
        self._dbname = "amazon"
        self._duser = "usql"
        self._dpass = "admin123"
        self._dhost = "localhost"
        self._dport = "3306"
        self.connection = None

    def connect(self):
        """This method connects to the database."""
        try:
            self.connection = mysql.connector.connect(
                database=self._dbname,
                user=self._duser,
                password=self._dpass,
                host=self._dhost,
                port=self._dport
            )
            print("✅ MySQL connection successful!")
        except Exception as e:
            print(f"❌ MySQL connection failed: {e}")

    def test_query(self):
        """This method tests a simple query to check the connection."""
        if self.connection:
            try:
                cursor = self.connection.cursor()
                cursor.execute("SHOW TABLES;")
                tables = cursor.fetchall()
                print("📋 Tables in 'amazon' database:", tables)
            except Exception as e:
                print(f"❌ MySQL query failed: {e}")
        else:
            print("⚠️ No active MySQL connection.")

    def close(self):
        """This method closes the database connection."""
        if self.connection:
            self.connection.close()
            print("🔌 MySQL connection closed.")

# Test the MySQL connection
if __name__ == "__main__":
    db = MySQLDatabaseConnection()
    db.connect()
    db.test_query()
    db.close()