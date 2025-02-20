from flask import Flask, render_template # Flask 
import os 
import time
import mysql.connector

db_config = {
    "host": os.environ.get("DATABASE_HOST", "localhost"),
    "user": os.environ.get("DATABASE_USER", "root"),
    "password": os.environ.get("DATABASE_PASSWORD", "rootpassword"),
    "database": os.environ.get("DATABASE_NAME", "car_maintenance")
}

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

app = Flask(__name__) # Create a instance of Flask

@app.route("/")
def home():
    return "<h1> Car Maintenance Tracker </h1>"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)