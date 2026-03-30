import re

from core.presets import get_config

def clean_and_categorize(raw_lead: dict, product_key: str = "web_dev") -> dict:
    """Deep intelligence pass to evaluate fit for the entire Jiggabyte Product Suite."""
    
    website_url = raw_lead.get("website_url")
    company_name = raw_lead.get("company_name", "").lower()
    has_website = bool(website_url and "facebook.com" not in website_url)
    
    # Inspection Data
    inspection = raw_lead.get("inspection", {})
    has_chatbot = inspection.get("has_chatbot", False)
    has_whatsapp_widget = inspection.get("has_whatsapp_widget", False)
    
    # Primitives Detection
    patterns = {
        "booking": ["calendly", "mindbody", "fresha", "booking.com", "schedulicity", "zocdoc", "reserveyour", "appointment", "book"],
        "payment": ["paystack", "flutterwave", "dpo", "pesapal", "ecocash", "m-pesa", "checkout", "cart", "shop"],
        "whatsapp": ["wa.me", "whatsapp", "api.whatsapp"],
        "medical": ["clinic", "hospital", "doctor", "medical", "health", "surgery"],
        "legal": ["law", "firm", "attorney", "legal", "advocate"],
        "finance": ["lending", "loan", "finance", "credit", "sacco", "microfinance"],
        "edu": ["school", "university", "academy", "college", "institute", "training"],
        "property": ["real estate", "property", "rental", "agency", "realtor"],
        "hotel": ["hotel", "lodge", "guesthouse", "safari", "resort", "inn"]
    }
    
    found = {k: any(p in (website_url or "").lower() or p in company_name for p in v) for k, v in patterns.items()}
    
    # Refine WhatsApp detection with widget check
    found_whatsapp = found["whatsapp"] or has_whatsapp_widget
    
    # Evaluate All Products
    product_fit = {}
    
    # 1. LeadBot360
    product_fit["leadbot_360"] = {
        "fit": not has_whatsapp_widget or not found["booking"],
        "deficit": "MISSED_LEADS" if not found["whatsapp"] else "INQUIRY_LATENCY",
        "notes": "No WhatsApp automation detected." if not found["whatsapp"] else "Has WhatsApp but likely manual chat."
    }
    
    # 2. AgriWise
    product_fit["agri_wise"] = {
        "fit": any(p in company_name for p in ["agri", "farm", "coop", "grower", "tobacco", "maize"]),
        "deficit": "OFFLINE_FARMERS",
        "notes": "Agri-business needs automated farmer reporting."
    }
    
    # 3. BizDesk
    product_fit["biz_desk"] = {
        "fit": has_website and not found["payment"], # Good fit for small offices needing better ops
        "deficit": "COMPLIANCE_RISK",
        "notes": "SME needs automated bookkeeping/compliance tools."
    }
    
    # 4. EduPath
    product_fit["edu_path"] = {
        "fit": found["edu"],
        "deficit": "ADMISSIONS_FRICTION",
        "notes": "Institution needs 24/7 student guidance/admissions guide."
    }
    
    # 5. AdmitFlow
    product_fit["admit_flow"] = {
        "fit": found["edu"] and not found["booking"],
        "deficit": "OCR_NEED",
        "notes": "Needs document automation for student certificates/IDs."
    }
    
    # 6. CreditGuide
    product_fit["credit_guide"] = {
        "fit": found["finance"],
        "deficit": "SCORING_GAP",
        "notes": "Lender needs AI-based pre-scoring for MSMEs."
    }
    
    # 7. HealthLine
    product_fit["health_line"] = {
        "fit": found["medical"],
        "deficit": "TRIAGE_BOTTLENECK" if not found["booking"] else "LANGUAGE_BARRIER",
        "notes": "Medical facility lacks symptom triage/multilingual support."
    }
    
    # 8. LegalScout
    product_fit["legal_scout"] = {
        "fit": found["legal"],
        "deficit": "INTAKE_BOTTLENECK",
        "notes": "Law firm needs automated client intake and doc drafting."
    }
    
    # 9. WorkBridge
    product_fit["work_bridge"] = {
        "fit": found["edu"] or "agency" in company_name,
        "deficit": "PLACEMENT_GAP",
        "notes": "Needs AI-powered internship/job matching."
    }
    
    # 10. CivicAssist
    product_fit["civic_assist"] = {
        "fit": any(p in company_name for p in ["council", "municipality", "gov", "social", "home affairs"]),
        "deficit": "NAV_FRICTION",
        "notes": "Public sector needs citizen service navigation bot."
    }
    
    # 11. WebPrime (Fallback/Modernization)
    product_fit["web_prime"] = {
        "fit": not has_website or (has_website and not found["payment"]),
        "deficit": "NO_WEBSITE" if not has_website else "NO_ECOM",
        "notes": "Missing site." if not has_website else "Needs payment integration."
    }

    # Assign Primary Fit based on requested product_key
    primary = product_fit.get(product_key, product_fit["web_dev"])
    
    # Identify Cross-Sells
    cross_sells = [k for k, v in product_fit.items() if v["fit"] and k != product_key]
    
    import json
    metadata = {
        "all_product_analysis": product_fit,
        "suggested_cross_sell": cross_sells[:3],
        "found_patterns": {k: v for k, v in found.items() if v},
        "inspection": inspection # Pass raw inspection through
    }
    
    raw_lead["has_website"] = has_website
    raw_lead["has_booking_system"] = found["booking"]
    raw_lead["booking_method"] = "online_portal" if found["booking"] else "phone_only"
    raw_lead["friction_notes"] = primary["notes"]
    raw_lead["primary_deficit"] = primary["deficit"]
    raw_lead["product_key"] = product_key
    raw_lead["metadata_json"] = json.dumps(metadata)
    
    return raw_lead
