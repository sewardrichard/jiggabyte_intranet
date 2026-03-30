from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class LeadBase(BaseModel):
    company_name: str
    industry: Optional[str] = None
    location_city: Optional[str] = None
    google_maps_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    website_url: Optional[str] = None
    facebook_url: Optional[str] = None
    product_key: str = "web_dev"
    country_code: Optional[str] = None
    booking_method: Optional[str] = None
    friction_notes: Optional[str] = None
    has_website: bool = False
    has_booking_system: bool = False
    primary_deficit: Optional[str] = None
    decision_maker_name: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    ai_generated_copy: Optional[str] = None
    lead_status: str = "NEW"
    data_source: Optional[str] = None

class LeadCreate(LeadBase):
    pass

class LeadUpdate(BaseModel):
    ai_generated_copy: Optional[str] = None
    lead_status: Optional[str] = None

class LeadResponse(LeadBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class ProductBase(BaseModel):
    product_key: str
    description: Optional[str] = None
    price_range: Optional[str] = None

class ProductUpdate(BaseModel):
    description: Optional[str] = None
    price_range: Optional[str] = None

class ProductResponse(ProductBase):
    updated_at: datetime

    class Config:
        from_attributes = True

class SettingBase(BaseModel):
    setting_key: str
    setting_value: str

class SettingCreate(SettingBase):
    pass

class SettingResponse(SettingBase):
    id: int
    updated_at: datetime
    
    class Config:
        from_attributes = True

class SearchLogCreate(BaseModel):
    search_query: str
    location: str
    results_found: int

class ScrapeRequest(BaseModel):
    query: str
    location: str
    product_key: str = "web_dev"
    country_code: Optional[str] = "ZA"
    business_type: str = "custom"
    must_need_website: bool = False
    must_need_booking: bool = False
    auto_generate_copy: bool = False
