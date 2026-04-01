

import pandas as pd
import openpyxl
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(BASE_DIR, "food_delivery_data.xlsx")

# LOAD EXCEL WITH MULTIPLE SHEETS
excel_file = pd.ExcelFile(INPUT_FILE)

# OUTPUT DIRECTORY
OUTPUT_DIR = os.path.join(BASE_DIR, "csv")
os.makedirs(OUTPUT_DIR, exist_ok=True)

excel_file = pd.ExcelFile(INPUT_FILE)

def load_sheet(name):
    if name not in excel_file.sheet_names:
        raise ValueError(f"Sheet '{name}' not found.")
    df = excel_file.parse(name)
    df.columns = df.columns.str.lower().str.strip()
    return df

# CUSTOMER TABLE
customer_df = load_sheet("Customer")
customer_df.to_csv(os.path.join(OUTPUT_DIR, "Customer.csv"), index=False)

# RESTAURANT TABLE
restaurant_df = load_sheet("Restaurant")
restaurant_df.to_csv(os.path.join(OUTPUT_DIR, "Restaurant.csv"), index=False)

# DRIVER TABLE
driver_df = load_sheet("Driver")
driver_df.to_csv(os.path.join(OUTPUT_DIR, "Driver.csv"), index=False)

# FOOD_ORDER TABLE
order_df = load_sheet("Food_Order")
order_df.to_csv(os.path.join(OUTPUT_DIR, "Food_Order.csv"), index=False)

# MENU ITEM TABLE
menu_df = load_sheet("MenuItem")
menu_df.to_csv(os.path.join(OUTPUT_DIR, "MenuItem.csv"), index=False)

# ORDER ITEM TABLE
order_item_df = load_sheet("OrderItem")
order_item_df.to_csv(os.path.join(OUTPUT_DIR, "OrderItem.csv"), index=False)

# PAYMENT TABLE
payment_df = load_sheet("Payment")
payment_df.to_csv(os.path.join(OUTPUT_DIR, "Payment.csv"), index=False)

# REVIEW TABLE
review_df = load_sheet("Review")
review_df.to_csv(os.path.join(OUTPUT_DIR, "Review.csv"), index=False)

print("CSV files saved to:", OUTPUT_DIR)