from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime
from sqlalchemy.sql import func
from database import Base

class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String, index=True)
    industry = Column(String, nullable=True)
    location_city = Column(String, index=True, nullable=True)
    
    google_maps_url = Column(String, nullable=True)
    linkedin_url = Column(String, nullable=True)
    website_url = Column(String, nullable=True)
    facebook_url = Column(String, nullable=True)
    
    product_key = Column(String, index=True, default="web_dev") # whatsapp_sales, agri_reporting, etc.
    metadata_json = Column(Text, nullable=True) # JSON blob for product-specific data
    
    country_code = Column(String, index=True, nullable=True) # e.g. ZA, ZM, ZW
    booking_method = Column(String, nullable=True) # none, form, phone_only, whatsapp_only, online_portal
    friction_notes = Column(Text, nullable=True)
    
    has_website = Column(Boolean, default=False)
    has_booking_system = Column(Boolean, default=False)
    
    primary_deficit = Column(String, nullable=True) # e.g. NEEDS_WEBSITE, NEEDS_BOOKING, NEEDS_CHATBOT, NEEDS_XCALLY_OMNICHANNEL, OUTDATED_TECH
    decision_maker_name = Column(String, nullable=True)
    contact_email = Column(String, nullable=True)
    contact_phone = Column(String, nullable=True)
    
    ai_generated_copy = Column(Text, nullable=True)
    lead_status = Column(String, default="NEW") # NEW, REVIEWING, COPY_DRAFTED, CONTACTED, REJECTED
    data_source = Column(String, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Setting(Base):
    __tablename__ = "settings"

    id = Column(Integer, primary_key=True, index=True)
    setting_key = Column(String, unique=True, index=True)
    setting_value = Column(String)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

class SearchLog(Base):
    __tablename__ = "search_log"

    id = Column(Integer, primary_key=True, index=True)
    search_query = Column(String)
    location = Column(String)
    results_found = Column(Integer, default=0)
    run_at = Column(DateTime(timezone=True), server_default=func.now())

class Product(Base):
    __tablename__ = "products"

    product_key = Column(String, primary_key=True, index=True)
    description = Column(Text, nullable=True)
    price_range = Column(String, nullable=True) # e.g. "$500 - $1500"
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
