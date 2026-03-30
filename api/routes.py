from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
import models, schemas
from database import get_db
from core.scraper import search_google_maps
from core.etl import clean_and_categorize
from core.gemini import draft_copy, get_gemini_key
import time
from typing import List, Dict, Any
from pydantic import BaseModel

scrape_state: Dict[str, Any] = {
    "is_running": False,
    "start_time": 0.0,
    "found": 0,
    "logs": []
}

def log_progress(msg: str):
    scrape_state["logs"].append(f"[{time.strftime('%H:%M:%S')}] {msg}")
    
class TestGeminiRequest(BaseModel):
    api_key: str

router = APIRouter()

@router.get("/settings", response_model=List[schemas.SettingResponse])
def get_settings(db: Session = Depends(get_db)):
    return db.query(models.Setting).all()

@router.post("/settings", response_model=schemas.SettingResponse)
def update_setting(setting: schemas.SettingCreate, db: Session = Depends(get_db)):
    db_setting = db.query(models.Setting).filter(models.Setting.setting_key == setting.setting_key).first()
    if db_setting:
        db_setting.setting_value = setting.setting_value
    else:
        db_setting = models.Setting(setting_key=setting.setting_key, setting_value=setting.setting_value)
        db.add(db_setting)
    db.commit()
    db.refresh(db_setting)
    return db_setting

@router.post("/settings/test-gemini")
def test_gemini(request: TestGeminiRequest):
    import google.generativeai as genai
    try:
        genai.configure(api_key=request.api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content("Say 'Hello, the Gemini API is working!'. Just reply with this phrase exactly.")
        return {"status": "success", "message": response.text}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/products/{product_key}", response_model=schemas.ProductResponse)
def get_product(product_key: str, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.product_key == product_key).first()
    if not product:
        # Create default entry if not found
        product = models.Product(product_key=product_key, description="Product description pending...", price_range="$500 - $1500")
        db.add(product)
        db.commit()
        db.refresh(product)
    return product

@router.put("/products/{product_key}", response_model=schemas.ProductResponse)
def update_product(product_key: str, product_update: schemas.ProductUpdate, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.product_key == product_key).first()
    if not product:
        product = models.Product(product_key=product_key)
        db.add(product)
    
    update_data = product_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(product, key, value)
        
    db.commit()
    db.refresh(product)
    return product

@router.get("/leads", response_model=List[schemas.LeadResponse])
def get_leads(db: Session = Depends(get_db)):
    return db.query(models.Lead).order_by(models.Lead.created_at.desc()).all()

@router.get("/leads/{lead_id}", response_model=schemas.LeadResponse)
def get_lead(lead_id: int, db: Session = Depends(get_db)):
    lead = db.query(models.Lead).filter(models.Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead

@router.put("/leads/{lead_id}", response_model=schemas.LeadResponse)
def update_lead(lead_id: int, lead_update: schemas.LeadUpdate, db: Session = Depends(get_db)):
    db_lead = db.query(models.Lead).filter(models.Lead.id == lead_id).first()
    if not db_lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    update_data = lead_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_lead, key, value)
        
    db.commit()
    db.refresh(db_lead)
    return db_lead

from core.outreach import send_email_outreach, trigger_whatsapp_placeholder
@router.post("/leads/quantify")
def quantify_leads(product_key: str = "web_dev", db: Session = Depends(get_db)):
    """Agent 2: The Specialist - Quantify existing leads for the selected product."""
    leads = db.query(models.Lead).filter(models.Lead.product_key == product_key).all()
    count = 0
    for lead in leads:
        lead_dict = {
            "website_url": lead.website_url,
            "google_maps_url": lead.google_maps_url,
            "company_name": lead.company_name
        }
        cleaned = clean_and_categorize(lead_dict, product_key=product_key)
        lead.primary_deficit = cleaned["primary_deficit"]
        lead.booking_method = cleaned["booking_method"]
        lead.friction_notes = cleaned["friction_notes"]
        lead.metadata_json = cleaned["metadata_json"] # Ensure metadata is updated
        count += 1
    db.commit()
    return {"status": "success", "processed": count}


@router.post("/leads/reach")
def trigger_reach(product_key: str = "web_dev", db: Session = Depends(get_db)):
    """Agent 3: The Operative - Execute outreach for copy-drafted leads."""
    leads = db.query(models.Lead).filter(
        models.Lead.product_key == product_key,
        models.Lead.lead_status == "COPY_DRAFTED"
    ).all()
    
    results = {"sent": 0, "failed": 0}
    for lead in leads:
        # Placeholder for real outreach
        success = trigger_whatsapp_placeholder(lead.id, db)
        if success:
            results["sent"] += 1
        else:
            results["failed"] += 1
            
    return {"status": "success", "results": results}

@router.post("/leads/{lead_id}/generate-copy")
def generate_copy_endpoint(lead_id: int, db: Session = Depends(get_db)):
    lead = db.query(models.Lead).filter(models.Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
        
    api_key = get_gemini_key(db)
    if not api_key:
        raise HTTPException(status_code=400, detail="Gemini API Key not set.")
        
    copy = draft_copy(
        company_name=lead.company_name,
        location_city=lead.location_city or "Unknown",
        country_code=lead.country_code or "ZA",
        primary_deficit=lead.primary_deficit or "NEEDS_CHATBOT",
        niche=lead.product_key or "web_dev",
        api_key=api_key
    )
    
    lead.ai_generated_copy = copy
    lead.lead_status = "COPY_DRAFTED"
    db.commit()
    db.refresh(lead)
    return {"copy": copy}

def run_scrape_task(req: schemas.ScrapeRequest, db: Session):
    try:
        scrape_state["is_running"] = True
        scrape_state["start_time"] = time.time()
        scrape_state["found"] = 0
        scrape_state["logs"] = []
        log_progress(f"Initializing scraping job for '{req.query}'...")
        
        # Log search
        log_db = models.SearchLog(search_query=req.query, location=req.location)
        db.add(log_db)
        db.commit()
        
        def scraper_callback(msg: str):
            log_progress(msg)
            if msg.startswith("Found:"):
                scrape_state["found"] += 1
                
        # Scrape
        results = search_google_maps(req.query, req.location, req.country_code or "ZA", scraper_callback)
        
        log_db.results_found = len(results)
        db.commit()
        
        log_progress("Processing and applying filters to leads...")
        # Process and save
        saved_count = 0
        for item in results:
            cleaned_item = clean_and_categorize(item, product_key=req.product_key)
            
            # Apply Filters
            if req.must_need_website and cleaned_item.get("has_website"):
                continue
            if req.must_need_booking and cleaned_item.get("has_booking_system"):
                continue
            
            # Check if exists for THIS SPECIFIC product
            existing = db.query(models.Lead).filter(
                models.Lead.company_name == cleaned_item["company_name"],
                models.Lead.product_key == req.product_key
            ).first()
            
            if not existing:
                # Filter item to only include keys present in the Lead model
                valid_keys = {c.name for c in models.Lead.__table__.columns}
                filtered_item = {k: v for k, v in cleaned_item.items() if k in valid_keys}
                
                lead = models.Lead(**filtered_item)
                db.add(lead)
                db.flush() # ensure we have an ID for the lead
                
                # Auto generate copy if requested
                if req.auto_generate_copy:
                    api_key = get_gemini_key(db)
                    if api_key:
                        log_progress(f"Auto-generating copy for {lead.company_name}...")
                        try:
                            copy = draft_copy(
                                company_name=lead.company_name,
                                location_city=lead.location_city or "Unknown",
                                country_code=lead.country_code or "ZA",
                                primary_deficit=lead.primary_deficit or "NEEDS_CHATBOT",
                                niche=req.product_key,
                                api_key=api_key
                            )
                            lead.ai_generated_copy = copy
                            lead.lead_status = "COPY_DRAFTED"
                        except Exception as e:
                            log_progress(f"Copy generation failed: {str(e)}")
                            
                saved_count += 1
        
        db.commit()
        log_progress(f"Job completed. Saved {saved_count} new leads to Vault.")
    except Exception as e:
        import traceback
        print("SCRAPER ERROR TRACEBACK:")
        traceback.print_exc()
        log_progress(f"Error during scraping: {type(e).__name__} - {str(e)}")
    finally:
        scrape_state["is_running"] = False

@router.get("/scrape/status")
def get_scrape_status():
    elapsed = int(time.time() - scrape_state["start_time"]) if scrape_state["is_running"] else 0
    return {
        "is_running": scrape_state["is_running"],
        "elapsed_seconds": elapsed,
        "found": scrape_state["found"],
        "logs": scrape_state["logs"]
    }

@router.post("/scrape")
async def trigger_scrape(request: schemas.ScrapeRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    if scrape_state["is_running"]:
        raise HTTPException(status_code=400, detail="A scraper job is already running.")
        
    background_tasks.add_task(run_scrape_task, request, db)
    return {"status": "Scrape started in background", "query": request.query, "location": request.location}
