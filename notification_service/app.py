from flask import Flask, request, jsonify
import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

DB_HOST = "mooninsurance.ca7isqgecjpt.us-east-1.rds.amazonaws.com"
DB_PORT = 3306
DB_NAME = "mooninsurance_db"
DB_USERNAME = "admin"
DB_PASSWORD = "Hsnmef_9575$"

def create_db_connection():
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USERNAME,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        return connection
    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

@app.route('/')
def home():
    print("Home route hit")
    return "Welcome to the Notification Service!"

@app.route('/target-reminder', methods=['POST'])
def send_target_reminder():
    data = request.get_json()
    print(f"Received target reminder request: {data}")
    agent_code = data.get("agent_code")
    target_sales = data.get("target_sales")

    connection = create_db_connection()
    if not connection:
        return jsonify({"error": "Failed to connect to database"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT name, email FROM agent WHERE agent_code = %s"
        cursor.execute(query, (agent_code,))
        result = cursor.fetchone()

        if not result:
            return jsonify({"error": "Agent not found"}), 404

        agent_name = result["name"]
        email = result["email"]

        # Mock notification logic
        print(f"Sending reminder to {agent_name} ({email}) about target: {target_sales}")

        return jsonify({"message": f"Reminder sent to {agent_name} ({email})"}), 200

    except mysql.connector.Error as e:
        print(f"Query error: {e}")
        return jsonify({"error": "Database query failed"}), 500

    finally:
        if connection.is_connected():
            connection.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
