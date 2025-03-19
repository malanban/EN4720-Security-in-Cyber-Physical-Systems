import mysql.connector

class APIDatabase:
    # Database Configuration
    DB_CONFIG = {
        "host": "localhost",
        "user": "root",
        "password": "Concy@280200",
        "database": "cyber_security"
    }
    
    query = """
    SELECT 
    k.key_type,
    k.key_size,
    CASE 
        WHEN k.key_type = 'RSA' THEN r.public_key
        WHEN k.key_type = 'AES' THEN a.key_value
        ELSE NULL
    END AS public_key_or_value,
    CASE 
        WHEN k.key_type = 'RSA' THEN r.private_key
        ELSE NULL
    END AS private_key
    FROM key_id_type k
    LEFT JOIN rsa r ON k.key_id = r.key_id AND k.key_type = 'RSA'
    LEFT JOIN aes a ON k.key_id = a.key_id AND k.key_type = 'AES'
    WHERE k.key_id = %s
    """

    @staticmethod
    def check_database_exists():
        """Check if the database exists."""
        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(
                host=APIDatabase.DB_CONFIG["host"], 
                user=APIDatabase.DB_CONFIG["user"], 
                password=APIDatabase.DB_CONFIG["password"]
            )
            cursor = conn.cursor()
            cursor.execute("SHOW DATABASES")
            databases = [db[0] for db in cursor.fetchall()]
            return APIDatabase.DB_CONFIG["database"] in databases
        except mysql.connector.Error as err:
            print(f"Database Connection Error: {err}")
            return False
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    @staticmethod
    def check_table_exists():
        """Check if the required table exists."""
        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(**APIDatabase.DB_CONFIG)
            cursor = conn.cursor()
            cursor.execute("SHOW TABLES")
            tables = [table[0] for table in cursor.fetchall()]
            return "key_id_type" in tables
        except mysql.connector.Error as err:
            print(f"Table Check Error: {err}")
            return False
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    @staticmethod
    def insert_key(key_type, key_size, key_value_1, key_value_2=None):
        """Inserts a new encryption key into the database."""
        if not APIDatabase.check_database_exists():
            return {"error": "Database does not exist"}
        
        if not APIDatabase.check_table_exists():
            return {"error": "Table does not exist"}
    
        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(**APIDatabase.DB_CONFIG)
            cursor = conn.cursor()
    
            insert_key_id_type_query = """
            INSERT INTO key_id_type (key_type, key_size)
            VALUES (%s, %s)
            """
            cursor.execute(insert_key_id_type_query, (key_type, key_size))
            key_id = cursor.lastrowid
    
            if key_type.upper() == "AES":
                insert_aes_query = """
                INSERT INTO aes (key_id, key_value)
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE key_value = VALUES(key_value)
                """
                cursor.execute(insert_aes_query, (key_id, key_value_1))
                conn.commit()
                print(f"Successfully inserted: key_id={key_id}, key_type={key_type}, key_value={key_value_1} into tables.")
    
                return {
                    "key_id": key_id,
                    "key_value": key_value_1
                }
    
            elif key_type.upper() == "RSA":
                insert_rsa_query = """
                INSERT INTO rsa (key_id, public_key, private_key)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE public_key = VALUES(public_key), private_key = VALUES(private_key)
                """
                cursor.execute(insert_rsa_query, (key_id, key_value_1, key_value_2))
                conn.commit()
                print(f"Successfully inserted: key_id={key_id}, key_type={key_type}, public_key={key_value_1}, private_key={key_value_2} into tables.")
    
                return {
                    "key_id": key_id,
                    "public_key": key_value_1,
                    "private_key": key_value_2
                }
    
        except mysql.connector.Error as err:
            return {"error": f"Database error: {err}"}
    
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    @staticmethod
    def get_key_by_id(key_id):
        """Fetches key_type, key_value, and key_size using key_id."""
        if not APIDatabase.check_database_exists():
            return {"error": "Database does not exist"}
    
        if not APIDatabase.check_table_exists():
            return {"error": "Table does not exist"}
    
        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(**APIDatabase.DB_CONFIG)
            cursor = conn.cursor()
    
            cursor.execute(APIDatabase.query, (key_id,))
            result = cursor.fetchone()
    
            if result:
                key_type, key_size, key_value_1, key_value_2 = result
                return {
                    'key_type': key_type,
                    'key_size': key_size,
                    'key_value_1': key_value_1,
                    'key_value_2': key_value_2
                }
            else:
                return {"error": "Key ID not found"}
    
        except mysql.connector.Error as err:
            return {"error": f"Database error: {err}"}
    
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
