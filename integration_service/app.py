import os
from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)


DB_HOST = "mooninsurance.ca7isqgecjpt.us-east-1.rds.amazonaws.com"
DB_PORT = 3306
DB_NAME = "mooninsurance_db"
DB_USERNAME = "admin"
DB_PASSWORD = "Hsnmef_9575$"

@app.route('/')
def home():
    print("Home route hit")
    return "Welcome to the Integration Service!"


@app.route('/sales', methods=['POST'])
def create_sale():
    data = request.get_json()
    print(f"Received data: {data}")

    connection = None
    cursor = None

    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USERNAME,
            password=DB_PASSWORD,
            database=DB_NAME,
            port=DB_PORT
        )

        if connection.is_connected():
            cursor = connection.cursor()
            query = """
                INSERT INTO sales (agent_code, product_id, sale_amount)
                VALUES (%s, %s, %s)
            """
            values = (
                data.get('agent_code'),
                data.get('product_id'),
                data.get('sale_amount')
            )
            cursor.execute(query, values)
            connection.commit()
            return jsonify({"message": "Sale recorded successfully!"}), 201
        else:
            return jsonify({"error": "Database connection failed."}), 500

    except Error as e:
        print(f"Database Error: {e}")
        return jsonify({"error": str(e)}), 500

    except Exception as e:
        print(f"Unexpected Error: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
