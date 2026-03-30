import urllib.parse
from playwright.sync_api import sync_playwright

def inspect_website(url: str, browser_context) -> dict:
    """Visits a website to detect technical features like chatbots, booking, and e-commerce."""
    features = {
        "has_chatbot": False,
        "chatbot_type": None,
        "has_whatsapp_widget": False,
        "emails": [],
        "phones": []
    }
    
    if not url or not url.startswith("http"):
        return features
        
    try:
        page = browser_context.new_page()
        # Set a shorter timeout for inspection
        page.goto(url, timeout=20000, wait_until="domcontentloaded")
        page.wait_for_timeout(2000) # Wait for widgets to load
        
        content = page.content().lower()
        
        # Chatbot Detection
        bot_patterns = {
            "intercom": "intercom-container",
            "crisp": "crisp-client",
            "tawk.to": "tawk.to",
            "drift": "drift-frame",
            "zendesk": "zendesk-embeddable",
            "tidio": "tidio-chat",
            "chatbot.com": "chatbot.com",
            "hubspot": "hs-messages",
            "chatwoot": "chatwoot"
        }
        
        for bot_name, pattern in bot_patterns.items():
            if pattern in content:
                features["has_chatbot"] = True
                features["chatbot_type"] = bot_name
                break
        
        # WhatsApp Widget Detection
        if "wa.me" in content or "whatsapp" in content or "whatsapp-widget" in content:
            features["has_whatsapp_widget"] = True
            
        # Basic Email/Phone Extraction
        import re
        emails = re.findall(r'[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+', content)
        features["emails"] = list(set(emails))[:3]
        
        page.close()
    except Exception as e:
        print(f"Error inspecting {url}: {str(e)}")
    
    return features

def search_google_maps(query: str, location: str, country_code: str = "ZA", progress_callback=None):
    search_term = f"{query} near {location}"
    results = []
    
    if progress_callback: progress_callback(f"Starting deep search for '{search_term}'...")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={'width': 1280, 'height': 800}
        )
        page = context.new_page()
        
        encoded_query = urllib.parse.quote(search_term)
        search_url = f"https://www.google.com/maps/search/{encoded_query}?hl=en"
        
        page.goto(search_url)
        page.wait_for_timeout(5000)
        
        # Scroll to load more
        if progress_callback: progress_callback("Expanding search radius...")
        for _ in range(3):
            page.mouse.wheel(0, 4000)
            page.wait_for_timeout(2000)

        # Extract items
        items = page.query_selector_all('div[role="article"]')
        if progress_callback: progress_callback(f"Analyzing {len(items)} potential matches...")
        
        for item in items[:20]:
            try:
                # Name
                name_el = item.query_selector('div.fontHeadlineSmall')
                name = name_el.inner_text() if name_el else None
                
                # Maps URL
                link_el = item.query_selector('a')
                maps_url = link_el.get_attribute('href') if link_el else None
                
                # Direct Website Link (Google Maps often has a website icon/link in the card)
                website_url = None
                all_links = item.query_selector_all('a')
                for l in all_links:
                    href = l.get_attribute('href')
                    if href and not href.startswith("https://www.google.com/maps"):
                        website_url = href
                        break
                
                if name:
                    if progress_callback: progress_callback(f"Found: {name}")
                    results.append({
                        "company_name": name, 
                        "google_maps_url": maps_url,
                        "location_city": location,
                        "country_code": country_code,
                        "industry": query,
                        "data_source": "Google Maps",
                        "website_url": website_url
                    })
            except Exception:
                continue
        
        # Secondary Search for missing websites
        exclude_domains = [
            "facebook.com", "instagram.com", "linkedin.com", "twitter.com", "x.com",
            "yellowpages", "brabys.com", "mapquest.com", "yelp.com", "tripadvisor", 
            "zoominfo", "dnb.com", "google.com", "sayellow.com", "snupit.co.za", "pathcare", "ampath"
        ]
        
        for res in results:
            if not res['website_url']:
                if progress_callback: progress_callback(f"Searching web for {res['company_name']}...")
                try:
                    look_query = urllib.parse.quote(f"{res['company_name']} {location} official website")
                    page.goto(f"https://html.duckduckgo.com/html/?q={look_query}", timeout=15000)
                    page.wait_for_timeout(1000)
                    
                    search_links = page.query_selector_all('.result__a')
                    for sl in search_links[:3]:
                        href = sl.get_attribute('href')
                        if href and 'uddg=' in href:
                            actual_url = urllib.parse.unquote(href.split('uddg=')[1].split('&')[0])
                            is_directory = any(domain in actual_url.lower() for domain in exclude_domains)
                            if not is_directory and '.' in actual_url:
                                if progress_callback: progress_callback(f"→ Discovered Site: {actual_url}")
                                res['website_url'] = actual_url
                                break
                except Exception:
                    pass
            
            # Deep Inspection if we have a website
            if res['website_url']:
                if progress_callback: progress_callback(f"Inspecting tech stack for {res['company_name']}...")
                inspection = inspect_website(res['website_url'], context)
                res['inspection'] = inspection
                if inspection['emails']: res['contact_email'] = inspection['emails'][0]
        
        if progress_callback: progress_callback(f"Scrape complete. Total leads: {len(results)}")
        browser.close()
    
    return results
