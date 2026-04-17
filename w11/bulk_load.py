import oracledb
import csv
import os

# --- SETUP ---
LIB_DIR = r"C:\oracle\instantclient_23_0"

DB_USER = "FRANK2006DAVID_SCHEMA_0JBG4"
DB_PASS = "60QRJVO63EX!MIvDDOQ61UPNWR8K1E"
DB_DSN  = "db.freesql.com:1521/23ai_34ui2"

# CSV DIRECTORY
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_DIR = os.path.join(BASE_DIR, "csv")

# --- INIT ORACLE CLIENT ---
oracledb.init_oracle_client(lib_dir=LIB_DIR)


# --- BULK LOAD FUNCTION ---
def bulk_load_csv(cursor, conn, table_name, file_path):
    try:
        table_name = table_name.upper()

        with open(file_path, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            headers = next(reader)

            # normalize headers
            headers = [h.lower().strip() for h in headers]

            # =========================
            # REMOVE PROBLEM COLUMNS
            # =========================
            remove_cols = {
                "customer": ["customer_id", "date_created"],
                "restaurant": ["restaurant_id"],
                "driver": ["driver_id"],
                "menuitem": ["menu_item_id"],
                "food_order": ["order_id", "order_date"],
                "orderitem": ["order_item_id"],
                "payment": ["payment_id", "payment_date"],
                "review": ["review_id", "review_date"]
            }

            # filter columns
            cols_to_keep = [
                col for col in headers
                if col not in remove_cols.get(table_name.lower(), [])
            ]

            # special fix for COMMENT column
            cols_sql = []
            for col in cols_to_keep:
                if col == "comment":
                    cols_sql.append('"COMMENT"')
                else:
                    cols_sql.append(col)

            # build index map
            indices = [headers.index(col) for col in cols_to_keep]

            # filter data rows
            data_to_insert = []
            for row in reader:
                filtered_row = [row[i] for i in indices]
                data_to_insert.append(filtered_row)

        if not data_to_insert:
            print(f"{table_name}: No data to insert.")
            return

        # =========================
        # BUILD SQL
        # =========================
        num_cols = len(cols_to_keep)
        placeholders = ", ".join([f":{i+1}" for i in range(num_cols)])
        columns = ", ".join(cols_sql)

        sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

        print(f"{table_name}: Inserting {len(data_to_insert)} rows...")

        cursor.executemany(sql, data_to_insert, batcherrors=True)

        errors = cursor.getbatcherrors()
        for err in errors:
            print(f"{table_name}: Row {err.offset} error: {err.message}")

        conn.commit()
        print(f"{table_name}: Insert complete.")

    except Exception as e:
        print(f"{table_name}: Fatal error -> {e}")
        conn.rollback()



# --- LOAD ALL TABLES ---
def load_all():
    try:
        conn = oracledb.connect(
            user=DB_USER,
            password=DB_PASS,
            dsn=DB_DSN
        )
        cursor = conn.cursor()

        print("Connected to Oracle Database")

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

            # ✅ FIXED CALL (this was your error)
            bulk_load_csv(cursor, conn, table, file_path)

        cursor.close()
        conn.close()
        print("\nAll tables processed. Connection closed.")

    except Exception as e:
        print(f"Connection failed: {e}")



load_all()