import oracledb
import csv

# --- SETUP ---
LIB_DIR = r"C:\oracle\instantclient_21_3"  # Your Instant Client Path
DB_USER = "your_username"
DB_PASS = "your_password"
DB_DSN  = "host:port/service_name"

# Initialize Thick Mode (Required for FreeSQL/Cloud)
oracledb.init_oracle_client(lib_dir=LIB_DIR)

def bulk_load_csv(file_path):
    try:
        # 1. Connect
        conn = oracledb.connect(user=DB_USER, password=DB_PASS, dsn=DB_DSN)
        cursor = conn.cursor()
        
        # 2. Read CSV Data into a List
        with open(file_path, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)  # Skip the header row
            data_to_insert = [row for row in reader]

        # 3. Prepare Bulk Insert SQL
        # :1 and :2 correspond to the values in each row of your list
        sql = "INSERT INTO students (name, email) VALUES (:1, :2)"

        # 4. Execute Batch
        print(f"Starting bulk load of {len(data_to_insert)} rows...")
        cursor.executemany(sql, data_to_insert)
        
        # 5. Commit Changes
        conn.commit()
        print(f"Successfully loaded {cursor.rowcount} rows into the database.")

    except Exception as e:
        print(f"Error during bulk load: {e}")
        if 'conn' in locals():
            conn.rollback() # Undo changes if an error occurs

    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()

# Run the function
bulk_load_csv('students_data.csv')