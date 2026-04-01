'''
If you are running this code first time, and you don't have streamlit installed, then follow this instruction:
1. open a terminal
2. enter this command
    pip install streamlit

'''

import streamlit as st
import oracledb

# --- DATABASE SETUP ---
# Update this path to your local Instant Client folder
LIB_DIR = r"C:\Users\fmoya9845\Downloads\instantclient_11_2"
DB_USER = "FRANK2006DAVID_SCHEMA_0JBG4" # or your FreeSQL username
DB_PASS = "60QRJVO63EX!MIvDDOQ61UPNWR8K1E" # your password for the dbms user
DB_DSN  = "db.freesql.com:1521/23ai_34ui2" # or your FreeSQL DSN

# Initialize Oracle Client for Thick Mode
@st.cache_resource
def init_db():
    if LIB_DIR:
        try:
            oracledb.init_oracle_client(lib_dir=LIB_DIR)
        except Exception as e:
            st.error(f"Error initializing Oracle Client: {e}")


init_db()


def get_connection():
    return oracledb.connect(user=DB_USER, password=DB_PASS, dsn=DB_DSN)


# --- STREAMLIT UI ---
st.title("Florida Poly Student Database")
st.subheader("CRUD Operations (PK: Email)")

menu = ["Create", "Read", "Update", "Delete"]
choice = st.sidebar.selectbox("Select Action", menu)

# --- CREATE ---
if choice == "Create":
    st.write("### Add a New Student")
    email = st.text_input("Email Address (Primary Key)")
    name = st.text_input("Full Name")

    if st.button("Add Student"):
        try:
            conn = get_connection()
            cur = conn.cursor()
            # Note: email is first to match your input logic or the table structure
            cur.execute("INSERT INTO students (email, name) VALUES (:1, :2)", [email, name])
            conn.commit()
            cur.close()
            conn.close()
            st.success(f"Successfully added {name}!")
        except Exception as e:
            st.error(f"Error: {e}")

# --- READ ---
elif choice == "Read":
    st.write("### Student Directory")
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT email, name FROM students")
        data = cur.fetchall()
        cur.close()
        conn.close()

        if data:
            st.table(data)
        else:
            st.info("No records found.")
    except Exception as e:
        st.error(f"Error: {e}")

# --- UPDATE ---
elif choice == "Update":
    st.write("### Update Student Name")
    email_to_update = st.text_input("Enter the Student Email to find them")
    new_name = st.text_input("Enter the New Name")

    if st.button("Update Name"):
        try:
            conn = get_connection()
            cur = conn.cursor()
            # Update NAME where EMAIL matches
            cur.execute("UPDATE students SET name = :1 WHERE email = :2", [new_name, email_to_update])

            if cur.rowcount > 0:
                conn.commit()
                st.success(f"Record updated for {email_to_update}")
            else:
                st.warning("No student found with that email.")

            cur.close()
            conn.close()
        except Exception as e:
            st.error(f"Error: {e}")

# --- DELETE ---
elif choice == "Delete":
    st.write("### Remove a Student")
    email_to_delete = st.text_input("Enter Student Email to Delete")

    if st.button("Delete"):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("DELETE FROM students WHERE email = :1", [email_to_delete])

            if cur.rowcount > 0:
                conn.commit()
                st.warning(f"Student with email {email_to_delete} removed.")
            else:
                st.info("No student found with that email.")

            cur.close()
            conn.close()
        except Exception as e:
            st.error(f"Error: {e}")

# run using: streamlit run app.py

