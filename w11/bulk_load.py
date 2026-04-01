import oracledb
import csv
import os

# --- SETUP ---
LIB_DIR = r"C:\oracle\instantclient_21_3"
DB_USER = "FRANK2006DAVID_SCHEMA_0JBG4"
DB_PASS = "60QRJVO63EX!MIvDDOQ61UPNWR8K1E"
DB_DSN  = "db.freesql.com:1521/23ai_34ui2"

# CSV DIRECTORY (same as preprocess output)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_DIR = os.path.join(BASE_DIR, "csv")

# Initialize Oracle Client
oracledb.init_oracle_client(lib_dir=LIB_DIR)

def bulk_load_csv(table_name, file_path):
    try:
        conn = oracledb.connect(user=DB_USER, password=DB_PASS, dsn=DB_DSN)
        cursor = conn.cursor()

        with open(file_path, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            headers = next(reader)

            data_to_insert = [row for row in reader]

        if not data_to_insert:
            print(f"{table_name}: No data to insert.")
            return

        # Create dynamic placeholders (:1, :2, ...)
        num_cols = len(headers)
        placeholders = ", ".join([f":{i+1}" for i in range(num_cols)])

        sql = f"INSERT INTO {table_name} VALUES ({placeholders})"

        print(f"{table_name}: Inserting {len(data_to_insert)} rows...")
        cursor.executemany(sql, data_to_insert)

        conn.commit()
        print(f"{table_name}: {cursor.rowcount} rows inserted.")

    except Exception as e:
        print(f"{table_name}: Error -> {e}")
        if 'conn' in locals():
            conn.rollback()

    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()


# LOAD ALL TABLES IN ORDER 
def load_all():
    # Order matters because of foreign keys
    load_order = [
        "Customer",
        "Restaurant",
        "Driver",
        "MenuItem",
        "Food_Order",
        "OrderItem",
        "Payment",
        "Review"
    ]

    for table in load_order:
        file_path = os.path.join(CSV_DIR, f"{table}.csv")

        if not os.path.exists(file_path):
            print(f"{table}: CSV file not found, skipping.")
            continue

        bulk_load_csv(table, file_path)


if __name__ == "__main__":
    load_all()