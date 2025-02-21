from flask import Flask, render_template, jsonify, request
import os 
import time
import mysql.connector
import db_handler

db_config = {
    "host": os.environ.get("DATABASE_HOST", "localhost"),
    "user": os.environ.get("DATABASE_USER", "root"),
    "password": os.environ.get("DATABASE_PASSWORD", "rootpassword"),
    "database": os.environ.get("DATABASE_NAME", "car_maintenance")
}

db_handler.create_tables_if_missing()


def initialize_database():
    """Checks if tables exist and creates them if missing."""
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    # Check if cars table exists
    cursor.execute("SHOW TABLES LIKE 'cars'")
    result = cursor.fetchone()
    if not result:
        print("⚠️ Tables missing! Run `init.sql` manually or restart MySQL.")

    cursor.close()
    connection.close()



# Retry database connection until MySQL is ready
attempts = 10
while attempts > 0:
    try:
        connection = mysql.connector.connect(**db_config)
        print("✅ Successfully connected to MySQL!")
        break
    except mysql.connector.Error as e:
        print(f"⏳ MySQL not ready, retrying in 5 seconds... ({attempts} attempts left)")
        time.sleep(5)
        attempts -= 1

if attempts == 0:
    print("❌ Could not connect to MySQL. Exiting.")
    exit(1)  # Exit Flask if DB connection fails

# Run table check on startup
initialize_database()

app = Flask(__name__) # Create a instance of Flask

@app.route("/")
def home():
    return "<h1> Car Maintenance Tracker </h1>"

# ✅ Add a new car
@app.route("/add_car", methods=["POST"])
def add_car():
    data = request.json
    car_id = db_handler.add_car(data["make"], data["model"], data["year"], data["vin"])
    if car_id:
        return jsonify({"message": "Car added successfully!", "car_id": car_id}), 201
    return jsonify({"error": "Failed to add car"}), 500

# ✅ Get all cars
@app.route("/cars", methods=["GET"])
def get_cars():
    cars = db_handler.get_all_cars()
    return jsonify(cars)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)