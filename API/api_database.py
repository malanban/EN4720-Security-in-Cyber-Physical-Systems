import mysql.connector

# Database Configuration
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "database": "cyber_security"
}

def check_database_exists():
    """Check if the database exists."""
    try:
        conn = mysql.connector.connect(host=DB_CONFIG["host"], user=DB_CONFIG["user"], password=DB_CONFIG["password"])
        cursor = conn.cursor()
        cursor.execute("SHOW DATABASES")
        databases = [db[0] for db in cursor.fetchall()]
        return DB_CONFIG["database"] in databases
    except mysql.connector.Error as err:
        print(f"Database Connection Error: {err}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def check_table_exists():
    """Check if the required table exists."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES")
        tables = [table[0] for table in cursor.fetchall()]
        return "key_id_value" in tables
    except mysql.connector.Error as err:
        print(f"Table Check Error: {err}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def insert_key(key_type, key_size, key_value):
    """Inserts a new encryption key into the database."""
    if not check_database_exists():
        return {"error": "Database not exist"}
    
    if not check_table_exists():
        return {"error": "Table is not existing"}

    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        sql = "INSERT INTO key_id_value (key_type, key_size, key_value) VALUES (%s, %s, %s)"
        values = (key_type, key_size, key_value)
        cursor.execute(sql, values)
        conn.commit()

        return {"success": "Key inserted successfully"}

    except mysql.connector.Error as err:
        return {"error": f"Database error: {err}"}

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def get_key_by_id(key_id):
    """Fetches key_type, key_value, and key_size using key_id."""
    if not check_database_exists():
        return {"error": "Database not exist"}

    if not check_table_exists():
        return {"error": "Table is not existing"}

    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)

        sql = "SELECT * FROM key_id_value WHERE key_id = %s"
        cursor.execute(sql, (key_id,))
        result = cursor.fetchone()

        return result if result else {"error": "Key ID not found"}

    except mysql.connector.Error as err:
        return {"error": f"Database error: {err}"}

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# Example Usage
print(insert_key("AES", 256, "bXlTZWNyZXRLZXk="))  # Insert Example Key
print(get_key_by_id(18))  # Retrieve Key with ID 1
