import argparse
import sys
import os

# Add parent dir to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import SessionLocal, engine
import models

# Create tables
models.Base.metadata.create_all(bind=engine)

from core.scraper import search_google_maps
from core.etl import clean_and_categorize
from core.gemini import draft_copy, get_gemini_key

def run_scout(query, location, country_code, product_key):
    db = SessionLocal()
    print(f"[*] Starting Scout: {query} in {location} ({country_code}) for product: {product_key}")
    
    results = search_google_maps(query, location, country_code, print)
    
    saved = 0
    for item in results:
        cleaned = clean_and_categorize(item, product_key=product_key)
        existing = db.query(models.Lead).filter(models.Lead.company_name == cleaned["company_name"]).first()
        if not existing:
            lead = models.Lead(**cleaned)
            db.add(lead)
            saved += 1
    
    db.commit()
    db.close()
    print(f"[+] Scout finished. Saved {saved} new leads.")

def run_quantify(product_key):
    db = SessionLocal()
    print(f"[*] Quantifying leads for product: {product_key}...")
    leads = db.query(models.Lead).filter(models.Lead.product_key == product_key).all()
    for lead in leads:
        lead_dict = {
            "website_url": lead.website_url, 
            "company_name": lead.company_name,
            "google_maps_url": lead.google_maps_url
        }
        cleaned = clean_and_categorize(lead_dict, product_key=product_key)
        lead.primary_deficit = cleaned["primary_deficit"]
        lead.booking_method = cleaned["booking_method"]
        lead.friction_notes = cleaned["friction_notes"]
    db.commit()
    db.close()
    print(f"[+] Quantification finished for {len(leads)} leads.")

def run_copywriter(product_key):
    db = SessionLocal()
    api_key = get_gemini_key(db)
    if not api_key:
        print("[!] Gemini API Key not found.")
        return

    leads = db.query(models.Lead).filter(
        models.Lead.product_key == product_key, 
        models.Lead.lead_status == "NEW"
    ).all()
    print(f"[*] Copywriter: Processing {len(leads)} leads for product: {product_key}...")
    
    for lead in leads:
        print(f"[*] Generating copy for {lead.company_name}...")
        copy = draft_copy(
            company_name=lead.company_name,
            location_city=lead.location_city or "Unknown",
            country_code=lead.country_code or "ZA",
            primary_deficit=lead.primary_deficit or "NEEDS_CHATBOT",
            niche=product_key,
            api_key=api_key
        )
        lead.ai_generated_copy = copy
        lead.lead_status = "COPY_DRAFTED"
        db.commit()
    
    db.close()
    print("[+] Copywriter finished.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Jiggabyte Command Center CLI")
    parser.add_init = parser.add_subparsers(dest="command")
    
    scout_parser = parser.add_init.add_parser("scout")
    scout_parser.add_argument("--query", required=True)
    scout_parser.add_argument("--location", required=True)
    scout_parser.add_argument("--country", default="ZA")
    scout_parser.add_argument("--product", default="web_dev")
    
    quantify_parser = parser.add_init.add_parser("quantify")
    quantify_parser.add_argument("--product", default="web_dev")
    
    copy_parser = parser.add_init.add_parser("copywriter")
    copy_parser.add_argument("--product", default="web_dev")
    
    args = parser.parse_args()
    
    if args.command == "scout":
        run_scout(args.query, args.location, args.country, args.product)
    elif args.command == "quantify":
        run_quantify(args.product)
    elif args.command == "copywriter":
        run_copywriter(args.product)
    else:
        parser.print_help()
