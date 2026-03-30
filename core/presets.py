# Jiggabyte Strategic AI Product Suite (The Final 15)

NICHE_CONFIGS = {
    "prop_engage": {
        "label": "PropEngage AI",
        "solution": "Real Estate Lead Capture & Nurturing",
        "default_query": "Real estate agency property management rental agency realtor",
        "niche": "Real Estate",
        "deficit_types": {
            "VIEWING_FRICTION": "Manual viewing appointment booking",
            "UNQUALIFIED_LEADS": "Too much time on non-serious tenants",
            "INQUIRY_LATENCY": "High missed inquiry risk on listings"
        },
        "system_prompt_nuance": "Pitch an omnichannel AI agent that qualifies leads 24/7 via WhatsApp and schedules viewings directly into agent calendars."
    },
    "edu_match": {
        "label": "EduMatch AI",
        "solution": "University Course & Career Guide",
        "default_query": "Private college university TVET training institute secondary school",
        "niche": "Education",
        "deficit_types": {
            "GUIDANCE_GAP": "Students lack career counseling and program matching",
            "ENROLMENT_FRICTION": "Manual and fragmented course selection info",
            "ADMISSIONS_LATENCY": "Slow response to prospective student inquiries"
        },
        "system_prompt_nuance": "Pitch a conversational advisory platform that matches students to programs based on grades and budget via WhatsApp."
    },
    "skill_bridge": {
        "label": "SkillBridge AI",
        "solution": "Internship & Talent Matcher",
        "default_query": "University career office coding bootcamp placement agency",
        "niche": "HR & Placement",
        "deficit_types": {
            "PLACEMENT_GAP": "Weak links between graduating students and employers",
            "MANUAL_MATCHING": "Institution sifts through student CVs manually",
            "DATA_SPARSITY": "Low visibility into student skill profiles"
        },
        "system_prompt_nuance": "Pitch a semantic matching platform that connects graduates with relevant corporate internships using AI skill-mapping."
    },
    "docu_admit": {
        "label": "DocuAdmit AI",
        "solution": "Admissions OCR & Verification",
        "default_query": "Examination council university registrar secondary school admissions",
        "niche": "Education Admin",
        "deficit_types": {
            "OCR_NEED": "Manual data entry from paper certificates and IDs",
            "FRAUD_RISK": "No automated validation of academic transcripts",
            "QUEUE_FRICTION": "In-person physical document submission bottlenecks"
        },
        "system_prompt_nuance": "Pitch an intelligent document processing engine that automates the extraction and verification of student IDs and transcripts."
    },
    "pacra_assist": {
        "label": "PACRA-Assist AI",
        "solution": "Business Registration & Compliance",
        "default_query": "Legal consultant registrar office SME center startup hub",
        "niche": "Legal Compliance",
        "deficit_types": {
            "REGISTRATION_PANIC": "Mass deregistration threat; urgent need for returns",
            "FORMALIZATION_GAP": "Informal micro-enterprises struggle with registration",
            "COMPLIANCE_FRICTION": "Complex and opaque manual return filing"
        },
        "system_prompt_nuance": "Pitch a WhatsApp-native assistant that navigates micro-entrepreneurs through business registration and annual compliance filings."
    },
    "medi_connect": {
        "label": "MediConnect AI",
        "solution": "Clinic Triage & Appointment Bot",
        "default_query": "Private medical clinic doctor surgery medical center hospital",
        "niche": "Healthcare",
        "deficit_types": {
            "TRIAGE_BOTTLENECK": "Clinician shortages and long hospital queues",
            "BOOKING_FRICTION": "Manual, rigid appointment scheduling over phone",
            "REMINDER_GAP": "No automated medication or follow-up reminders"
        },
        "system_prompt_nuance": "Pitch a conversational triage and scheduling bot that alleviates administrative burdens and manages chronic patient follow-ups."
    },
    "agri_vision": {
        "label": "AgriVision Bot",
        "solution": "Crop Disease Detection CV",
        "default_query": "Agriculture cooperative input supplier farming NGO",
        "niche": "Agri-Tech",
        "deficit_types": {
            "DISEASE_OUTBREAK": "Slow manual diagnosis of crop pests and diseases",
            "EXTENSION_GAP": "Shortage of extension officers for remote farms",
            "YIELD_RISK": "Delayed treatment leading to massive crop losses"
        },
        "system_prompt_nuance": "Pitch a computer vision tool that enables farmers to instantly diagnose crop diseases by submitting photos via WhatsApp."
    },
    "border_flow": {
        "label": "BorderFlow AI",
        "solution": "Customs Document Gateway",
        "default_query": "Logistics company freight forwarder clearing agent weighbridge",
        "niche": "Logistics",
        "deficit_types": {
            "CLEARANCE_DELAY": "Catastrophic administrative delays at border crossings",
            "PAPER_BASED": "Archaic paper customs processes and redundant entry",
            "COMPLIANCE_RISK": "Manual check against complex SADC tariff codes"
        },
        "system_prompt_nuance": "Pitch a computer vision platform that automates the digitization and compliance checking of cross-border trade documentation."
    },
    "credi_score": {
        "label": "CrediScore Africa",
        "solution": "Informal Sector Credit Scoring",
        "default_query": "Microfinance institution SACCO digital lender credit bureau",
        "niche": "Fintech",
        "deficit_types": {
            "UNBANKED_RISK": "Lack of formal credit history for informal MSMEs",
            "ASSESSMENT_COST": "Expensive manual risk assessment for small loans",
            "COLLATERAL_BARRIER": "Lenders can't verify economic activity of spaza shops"
        },
        "system_prompt_nuance": "Pitch an alternative credit scoring API that uses mobile money and behavioral data to lend to the unbanked sector."
    },
    "web_prime": {
        "label": "WebPrime",
        "solution": "E-commerce & Web Modernization",
        "default_query": "Business local store company office boutique",
        "niche": "General Business",
        "deficit_types": {
            "NO_WEBSITE": "Zero digital visibility; no storefront",
            "OUTDATED_UI": "Old non-responsive site with low conversion",
            "NO_ECOM": "Missing local mobile money payment integration"
        },
        "system_prompt_nuance": "Pitch modern, high-conversion websites integrated with local payments like EcoCash, M-Pesa, and Paystack."
    },
    "spaza_sync": {
        "label": "SpazaSync AI",
        "solution": "Informal Retail Forecasting",
        "default_query": "FMCG distributor wholesaler cash and carry township market",
        "niche": "Retail & Wholesale",
        "deficit_types": {
            "STOCKOUT_RISK": "Frequent stockouts of high-demand necessities",
            "CAPITAL_LOCK": "Working capital tied up in slow-moving inventory",
            "DATA_BLINDNESS": "Distributors lack visibility into last-mile sales"
        },
        "system_prompt_nuance": "Pitch a predictive inventory tool for spaza shops that enables dynamic ordering and demand forecasting via USSD/WhatsApp."
    },
    "civic_assist": {
        "label": "CivicAssist",
        "solution": "Gov & NGO Service Navigator",
        "default_query": "Municipality council social grant NGO home affairs",
        "niche": "Public Sector",
        "deficit_types": {
            "ELIGIBILITY_Opaque": "Citizens struggle to understand social grant criteria",
            "FRONT_DESK_OVERLOAD": "Offices overwhelmed by basic inquiries",
            "DOCUMENT_FRICTION": "Citizens arrive with incorrect paperwork for IDs"
        },
        "system_prompt_nuance": "Pitch an AI assistant that helps citizens navigate government services and eligibility checklists in local languages."
    },
    "guest_flow": {
        "label": "GuestFlow AI",
        "solution": "Hospitality Guest Services",
        "default_query": "Boutique hotel safari lodge guesthouse resort",
        "niche": "Hospitality",
        "deficit_types": {
            "RESERVATION_FRICTION": "Manual booking via WhatsApp or DM",
            "MISSED_UPSELL": "No automated promotion of tours or spa services",
            "REVIEW_GAP": "No automated collection of post-stay reviews"
        },
        "system_prompt_nuance": "Pitch an AI guest assistant that handles reservations, manages requests, and automates upselling and reviews via WhatsApp."
    },
    "biz_desk": {
        "label": "BizDesk AI",
        "solution": "SME Operational Copilot",
        "default_query": "SME office small business boutique accounting startup",
        "niche": "SME Operations",
        "deficit_types": {
            "ADMIN_OVERHEAD": "High manual effort for invoicing and HR letters",
            "BOOKKEEPING_GAP": "Unstructured expense tracking from mobile money",
            "COMPLIANCE_RISK": "Missing key statutory or tax deadlines"
        },
        "system_prompt_nuance": "Pitch an AI assistant that generates invoices, contracts, and HR letters via a simple WhatsApp-based bookkeeping interface."
    },
    "agri_connect": {
        "label": "AgriConnect AI",
        "solution": "Farmer Reporting & Communication",
        "default_query": "Agriculture cooperative farming aggregator farming NGO",
        "niche": "Agri-Business",
        "deficit_types": {
            "COMMUNICATION_GAP": "No direct channel to alert farmers about weather/pests",
            "MANUAL_LOGISTICS": "Relies on physical visits for harvest reporting",
            "OFFLINE_NETWORK": "Disconnected smallholder farmer clusters"
        },
        "system_prompt_nuance": "Pitch a USSD/SMS platform that connects farmers to alerts and harvest reporting without requiring smartphones or data."
    }
}

def get_config(product_key: str) -> dict:
    return NICHE_CONFIGS.get(product_key, NICHE_CONFIGS["web_prime"])
