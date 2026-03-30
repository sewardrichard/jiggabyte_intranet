import os
import google.generativeai as genai
from sqlalchemy.orm import Session
from models import Setting

def get_gemini_key(db: Session):
    # Try database first
    setting = db.query(Setting).filter(Setting.setting_key == "GEMINI_API_KEY").first()
    if setting and setting.setting_value:
        return setting.setting_value
    
    # Fallback to environment variable
    return os.getenv("GEMINI_API_KEY")

from core.presets import get_config

def draft_copy(company_name: str, location_city: str, country_code: str, primary_deficit: str, niche: str, api_key: str) -> str:
    if not api_key:
        return "Error: Gemini API key not found in settings."
        
    genai.configure(api_key=api_key)
    config = get_config(niche)
    
    country_map = {
        "ZA": "South Africa",
        "ZM": "Zambia",
        "ZW": "Zimbabwe",
        "BW": "Botswana",
        "NA": "Namibia"
    }
    country_name = country_map.get(country_code, "Southern Africa")
    
    system_prompt = f"""You are a friendly, local tech consultant representing Jiggabyte (jiggabyte.co.zm) in {country_name}. 
You are reaching out to a local business in {location_city}. 
Your tone must be warm, neighborly, and helpful—never aggressive, corporate, or overly "salesy". 
Keep it concise (under 4 sentences). 

Target Business: {company_name}
Observed Issue: {primary_deficit}

{config['system_prompt_nuance']} Use local nuances if appropriate for {country_name}."""

    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content(system_prompt)
    
    return response.text
