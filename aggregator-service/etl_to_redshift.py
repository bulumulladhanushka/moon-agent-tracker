import os
import mysql.connector
import psycopg2
from psycopg2.extras import execute_values
from datetime import datetime

# === RDS (MySQL) Connection ===
rds_conn = mysql.connector.connect(
    host=os.getenv('RDS_HOST', 'mooninsurance.ca7isqgecjpt.us-east-1.rds.amazonaws.com'),
    user=os.getenv('RDS_USER', 'admin'),
    password=os.getenv('RDS_PASSWORD', 'Hsnmef_9575$'),
    database=os.getenv('RDS_DB', 'mooninsurance_db'),
    port=int(os.getenv('RDS_PORT', 3306))
)
rds_cursor = rds_conn.cursor(dictionary=True)

# === Redshift Connection ===
redshift_conn = psycopg2.connect(
    host=os.getenv('REDSHIFT_HOST', 'mooninsurance-wg.457087769533.us-east-1.redshift-serverless.amazonaws.com'),
    user=os.getenv('REDSHIFT_USER', 'admin'),
    password=os.getenv('REDSHIFT_PASSWORD', 'Hsnmef_9575$'),
    dbname=os.getenv('REDSHIFT_DB', 'mooninsurance-red_db'),
    port=int(os.getenv('REDSHIFT_PORT', 5439))
)
redshift_cursor = redshift_conn.cursor()

# === ETL Query ===
aggregation_query = """
SELECT 
    d.agent_code,
    d.name,
    d.region,
    d.product_id,
    d.product_name,
    d.month,
    d.total_sales,
    e.product_target,
    e.target_month
FROM (
    SELECT 
        b.agent_code,
        b.name,
        b.region,
        a.product_id,
        c.product_name,
        DATE_FORMAT(a.sale_date, '%Y-%m-01') AS month,
        SUM(a.sale_amount) AS total_sales
    FROM sales a
    JOIN agent b ON a.agent_code = b.agent_code
    JOIN product c ON a.product_id = c.product_id
    GROUP BY 
        b.agent_code, b.name, b.region, 
        a.product_id, c.product_name, 
        DATE_FORMAT(a.sale_date, '%Y-%m-01')
) d
JOIN product_target e 
    ON d.product_id = e.product_id 
   AND d.month = e.target_month;
"""

# === Run Query in RDS ===
rds_cursor.execute(aggregation_query)
rows = rds_cursor.fetchall()

# === Transform and Insert into Redshift ===
insert_query = """
INSERT INTO product_vs_target (
    agent_code,
    name,
    region,
    product_id,
    product_name,
    month,
    total_sales,
    product_target,
    target_month,
    recorded_at
) VALUES %s
"""

data = []
for row in rows:
    data.append((
        row['agent_code'],
        row['name'],
        row['region'],
        row['product_id'],
        row['product_name'],
        row['month'],
        float(row['total_sales']),
        float(row['product_target']),
        row['target_month'],
        datetime.utcnow()
    ))


if data:
    execute_values(redshift_cursor, insert_query, data)
    redshift_conn.commit()
    print(f"✅ Inserted {len(data)} records into Redshift.")
else:
    print("ℹ️ No data to insert.")

# === Cleanup ===
rds_cursor.close()
rds_conn.close()
redshift_cursor.close()
redshift_conn.close()
