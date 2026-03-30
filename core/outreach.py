import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from sqlalchemy.orm import Session
import models

def send_email_outreach(lead_id: int, db: Session, smtp_settings: dict) -> bool:
    """Sends an email outreach for a specific lead."""
    lead = db.query(models.Lead).filter(models.Lead.id == lead_id).first()
    if not lead or not lead.ai_generated_copy or not lead.contact_email:
        return False
        
    try:
        msg = MIMEMultipart()
        msg['From'] = smtp_settings.get('sender_email')
        msg['To'] = lead.contact_email
        msg['Subject'] = f"Helping {lead.company_name} with digital booking"
        
        body = lead.ai_generated_copy
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP(smtp_settings.get('smtp_server'), smtp_settings.get('smtp_port'))
        server.starttls()
        server.login(smtp_settings.get('sender_email'), smtp_settings.get('sender_password'))
        text = msg.as_string()
        server.sendmail(smtp_settings.get('sender_email'), lead.contact_email, text)
        server.quit()
        
        lead.lead_status = "CONTACTED"
        db.commit()
        return True
    except Exception as e:
        print(f"Failed to send email to {lead.contact_email}: {str(e)}")
        return False

def trigger_whatsapp_placeholder(lead_id: int, db: Session) -> bool:
    """Placeholder for WhatsApp outreach logic."""
    lead = db.query(models.Lead).filter(models.Lead.id == lead_id).first()
    if not lead or not lead.ai_generated_copy or not lead.contact_phone:
        return False
    
    # In a real implementation, this might call a Twilio API or a Playwright script
    print(f"WHATSAPP OUTREACH (Placeholder) to {lead.contact_phone} for {lead.company_name}")
    
    lead.lead_status = "CONTACTED"
    db.commit()
    return True
