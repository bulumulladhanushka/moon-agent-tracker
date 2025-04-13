from flask import Flask, request, jsonify
import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Database configuration from environment variables
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

@app.route('/target-reminder', methods=['POST'])
def send_target_reminder():
    data = request.get_json(force=True)
    print("Received target reminder request:", data)

    required_fields = ['agent_code', 'target_sales']
    if not all(field in data and data[field] for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Check if agent exists
        cursor.execute("SELECT agent_id FROM agent WHERE agent_code = %s", (data['agent_code'],))
        agent_result = cursor.fetchone()

        if not agent_result:
            return jsonify({"error": "Agent code not found"}), 404

        # Fetch total sales using agent_code
        cursor.execute("""
            SELECT SUM(sale_amount)
            FROM sales
            WHERE agent_code = %s
        """, (data['agent_code'],))
        total_sales = cursor.fetchone()[0] or 0

        if total_sales >= data['target_sales']:
            return jsonify({"message": f"Agent {data['agent_code']} has achieved the sales target of {data['target_sales']}!"}), 200
        else:
            return jsonify({"message": f"Agent {data['agent_code']} has not met the sales target. Current sales: {total_sales}."}), 200

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
