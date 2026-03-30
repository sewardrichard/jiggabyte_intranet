import sqlite3
import os

DB_PATH = "C:/Users/sewar/repos/lead_gen/leads.db"

PRODUCTS = {
    "prop_engage": {
        "desc": "PropEngage AI: Omnichannel conversational agent for real estate lead qualification and automated viewing scheduling.\n\n"
                "The Problem:\nAgents waste 40% of their time answering repetitive listing questions. Delays in manual replies lead to 30% revenue loss in high-demand markets like Lusaka and Johannesburg.\n\n"
                "How AI Solves It:\nNLP agents qualify prospects by budget and location 24/7. Retrieval-Augmented Generation (RAG) serves live listings and books viewing slots via calendar integration.\n\n"
                "Revenue Model:\nTiered SaaS ($100 - $1000/month) based on lead volume.",
        "price": "$600 - $2500"
    },
    "edu_match": {
        "desc": "EduMatch AI: Predictive advisory platform matching students to university programmes based on history and aptitude.\n\n"
                "The Problem:\nLow counsellor ratios (1:5000) lead to high tertiary dropouts. Rural students face severe informational asymmetry regarding tuition and requirements.\n\n"
                "How AI Solves It:\nHybrid recommendation engine maps student grades against a regional curriculum database to generate a 'probability of admission' score.\n\n"
                "Revenue Model:\nB2B SaaS for institutions + Cost-Per-Lead (CPL) for pre-qualified enrolments.",
        "price": "$1000 - $4000"
    },
    "skill_bridge": {
        "desc": "SkillBridge AI: Semantic matching platform connecting graduates with internships based on deep skill-mapping.\n\n"
                "The Problem:\ncatastrophic youth unemployment combined with a corporate 'skills gap.' Traditional job boards fail to capture latent potential in academic projects.\n\n"
                "How AI Solves It:\nVector embeddings calculate semantic similarity between student portfolios and corporate job descriptions, moving beyond keyword matching.\n\n"
                "Revenue Model:\nEmployer SaaS for talent pool access + placement success fees.",
        "price": "$1000 - $3500"
    },
    "docu_admit": {
        "desc": "DocuAdmit AI: Document processing engine for automated extraction and verification of admissions data.\n\n"
                "The Problem:\nCrippling administrative backlogs during intake. Manual review of transcripts results in 90-day processing delays.\n\n"
                "How AI Solves It:\nDeep-learning OCR and computer vision extract Subject/Grade data from low-quality photos of transcripts and IDs with 99%+ accuracy.\n\n"
                "Revenue Model:\nUsage-based micro-transactions billed per document processed ($2 - $10/app).",
        "price": "$1500 - $5000"
    },
    "pacra_assist": {
        "desc": "PACRA-Assist AI: WhatsApp-native assistant for business registration and annual compliance filings in Zambia.\n\n"
                "The Problem:\nEstimated 2.7M unregistered Zambian businesses. Imminent threat of deregistration for 300k firms failing to file annual returns.\n\n"
                "How AI Solves It:\nVirtual legal clerk conducting interactive interviews to populate complex PACRA forms automatically via API integration.\n\n"
                "Revenue Model:\nB2C Transactional Fee (Convenience markup on statutory fees).",
        "price": "$50 - $200"
    },
    "medi_connect": {
        "desc": "MediConnect AI: Conversational triage and scheduling assistant for private clinic administration.\n\n"
                "The Problem:\nSystemic shortfall of 6M healthcare workers. Manual appointment scheduling leads to high no-show rates for chronic care (HIV/TB).\n\n"
                "How AI Solves It:\nStrictly constrained NLP triage based on medical decision trees. Automates multilingual reminder nudges for medication adherence.\n\n"
                "Revenue Model:\nB2B SaaS scaled on patient volume or number of medical practitioners.",
        "price": "$800 - $3000"
    },
    "agri_vision": {
        "desc": "AgriVision Bot: Computer vision tool for instant crop disease diagnosis via WhatsApp leaf photos.\n\n"
                "The Problem:\nPests like Fall Armyworm devastate yields due to delayed diagnosis. Remote farm locations lack access to extension officers.\n\n"
                "How AI Solves It:\nConvolutional Neural Networks (CNN) trained on regional pathology datasets return localized treatment recommendations instantly.\n\n"
                "Revenue Model:\nInstitutional licensing to NGOs/Government or input supplier sponsorship.",
        "price": "$1500 - $6000"
    },
    "border_flow": {
        "desc": "BorderFlow AI: Platform for automated digitization and compliance checking of cross-border trade documentation.\n\n"
                "The Problem:\nAverage clearance delays of 39-96 hours at SADC borders (Beitbridge/Chirundu) due to paper-based processes.\n\n"
                "How AI Solves It:\nComputer vision interprets bills of lading and commercial invoices, translating and checking them against SADC tariff codes in real-time.\n\n"
                "Revenue Model:\nB2B SaaS tiered by volume of freight documents or manifests processed.",
        "price": "$2000 - $8000"
    },
    "credi_score": {
        "desc": "CrediScore Africa: AI credit risk assessment API for unbanked micro-enterprises and smallholder farmers.\n\n"
                "The Problem:\n70% of employment is informal. Lack of formal credit history forces MSMEs into predatory lending cycles.\n\n"
                "How AI Solves It:\nAnalyzes alternative data (Mobile Money, behavioral USSD metadata, and satellite imagery) to predict default probabilities accurately.\n\n"
                "Revenue Model:\nRecurring per-API-call transaction fee for every credit score generated.",
        "price": "$2000 - $10000"
    },
    "web_prime": {
        "desc": "WebPrime: Modern Website & E-commerce Development built for high-growth African businesses.\n\n"
                "The Problem:\nLegacy sites are non-responsive and lack integration with local mobile money (EcoCash, M-Pesa, Paystack).\n\n"
                "How AI Solves It:\nAI-optimized conversion UIs with integrated payment gateways and automatic order management systems.\n\n"
                "Revenue Model:\nSetup fees plus monthly maintenance and hosting.",
        "price": "$400 - $2000"
    },
    "spaza_sync": {
        "desc": "SpazaSync AI: Predictive inventory management tool for informal township and market retailers.\n\n"
                "The Problem:\nMicro-merchants suffer from scarce capital locked in slow goods and frequent stockouts of daily necessities.\n\n"
                "How AI Solves It:\nARIMA/Prophet time-series forecasting analyzes community events and payday cycles to predict optimal restocking dates via USSD.\n\n"
                "Revenue Model:\nEnterprise licensing to FMCG distributors seeking last-mile data visibility.",
        "price": "$1500 - $5000"
    },
    "civic_assist": {
        "desc": "CivicAssist: AI assistant for navigating government services, grant eligibility, and documentation checklists.\n\n"
                "The Problem:\nCitizens miss out on grants and IDs due to complex, fragmented eligibility info. Overloaded front desks in home affairs offices.\n\n"
                "How AI Solves It:\nRetrieval-Augmented Generation (RAG) over official policy documents with multilingual support in native vernaculars.\n\n"
                "Revenue Model:\nProject implementation fees + annual support contracts for Municipalities/NGOs.",
        "price": "$1200 - $4000"
    },
    "guest_flow": {
        "desc": "GuestFlow AI: Conversational guest services bot for hotels and safari lodges to manage reservations and requests.\n\n"
                "The Problem:\nHigh labor cost for 24/7 front desk coverage. Missed opportunities for upselling spa, tours, and transfers during stay.\n\n"
                "How AI Solves It:\nWhatsApp-first agent handles check-in info, room service, and automated post-stay review collection.\n\n"
                "Revenue Model:\nMonthly SaaS per-property or per-room commission on upsells.",
        "price": "$700 - $2500"
    },
    "biz_desk": {
        "desc": "BizDesk AI: SME Operational Copilot for bookkeeping, HR drafting, and automated invoicing via WhatsApp.\n\n"
                "The Problem:\nSME owners are overwhelmed by HR paperwork and bookkeeping, leading to compliance penalties and credit rejection.\n\n"
                "How AI Solves It:\nLLM-based assistant generates contracts and invoices on the fly and classifies expenses from mobile money receipts.\n\n"
                "Revenue Model:\nLow-cost monthly subscription or white-label for accounting firms.",
        "price": "$500 - $1500"
    },
    "agri_connect": {
        "desc": "AgriConnect AI: Farmer reporting and communication system for cooperatives via SMS and USSD.\n\n"
                "The Problem:\nDisconnected farmer networks. No scalable way to send localized weather alerts or collect harvest estimates without smartphones.\n\n"
                "How AI Solves It:\nAutomated USSD/SMS alert system and harvest reporting bot that planning logistics ahead of season.\n\n"
                "Revenue Model:\nPlatform licensing to Agribusinesses and Cooperatives.",
        "price": "$1000 - $3500"
    }
}

def seed():
    if not os.path.exists(DB_PATH):
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Ensure products table exists
    cursor.execute("CREATE TABLE IF NOT EXISTS products (product_key VARCHAR PRIMARY KEY, description TEXT, price_range VARCHAR, updated_at DATETIME DEFAULT CURRENT_TIMESTAMP)")

    for key, data in PRODUCTS.items():
        cursor.execute("""
            INSERT INTO products (product_key, description, price_range)
            VALUES (?, ?, ?)
            ON CONFLICT(product_key) DO UPDATE SET
                description = excluded.description,
                price_range = excluded.price_range
        """, (key, data["desc"], data["price"]))
            
    conn.commit()
    conn.close()
    print("Strategic 15-Product Suite seeded successfully.")

if __name__ == "__main__":
    seed()
