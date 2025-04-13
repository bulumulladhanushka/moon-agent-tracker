import os
from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

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
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USERNAME'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME'),
            port=int(os.getenv('DB_PORT', 3306))
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
    app.run(host='0.0.0.0', port=5002,debug=True)
