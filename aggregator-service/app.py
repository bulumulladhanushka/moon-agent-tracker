import os
import mysql.connector
from flask import Flask, jsonify

app = Flask(__name__)

# DB config...
DB_HOST = os.getenv('DB_HOST', 'mooninsurance.ca7isqgecjpt.us-east-1.rds.amazonaws.com')
DB_PORT = int(os.getenv('DB_PORT', 3306))
DB_NAME = os.getenv('DB_NAME', 'mooninsurance_db')
DB_USER = os.getenv('DB_USER', 'admin')
DB_PASS = os.getenv('DB_PASS', 'Hsnmef_9575$')

def get_db_connection():
    return mysql.connector.connect(
        host=DB_HOST, port=DB_PORT,
        user=DB_USER, password=DB_PASS,
        database=DB_NAME
    )

@app.route('/aggregates/best-agents', methods=['GET'])
def best_agents(): return jsonify(fetch_best_agents())
@app.route('/aggregates/best-regions', methods=['GET'])
def best_regions(): return jsonify(fetch_best_regions())
@app.route('/aggregates/top-products', methods=['GET'])
def top_products(): return jsonify(fetch_top_products())
@app.route('/aggregates/region-performance', methods=['GET'])
def region_performance(): return jsonify(fetch_region_performance())

def fetch_best_agents():
    conn = get_db_connection()
    cur  = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT a.agent_code, a.name, SUM(s.sale_amount) AS total_sales
          FROM sales s JOIN agent a ON s.agent_code = a.agent_code
         GROUP BY a.agent_code, a.name
         ORDER BY total_sales DESC LIMIT 5
    """)
    rows = cur.fetchall(); cur.close(); conn.close()
    return rows

def fetch_best_regions():
    conn = get_db_connection()
    cur  = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT a.region, SUM(s.sale_amount) AS total_sales
          FROM sales s JOIN agent a ON s.agent_code = a.agent_code
         GROUP BY a.region ORDER BY total_sales DESC LIMIT 5
    """)
    rows = cur.fetchall(); cur.close(); conn.close()
    return rows

def fetch_top_products():
    conn = get_db_connection()
    cur  = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT p.product_name, COUNT(*) AS sales_count
          FROM sales s JOIN product p ON s.product_id = p.product_id
         WHERE s.sale_amount >= 100
      GROUP BY p.product_name
      ORDER BY sales_count DESC LIMIT 5
    """)
    rows = cur.fetchall(); cur.close(); conn.close()
    return rows

def fetch_region_performance():
    conn = get_db_connection()
    cur  = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT a.region, AVG(s.sale_amount) AS avg_sale
          FROM sales s JOIN agent a ON s.agent_code = a.agent_code
         GROUP BY a.region
    """)
    rows = cur.fetchall(); cur.close(); conn.close()
    return rows

if __name__ == '__main__':
    run_mode = os.getenv('RUN_MODE', 'server')
    if run_mode == 'server':
        port = int(os.getenv('PORT', 5004))
        app.run(host='0.0.0.0', port=port)
    else:
        print("\n[Aggregator CronJob Execution]")
        print("Best Agents:", fetch_best_agents())
        print("Best Regions:", fetch_best_regions())
        print("Top Products:", fetch_top_products())
        print("Region Performance:", fetch_region_performance())
        exit(0)
