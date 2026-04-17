

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

def load_sheet(name):
    if name not in excel_file.sheet_names:
        raise ValueError(f"Sheet '{name}' not found.")
    df = excel_file.parse(name)
    df.columns = df.columns.str.lower().str.strip()
    return df

# Identity columns to remove per table
IDENTITY_COLUMNS = {
    "Customer": ["customer_id"],
    "Restaurant": ["restaurant_id"],
    "Driver": ["driver_id"],
    "Food_Order": ["order_id"],
    "MenuItem": ["menu_item_id"],
    "OrderItem": ["order_item_id"],  # keep order_id (FK), remove only identity
    "Payment": ["payment_id"],
    "Review": ["review_id"]
}

def process_and_save(sheet_name):
    df = load_sheet(sheet_name)

    # Remove identity columns if they exist
    cols_to_drop = IDENTITY_COLUMNS.get(sheet_name, [])
    df = df.drop(columns=[col for col in cols_to_drop if col in df.columns], errors='ignore')

    # Save cleaned CSV
    output_path = os.path.join(OUTPUT_DIR, f"{sheet_name}.csv")
    df.to_csv(output_path, index=False)

    print(f"{sheet_name}: cleaned and saved ({len(df)} rows)")

# PROCESS ALL TABLES
tables = [
    "Customer",
    "Restaurant",
    "Driver",
    "MenuItem",
    "Food_Order",
    "OrderItem",
    "Payment",
    "Review"
]

for table in tables:
    process_and_save(table)

print("\nCSV files saved to:", OUTPUT_DIR)