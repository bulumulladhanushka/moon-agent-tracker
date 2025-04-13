from flask import Flask, request, jsonify
import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Database config
db_config = {
    'user': os.environ.get('DB_USERNAME'),
    'password': os.environ.get('DB_PASSWORD'),
    'host': os.environ.get('DB_HOST'),
    'database': os.environ.get('DB_NAME'),
    'port': int(os.environ.get('DB_PORT', 3306))
}

@app.route('/')
def home():
    print("Home route hit")
    return "Welcome to the Integration Service!"

@app.route('/agents', methods=['POST'])
def create_agent():
    data = request.get_json(force=True)
    print("Received data:", data)

    print("🚀 Starting Agent Onboarding")
    required_fields = ['name', 'email', 'phone', 'region', 'status']
    if not all(field in data and data[field] for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Insert new agent (auto-generates agent_code via trigger)
        insert_query = """
            INSERT INTO agent (name, email, phone, region, status)
            VALUES (%s, %s, %s, %s, %s)
        """
        values = (data['name'], data['email'], data['phone'], data['region'], data['status'])
        cursor.execute(insert_query, values)
        connection.commit()

        agent_id = cursor.lastrowid

        # Fetch agent_code using agent_id
        print(f"Executing query: SELECT agent_code FROM agent WHERE agent_id = {agent_id}")  #change 1
        cursor.execute("SELECT agent_code FROM agent WHERE agent_id = %s", (agent_id,))
        agent_code_result = cursor.fetchone()

        if agent_code_result:
            return jsonify({
                "message": "Agent created successfully",
                "agent_id": agent_id,
                "agent_code": agent_code_result[0]
            }), 201
        else:
            return jsonify({"error": "Agent created but agent_code not found"}), 500

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
