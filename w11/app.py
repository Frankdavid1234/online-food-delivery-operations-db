'''
if streamlit is not installed:
pip install streamlit
'''
import streamlit as st
import oracledb
import datetime

LIB_DIR = r"C:\Users\docto\OneDrive - Florida Polytechnic University\Florida Poly Stuff\Database\InClass\instantclient-basiclite-windows.x64-11.2.0.4.0\instantclient_11_2"
data_dir = r"C:\Users\docto\OneDrive - Florida Polytechnic University\Florida Poly Stuff\Database\Course Project\Part D\data"
DB_USER = "TCOCKERHAM3539_SCHEMA_0ZQNY"
DB_PASS = r"LU4YSUHWRO4IWRDPTMPG0oIHNDYQ$M"
DB_DSN = "db.freesql.com:1521/23ai_34ui2"

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

st.title("Food Delivery Database")
st.subheader("Feature Explorer")

menu = [
    "Search Orders by Date Range",
    "Filter Restaurants by Average Rating",
    "Sort Drivers by Deliveries",
    "Show Orders by Max Price",
    "Most Ordered Menu Item per Restaurant"
]
choice = st.sidebar.selectbox("Select Feature", menu)


if choice == "Search Orders by Date Range":
    st.write("### Search Orders by Date Range")
    st.write("Find all orders placed between two dates.")

    start_date = st.date_input("Start Date", value=datetime.date(2026, 1, 1))
    end_date = st.date_input("End Date", value=datetime.date(2026, 4, 30))

    if st.button("Search Orders"):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("""
                SELECT order_id, order_date, status, delivery_address, total_amount
                FROM Food_Order
                WHERE TRUNC(order_date) BETWEEN TO_DATE(:start_date, 'YYYY-MM-DD') AND TO_DATE(:end_date, 'YYYY-MM-DD')
                ORDER BY order_date DESC
                """, {"start_date": start_date.strftime('%Y-%m-%d'), "end_date": end_date.strftime('%Y-%m-%d')})
            data = cur.fetchall()
            cur.close()
            conn.close()

            if data:
                st.success(f"Found {len(data)} order(s).")
                st.table({
                    "Order ID":         [row[0] for row in data],
                    "Order Date":       [row[1] for row in data],
                    "Status":           [row[2] for row in data],
                    "Delivery Address": [row[3] for row in data],
                    "Total Amount ($)": [row[4] for row in data],
                })
            else:
                st.info("No orders found in that date range.")
        except Exception as e:
            st.error(f"Error: {e}")


elif choice == "Filter Restaurants by Average Rating":
    st.write("### Filter Restaurants by Average Rating")
    st.write("Find all restaurants at or above a minimum average review rating.")

    min_rating = st.slider("Minimum Average Rating", min_value=1.0, max_value=5.0, value=3.0, step=0.5)

    if st.button("Search Restaurants"):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("""
                SELECT r.restaurant_id, r.name, r.cuisine_type, ROUND(AVG(rv.rating), 2) AS avg_rating
                FROM Restaurant r
                JOIN Review rv ON r.restaurant_id = rv.restaurant_id
                GROUP BY r.restaurant_id, r.name, r.cuisine_type
                HAVING AVG(rv.rating) >= :min_rating
                ORDER BY avg_rating DESC
            """, {"min_rating": min_rating})
            data = cur.fetchall()
            cur.close()
            conn.close()

            if data:
                st.success(f"Found {len(data)} restaurant(s) with avg rating >= {min_rating}.")
                st.table({
                    "Restaurant ID": [row[0] for row in data],
                    "Name":          [row[1] for row in data],
                    "Cuisine Type":  [row[2] for row in data],
                    "Avg Rating":    [row[3] for row in data],
                })
            else:
                st.info("No restaurants found with that minimum rating.")
        except Exception as e:
            st.error(f"Error: {e}")


elif choice == "Sort Drivers by Deliveries":
    st.write("### Sort Drivers by Number of Deliveries")
    st.write("See which drivers have completed the most deliveries.")

    if st.button("Load Driver Stats"):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("""
                SELECT d.driver_id, d.first_name, d.last_name, d.vehicle_type, COUNT(fo.order_id) AS total_deliveries
                FROM Driver d
                JOIN Food_Order fo ON d.driver_id = fo.driver_id
                GROUP BY d.driver_id, d.first_name, d.last_name, d.vehicle_type
                ORDER BY total_deliveries DESC
            """)
            data = cur.fetchall()
            cur.close()
            conn.close()

            if data:
                st.success(f"Found {len(data)} driver(s) with deliveries.")
                st.table({
                    "Driver ID":          [row[0] for row in data],
                    "First Name":         [row[1] for row in data],
                    "Last Name":          [row[2] for row in data],
                    "Vehicle Type":       [row[3] for row in data],
                    "Total Deliveries":   [row[4] for row in data],
                })
            else:
                st.info("No delivery data found.")
        except Exception as e:
            st.error(f"Error: {e}")


elif choice == "Show Orders by Max Price":
    st.write("### Show Orders by Maximum Price")
    st.write("Find all orders at or under a specified total amount.")

    max_price = st.number_input("Maximum Order Total ($)", min_value=0.0, value=50.0, step=5.0)

    if st.button("Search Orders"):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("""
                SELECT order_id, order_date, status, delivery_address, total_amount
                FROM Food_Order
                WHERE total_amount <= :max_price
                ORDER BY total_amount DESC
            """, {"max_price": max_price})
            data = cur.fetchall()
            cur.close()
            conn.close()

            if data:
                st.success(f"Found {len(data)} order(s) under ${max_price}.")
                st.table({
                    "Order ID":         [row[0] for row in data],
                    "Order Date":       [row[1] for row in data],
                    "Status":           [row[2] for row in data],
                    "Delivery Address": [row[3] for row in data],
                    "Total Amount ($)": [row[4] for row in data],
                })
            else:
                st.info("No orders found under that price.")
        except Exception as e:
            st.error(f"Error: {e}")


elif choice == "Most Ordered Menu Item per Restaurant":
    st.write("### Most Ordered Menu Item per Restaurant")
    st.write("See which menu items are ordered most at each restaurant.")

    if st.button("Load Menu Stats"):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("""
                SELECT r.name AS restaurant_name, mi.item_name, SUM(oi.quantity) AS total_ordered
                FROM OrderItem oi
                JOIN MenuItem mi ON oi.menu_item_id = mi.menu_item_id
                JOIN Restaurant r ON mi.restaurant_id = r.restaurant_id
                GROUP BY r.name, mi.item_name
                ORDER BY r.name, total_ordered DESC
            """)
            data = cur.fetchall()
            cur.close()
            conn.close()

            if data:
                st.success(f"Found {len(data)} menu item record(s).")
                st.table({
                    "Restaurant":    [row[0] for row in data],
                    "Menu Item":     [row[1] for row in data],
                    "Total Ordered": [row[2] for row in data],
                })
            else:
                st.info("No order item data found.")
        except Exception as e:
            st.error(f"Error: {e}")

# run using: python -m streamlit run app.py