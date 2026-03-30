import sqlite3
import os

DB_PATH = "C:/Users/sewar/repos/lead_gen/leads.db"

def migrate():
    if not os.path.exists(DB_PATH):
        print(f"Database not found at {DB_PATH}. It will be created with the correct schema by the app.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    columns = [
        ("niche", "VARCHAR"),
        ("metadata_json", "TEXT"),
        ("country_code", "VARCHAR"),
        ("booking_method", "VARCHAR"),
        ("friction_notes", "TEXT")
    ]
    
    for col_name, col_type in columns:
        try:
            print(f"Adding column {col_name}...")
            cursor.execute(f"ALTER TABLE leads ADD COLUMN {col_name} {col_type}")
        except sqlite3.OperationalError:
            print(f"Column {col_name} already exists.")
            
    conn.commit()
    conn.close()
    print("Migration finished successfully.")

if __name__ == "__main__":
    migrate()
