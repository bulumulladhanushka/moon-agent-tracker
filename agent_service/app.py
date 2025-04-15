from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# MySQL connection
def get_db_connection():
    connection = mysql.connector.connect(
    host='mooninsurance.ca7isqgecjpt.us-east-1.rds.amazonaws.com',
    port=3306,
    user='admin',
    password='Hsnmef_9575$',
    database='mooninsurance_db'

    )
    return connection

@app.route('/agent', methods=['POST'])
def create_agent():
    data = request.get_json()
    email = data.get('email')
    name = data.get('name')
    phone = data.get('phone')
    region = data.get('region')
    status = data.get('status')

    if not email or not name or not phone or not region or not status:
        return jsonify({"error": "All fields are required"}), 400

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO agent (email, name, phone, region, status)
        VALUES (%s, %s, %s, %s, %s)
    """, (email, name, phone, region, status))
    connection.commit()
    connection.close()

    return jsonify({"message": "Agent created successfully"}), 201

@app.route('/agent', methods=['GET'])
def get_agent():
    email = request.args.get('email')
    if not email:
        return jsonify({"error": "Email parameter is required"}), 400

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM agent WHERE email = %s", (email,))
    agent = cursor.fetchone()
    connection.close()

    if agent:
        return jsonify({
            "agent_id": agent[0],
            "agent_code": agent[1],
            "name": agent[2],
            "email": agent[3],
            "phone": agent[4],
            "region": agent[5],
            "status": agent[6],
            "created_at": agent[7]
        })
    else:
        return jsonify({"error": "Agent not found"}), 404

@app.route('/agent', methods=['PUT'])
def update_agent():
    data = request.get_json()

    agent_id = data.get('agent_id')
    email = data.get('email')
    name = data.get('name')
    phone = data.get('phone')
    region = data.get('region')
    status = data.get('status')

    if not agent_id or not email or not name or not phone or not region or not status:
        return jsonify({"error": "All fields are required"}), 400

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("""
        UPDATE agent
        SET name = %s, email = %s, phone = %s, region = %s, status = %s
        WHERE agent_id = %s
    """, (name, email, phone, region, status, agent_id))
    connection.commit()
    connection.close()

    return jsonify({"message": "Agent updated successfully"})

@app.route('/agent', methods=['DELETE'])
def delete_agent():
    email = request.args.get('email')
    if not email:
        return jsonify({"error": "Email parameter is required"}), 400

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM agent WHERE email = %s", (email,))
    connection.commit()
    connection.close()

    return jsonify({"message": "Agent deleted successfully"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
