document.addEventListener("DOMContentLoaded", () => {
    // State
    let currentNiche = "web_prime";
    let currentLeads = [];
    let pollInterval = null;
    let scrapeState = { is_running: false, found: 0, logs: [] };

    const NICHE_CONFIGS = {
        "prop_engage": { label: "PROPENGAGE AI", solution: "REAL ESTATE LEAD CAPTURE", query: "Real estate agency rental management realtor", 
            desc: "Omnichannel conversational agent for real estate lead qualification and automated viewing scheduling." },
        "biz_desk": { label: "BIZDESK AI", solution: "SME OPERATIONAL COPILOT", query: "SME office boutique accounting firm startup", 
            desc: "SME Operational Copilot for bookkeeping, HR drafting, and automated invoicing via WhatsApp." },
        "guest_flow": { label: "GUESTFLOW AI", solution: "HOSPITALITY GUEST SERVICES", query: "Boutique hotel safari lodge guesthouse", 
            desc: "Conversational guest services bot for hotels and safari lodges to manage reservations and requests." },
        "web_prime": { label: "WEBPRIME", solution: "MODERN WEB & E-COMMERCE", query: "Business local store company office boutique", 
            desc: "Modern Website & E-commerce Development built for high-growth African businesses." },
        
        "edu_match": { label: "EDUMATCH AI", solution: "COURSE & CAREER GUIDE", query: "Private college university TVET institute", 
            desc: "Predictive advisory platform matching students to university programmes based on history and aptitude." },
        "skill_bridge": { label: "SKILLBRIDGE AI", solution: "INTERNSHIP & TALENT MATCHER", query: "University career office coding bootcamp agency", 
            desc: "Semantic matching platform connecting graduates with internships based on deep skill-mapping." },
        "docu_admit": { label: "DOCUADMIT AI", solution: "ADMISSIONS OCR & VERIFICATION", query: "University registrar admissions council", 
            desc: "Document processing engine for automated extraction and verification of admissions data." },
        
        "pacra_assist": { label: "PACRA-ASSIST AI", solution: "BUSINESS REGISTRATION & RETURNS", query: "Legal consultant registrar office SME center", 
            desc: "WhatsApp-native assistant for business registration and annual compliance filings in Zambia." },
        "civic_assist": { label: "CIVICASSIST", solution: "GOV & NGO SERVICE NAVIGATOR", query: "Municipality social grant NGO home affairs", 
            desc: "AI assistant for navigating government services, grant eligibility, and documentation checklists." },
        "border_flow": { label: "BORDERFLOW AI", solution: "CUSTOMS DOCUMENT GATEWAY", query: "Logistics company freight clearing agent", 
            desc: "Platform for automated digitization and compliance checking of cross-border trade documentation." },
        
        "agri_vision": { label: "AGRIVISION BOT", solution: "CROP DISEASE DETECTION CV", query: "Agriculture cooperative input supplier NGO", 
            desc: "Computer vision tool for instant crop disease diagnosis via WhatsApp leaf photos." },
        "agri_connect": { label: "AGRICONNECT AI", solution: "FARMER REPORTING & ALERTS", query: "Farming aggregator cooperative NGO", 
            desc: "Farmer reporting and communication system for cooperatives via SMS and USSD." },
        "medi_connect": { label: "MEDICONNECT AI", solution: "CLINIC TRIAGE & APPOINTMENTS", query: "Medical clinic doctor surgery hospital", 
            desc: "Conversational triage and scheduling assistant for private clinic administration." },
        
        "credi_score": { label: "CREDISCORE AFRICA", solution: "INFORMAL CREDIT SCORING", query: "Microfinance institution SACCO digital lender", 
            desc: "AI credit risk assessment API for unbanked micro-enterprises and smallholder farmers." },
        "spaza_sync": { label: "SPAZASYNC AI", solution: "INFORMAL RETAIL FORECASTING", query: "FMCG distributor wholesaler township market", 
            desc: "Predictive inventory management tool for informal township and market retailers." }
    };

    // UI Elements
    const nicheSwitcher = document.getElementById("nicheSwitcher");
    const productLabel = document.getElementById("productLabel");
    const productSolution = document.getElementById("productSolution");
    const productDescription = document.getElementById("productDescription");
    const priceRangeInput = document.getElementById("priceRangeInput");
    const savePriceBtn = document.getElementById("savePriceBtn");
    const searchQueryInput = document.getElementById("searchQuery");
    const totalLeadsCount = document.getElementById("totalLeadsCount");
    const activeAgentsCount = document.getElementById("activeAgentsCount");
    const scrapeLogs = document.getElementById("scrapeLogs");
    const scrapeTime = document.getElementById("scrapeTime");

    // Initialize UI
    async function updateNicheUI() {
        const config = NICHE_CONFIGS[currentNiche];
        if (!config) return;
        
        productLabel.textContent = config.label;
        productSolution.textContent = config.solution;
        searchQueryInput.value = config.query;
        productDescription.textContent = "Fetching specifications...";
        
        try {
            const res = await fetch(`/api/products/${currentNiche}`);
            if (!res.ok) throw new Error("Product not found");
            const data = await res.json();
            
            productDescription.innerHTML = (data.description && data.description !== "Product description pending...") 
                ? data.description.replace(/\n/g, "<br>") 
                : config.desc.replace(/\n/g, "<br>");
                
            priceRangeInput.value = data.price_range || "$500 - $1500";
        } catch (err) {
            productDescription.innerHTML = config.desc.replace(/\n/g, "<br>");
        }
        
        loadLeads();
    }

    nicheSwitcher.addEventListener("change", (e) => {
        currentNiche = e.target.value;
        updateNicheUI();
    });

    savePriceBtn.addEventListener("click", async () => {
        const newPrice = priceRangeInput.value;
        const currentDesc = productDescription.innerText; 
        addLog(`Updating price for ${currentNiche}...`);
        try {
            const res = await fetch(`/api/products/${currentNiche}`, {
                method: "PUT",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({ price_range: newPrice, description: currentDesc })
            });
            if (res.ok) addLog("Price updated successfully.", "SYSTEM");
        } catch (err) {
            addLog("Failed to update price.", "ERROR");
        }
    });

    // Navigation
    const navBtns = document.querySelectorAll(".nav-btn");
    const views = document.querySelectorAll(".view");

    navBtns.forEach(btn => {
        btn.addEventListener("click", () => {
            navBtns.forEach(b => b.classList.remove("active"));
            views.forEach(v => v.classList.remove("active"));
            btn.classList.add("active");
            document.getElementById(btn.dataset.target).classList.add("active");
            if (btn.dataset.target === "vault") loadLeads();
            if (btn.dataset.target === "settings") loadSettings();
        });
    });

    // Logging
    function addLog(msg, type = "SYSTEM") {
        const time = new Date().toLocaleTimeString();
        scrapeLogs.innerHTML += `<div><span style="color:var(--accent)">[${time}] [${type}]</span> ${msg}</div>`;
        scrapeLogs.scrollTop = scrapeLogs.scrollHeight;
    }

    // Agent Heartbeat
    function updateAgentStatus(isRunning) {
        const dots = document.querySelectorAll(".status-dot");
        dots.forEach(dot => {
            if (isRunning) dot.className = "status-dot active";
            else dot.className = "status-dot idle";
        });
        activeAgentsCount.textContent = isRunning ? "1" : "0";
    }

    // Scraper Polling
    async function startPolling() {
        if (pollInterval) clearInterval(pollInterval);
        updateAgentStatus(true);
        
        pollInterval = setInterval(async () => {
            try {
                const res = await fetch("/api/scrape/status");
                const data = await res.json();
                
                scrapeTime.textContent = data.elapsed_seconds + "s";
                if (data.logs.length > scrapeState.logs.length) {
                    const newLogs = data.logs.slice(scrapeState.logs.length);
                    newLogs.forEach(log => addLog(log, "SCOUT"));
                    scrapeState.logs = data.logs;
                }
                
                if (!data.is_running && data.elapsed_seconds > 0) {
                    clearInterval(pollInterval);
                    updateAgentStatus(false);
                    addLog("Scout job completed.", "SYSTEM");
                    loadLeads();
                }
            } catch (err) {
                console.error("Poll error", err);
            }
        }, 1000);
    }

    // Pipeline Stage 1: Scout
    const scrapeForm = document.getElementById("scrapeForm");
    scrapeForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const query = searchQueryInput.value;
        const location = document.getElementById("locationCity").value;
        const country = document.getElementById("countryCode").value;
        
        addLog(`Initializing Scout for ${query} in ${location}...`);
        
        try {
            const res = await fetch(`/api/scrape`, {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({
                    query: query,
                    location: location,
                    country_code: country,
                    product_key: currentNiche,
                    auto_generate_copy: false
                })
            });
            if (!res.ok) throw new Error("API Error");
            startPolling();
        } catch (err) {
            addLog(`Error: ${err.message}`, "ERROR");
        }
    });

    // Pipeline Stage 2: Quantify
    const runQuantifyBtn = document.getElementById("runQuantifyBtn");
    runQuantifyBtn.addEventListener("click", async () => {
        addLog(`Initializing Specialist to quantify ${currentNiche} leads...`);
        updateAgentStatus(true);
        try {
            const res = await fetch(`/api/leads/quantify?product_key=${currentNiche}`, { method: "POST" });
            const data = await res.json();
            addLog(`Quantification complete. Processed ${data.processed} leads.`, "SPECIALIST");
            loadLeads();
        } catch (err) {
            addLog(`Error: ${err.message}`, "ERROR");
        } finally {
            updateAgentStatus(false);
        }
    });

    // Pipeline Stage 3: Reach
    const runReachBtn = document.getElementById("runReachBtn");
    runReachBtn.addEventListener("click", async () => {
        addLog(`Initializing Operative for outreach...`);
        updateAgentStatus(true);
        try {
            const res = await fetch(`/api/leads/reach?product_key=${currentNiche}`, { method: "POST" });
            const data = await res.json();
            addLog(`Outreach complete. Sent: ${data.results.sent}, Failed: ${data.results.failed}`, "OPERATIVE");
            loadLeads();
        } catch (err) {
            addLog(`Error: ${err.message}`, "ERROR");
        } finally {
            updateAgentStatus(false);
        }
    });

    // Vault
    async function loadLeads() {
        try {
            activeAgentsCount.textContent = "1";
            const res = await fetch("/api/leads");
            const allLeads = await res.json();
            
            // FILTER BY PRODUCT_KEY
            currentLeads = allLeads.filter(l => l.product_key === currentNiche);
            totalLeadsCount.textContent = currentLeads.length;
            renderLeads();
            addLog(`Sync complete. Found ${currentLeads.length} leads for ${currentNiche}.`, "SYSTEM");
        } catch (err) {
            console.error("Failed to load leads", err);
            addLog("Sync failed. Check network.", "ERROR");
        } finally {
            activeAgentsCount.textContent = "0";
        }
    }

    function renderLeads() {
        const tbody = document.getElementById("leadsTableBody");
        tbody.innerHTML = "";
        currentLeads.forEach(lead => {
            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td>${lead.company_name}</td>
                <td>${lead.location_city || 'Unknown'}</td>
                <td><span class="badge">${lead.primary_deficit || 'PENDING'}</span></td>
                <td>${lead.booking_method || 'UNKNOWN'}</td>
                <td><span class="badge" style="color:var(--accent)">${lead.lead_status}</span></td>
                <td><button class="btn secondary review-btn" style="padding:0.4rem; font-size:0.6rem" data-id="${lead.id}">REVIEW</button></td>
            `;
            tbody.appendChild(tr);
        });
        document.querySelectorAll(".review-btn").forEach(btn => {
            btn.addEventListener("click", (e) => openReviewModal(parseInt(e.target.dataset.id)));
        });
    }

    // Modal
    const reviewModal = document.getElementById("reviewModal");
    let currentLeadId = null;

    function openReviewModal(id) {
        const lead = currentLeads.find(l => l.id === id);
        if (!lead) return;
        currentLeadId = id;
        
        document.getElementById("modalCompanyName").textContent = lead.company_name;
        document.getElementById("modalDeficitBadge").textContent = lead.primary_deficit || "PENDING";
        document.getElementById("modalLocation").textContent = lead.location_city || "N/A";
        document.getElementById("modalBookingMethod").textContent = lead.booking_method || "N/A";
        
        const notesBox = document.getElementById("modalFrictionNotes");
        if (lead.metadata_json) {
            try {
                const meta = JSON.parse(lead.metadata_json);
                if (meta.suggested_cross_sell && meta.suggested_cross_sell.length > 0) {
                    const crossSells = meta.suggested_cross_sell.map(k => NICHE_CONFIGS[k]?.label || k).join(", ");
                    notesBox.innerHTML = `<strong>ANALYSIS:</strong> ${lead.friction_notes}<br><br><strong>SUGGESTED UPSELLS:</strong> ${crossSells}`;
                } else {
                    notesBox.innerHTML = `<strong>ANALYSIS:</strong> ${lead.friction_notes}`;
                }
            } catch (e) { notesBox.innerHTML = lead.friction_notes; }
        } else {
            notesBox.innerHTML = lead.friction_notes || "No analysis yet.";
        }
        
        const webUrl = document.getElementById("modalWebsiteUrl");
        if (lead.website_url) { webUrl.href = lead.website_url; webUrl.style.display = "inline"; }
        else { webUrl.style.display = "none"; }
        
        document.getElementById("modalAiCopy").value = lead.ai_generated_copy || "";
        reviewModal.classList.remove("hidden");
    }

    document.querySelector(".close-btn").addEventListener("click", () => reviewModal.classList.add("hidden"));

    document.getElementById("generateCopyBtn").addEventListener("click", async () => {
        addLog(`Agent 2 re-drafting copy for lead ID ${currentLeadId}...`);
        try {
            const res = await fetch(`/api/leads/${currentLeadId}/generate-copy`, { method: "POST" });
            const data = await res.json();
            document.getElementById("modalAiCopy").value = data.copy;
            addLog(`Copy generated successfully.`, "SPECIALIST");
            loadLeads();
        } catch (err) {
            addLog(`Copy generation failed: ${err.message}`, "ERROR");
        }
    });

    document.getElementById("saveLeadBtn").addEventListener("click", async () => {
        const newCopy = document.getElementById("modalAiCopy").value;
        try {
            const res = await fetch(`/api/leads/${currentLeadId}`, {
                method: "PUT",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({ai_generated_copy: newCopy, lead_status: "COPY_DRAFTED"})
            });
            if (res.ok) {
                addLog(`Lead approved and saved.`, "SYSTEM");
                reviewModal.classList.add("hidden");
                loadLeads();
            }
        } catch (err) {
            console.error(err);
        }
    });

    // Settings
    async function loadSettings() {
        try {
            const res = await fetch("/api/settings");
            const settings = await res.json();
            const geminiKey = settings.find(s => s.setting_key === "GEMINI_API_KEY");
            if (geminiKey) document.getElementById("geminiApiKey").value = geminiKey.setting_value;
        } catch (e) { console.error(e); }
    }

    document.getElementById("settingsForm").addEventListener("submit", async (e) => {
        e.preventDefault();
        const apiKey = document.getElementById("geminiApiKey").value;
        const status = document.getElementById("settingsStatus");
        try {
            const res = await fetch("/api/settings", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({setting_key: "GEMINI_API_KEY", setting_value: apiKey})
            });
            if (res.ok) {
                status.textContent = "CONFIG SAVED";
                status.className = "status-msg success";
            }
        } catch (err) {
            status.textContent = "SAVE FAILED";
            status.className = "status-msg error";
        }
        status.classList.remove("hidden");
    });

    // Init
    updateNicheUI();
    document.getElementById("refreshLeadsBtn").addEventListener("click", loadLeads);
    document.getElementById("clearLogs").addEventListener("click", () => scrapeLogs.innerHTML = "[SYSTEM] Logs cleared.");
});
