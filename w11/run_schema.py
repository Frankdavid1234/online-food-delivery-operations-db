import oracledb

LIB_DIR = r"C:\oracle\instantclient_23_0"

DB_USER = "FRANK2006DAVID_SCHEMA_0JBG4"
DB_PASS = "60QRJVO63EX!MIvDDOQ61UPNWR8K1E"
DB_DSN  = "db.freesql.com:1521/23ai_34ui2"

SQL_FILE = "create_db.sql"   # <-- your file name

# init client
oracledb.init_oracle_client(lib_dir=LIB_DIR)

# connect
conn = oracledb.connect(user=DB_USER, password=DB_PASS, dsn=DB_DSN)
cursor = conn.cursor()

print("Running schema file...")

with open(SQL_FILE, "r") as f:
    sql_script = f.read()

# split statements by ;
statements = sql_script.split(";")

for stmt in statements:
    stmt = stmt.strip()
    if stmt:
        try:
            cursor.execute(stmt)
        except Exception as e:
            print(f"Error executing:\n{stmt}\n-> {e}")

conn.commit()
cursor.close()
conn.close()

print("Schema loaded.")