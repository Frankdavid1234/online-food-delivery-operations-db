import oracledb

# --- CONFIGURATION ---

# MUST be a valid, modern Instant Client path (NOT 11.2)
LIB_DIR = r"C:\oracle\instantclient_23_0"

DB_USER = "FRANK2006DAVID_SCHEMA_0JBG4"
DB_PASS = "60QRJVO63EX!MIvDDOQ61UPNWR8K1E"
DB_DSN  = "db.freesql.com:1521/23ai_34ui2"


# --- INITIALIZE THICK MODE ---
try:
    oracledb.init_oracle_client(lib_dir=LIB_DIR)
except Exception as e:
    print(f"Oracle Client init failed: {e}")
    exit()


# --- CONNECT ---
try:
    conn = oracledb.connect(
        user=DB_USER,
        password=DB_PASS,
        dsn=DB_DSN
    )
    cursor = conn.cursor()
    print("Connected to Oracle Database")

except Exception as e:
    print(f"Connection failed: {e}")
    exit()


# --- CREATE ---
def create_record(name, email):
    try:
        sql = "INSERT INTO students (name, email) VALUES (:1, :2)"
        cursor.execute(sql, [name, email])
        conn.commit()
        print(f"Created record for {name}")
    except Exception as e:
        print(f"Insert failed: {e}")


# --- READ ---
def read_records():
    print("\n--- Student Directory ---")
    try:
        cursor.execute("SELECT name, email FROM students")
        rows = cursor.fetchall()

        if not rows:
            print("No records found.")
        else:
            for row in rows:
                print(f"Name: {row[0]} | Email: {row[1]}")
    except Exception as e:
        print(f"Read failed: {e}")


# --- UPDATE ---
def update_email(old_email, new_email):
    try:
        sql = "UPDATE students SET email = :1 WHERE email = :2"
        cursor.execute(sql, [new_email, old_email])

        if cursor.rowcount > 0:
            conn.commit()
            print(f"Updated email from {old_email} to {new_email}")
        else:
            print("No matching record found.")
    except Exception as e:
        print(f"Update failed: {e}")


# --- DELETE ---
def delete_record(student_email):
    try:
        sql = "DELETE FROM students WHERE email = :1"
        cursor.execute(sql, [student_email])

        if cursor.rowcount > 0:
            conn.commit()
            print(f"Deleted Student {student_email}")
        else:
            print("No matching record found.")
    except Exception as e:
        print(f"Delete failed: {e}")

