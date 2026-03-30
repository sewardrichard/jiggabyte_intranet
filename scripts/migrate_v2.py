import sqlite3
import os

DB_PATH = "C:/Users/sewar/repos/lead_gen/leads.db"

def migrate():
    if not os.path.exists(DB_PATH):
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Check if column needs renaming
    cursor.execute("PRAGMA table_info(leads)")
    cols = [col[1] for col in cursor.fetchall()]
    
    if "niche" in cols and "product_key" not in cols:
        print("Renaming niche to product_key...")
        cursor.execute("ALTER TABLE leads RENAME COLUMN niche TO product_key")
    elif "product_key" not in cols:
        print("Adding product_key column...")
        cursor.execute("ALTER TABLE leads ADD COLUMN product_key VARCHAR DEFAULT 'web_dev'")
            
    conn.commit()
    conn.close()
    print("Migration complete.")

if __name__ == "__main__":
    migrate()
