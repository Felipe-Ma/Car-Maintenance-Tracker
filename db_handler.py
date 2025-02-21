import mysql.connector
import os

db_config = {
    "host": os.getenv("DATABASE_HOST", "db"),  # Matches MySQL service in docker-compose
    "user": os.getenv("DATABASE_USER", "root"),
    "password": os.getenv("DATABASE_PASSWORD", "rootpassword"),
    "database": os.getenv("DATABASE_NAME", "car_maintenance")
}


def get_db_connection():
    """Returns a connection to the database."""
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except mysql.connector.Error as e:
        print(f"Error connecting to database: {e}")
        return None
    
def add_car(make, model, year, vin):
    """Adds a car to the database."""
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            sql = "INSERT INTO cars (make, model, year, vin) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (make, model, year, vin))
            connection.commit()
            return cursor.lastrowid 
        except mysql.connector.Error as e:
            print(f"Error adding car: {e}")
        finally:
            cursor.close()
            connection.close()
    return None

def get_all_cars():
    """Returns a list of all cars in the database."""
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM cars ORDER BY created_at DESC")
            return cursor.fetchall()
        except mysql.connector.Error as e:
            print(f"Error getting cars: {e}")
        finally:
            cursor.close()
            connection.close()
    return []

def get_car_by_id(car_id):
    """Returns a car by its ID."""
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM cars WHERE id = %s", (car_id,))
            return cursor.fetchone()
        except mysql.connector.Error as e:
            print(f"Error getting car: {e}")
        finally:
            cursor.close()
            connection.close()
    return None

# 📌 Add a maintenance record
def add_maintenance(car_id, service_type_id, service_date, mileage, cost, notes, next_due_mileage):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            sql = """INSERT INTO maintenance_records 
                     (car_id, service_type_id, service_date, mileage, cost, notes, next_due_mileage) 
                     VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(sql, (car_id, service_type_id, service_date, mileage, cost, notes, next_due_mileage))
            connection.commit()
            return cursor.lastrowid  # Return new record ID
        except mysql.connector.Error as err:
            print(f"❌ Error adding maintenance record: {err}")
        finally:
            cursor.close()
            connection.close()
    return None

# 📌 Get maintenance history for a car
def get_maintenance_history(car_id):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            sql = """SELECT m.id, m.service_date, m.mileage, m.cost, m.notes, m.next_due_mileage, s.name AS service_name
                     FROM maintenance_records m
                     JOIN service_types s ON m.service_type_id = s.id
                     WHERE m.car_id = %s ORDER BY m.service_date DESC"""
            cursor.execute(sql, (car_id,))
            return cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"❌ Error fetching maintenance history: {err}")
        finally:
            cursor.close()
            connection.close()
    return []

# 📌 Retrieve all service types (for dropdowns in UI)
def get_all_service_types():
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM service_types ORDER BY name ASC")
            return cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"❌ Error fetching service types: {err}")
        finally:
            cursor.close()
            connection.close()
    return []

def create_tables_if_missing():
    """Ensures all necessary tables exist in the database."""
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()

            # Create cars table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS cars (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    make VARCHAR(50) NOT NULL,
                    model VARCHAR(50) NOT NULL,
                    year INT NOT NULL,
                    vin VARCHAR(20) UNIQUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)

            # Create service_types table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS service_types (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(50) UNIQUE NOT NULL
                );
            """)

            # Insert default service types if they don't exist
            cursor.execute("""
                INSERT IGNORE INTO service_types (name) VALUES
                ('Oil Change'), ('Tire Rotation'), ('Brake Inspection'), 
                ('Battery Replacement'), ('General Checkup');
            """)

            # Create maintenance_records table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS maintenance_records (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    car_id INT NOT NULL,
                    service_type_id INT NOT NULL,
                    service_date DATE NOT NULL,
                    mileage INT NOT NULL,
                    cost DECIMAL(10,2) NULL,
                    notes TEXT,
                    next_due_mileage INT NULL,
                    FOREIGN KEY (car_id) REFERENCES cars(id) ON DELETE CASCADE,
                    FOREIGN KEY (service_type_id) REFERENCES service_types(id) ON DELETE CASCADE
                );
            """)

            connection.commit()
            print("✅ Database tables checked/created successfully!")

        except mysql.connector.Error as err:
            print(f"❌ Error ensuring tables exist: {err}")
        finally:
            cursor.close()
            connection.close()


    


