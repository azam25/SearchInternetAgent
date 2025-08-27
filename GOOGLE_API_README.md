# Google Programmable Search — Get API Key & Search Engine ID (cx)

A clean, step‑by‑step guide to obtain:

- **Search Engine ID** (`cx`) from **Programmable Search Engine (PSE)**
- **API key** for the **Custom Search JSON API** in Google Cloud
- Test requests, key restrictions, pricing & quota tips

---

## Table of Contents

1. [What You’ll Set Up](#what-youll-set-up)
2. [Prerequisites](#prerequisites)
3. [Part A — Create a Programmable Search Engine (get `cx`)](#part-a)
4. [Part B — Enable the Custom Search JSON API & create an API key](#part-b)
5. [Part C — Quick Test (curl + code)](#part-c)
6. [Part D — Secure the API key (restrictions)](#part-d)
7. [Part E — Pricing & Quotas](#part-e)
8. [Troubleshooting](#troubleshooting)
9. [Copy‑Paste Checklist](#checklist)

---

## What You’ll Set Up

- A **Programmable Search Engine** (PSE) to define what the API searches
- Your **Search engine ID** (`cx`) from the PSE
- A **Google Cloud API key** with the **Custom Search JSON API** enabled

> Terminology: Google’s “Custom Search JSON API” is the HTTP API that returns JSON results from your **Programmable Search Engine**.

---

## Prerequisites

- A Google account
- Access to **Google Cloud Console** (you can create/select a project during setup)
- Basic familiarity with Cloud Console navigation (APIs & Services → Library / Credentials)

---

## Part A — Create a Programmable Search Engine (get `cx`) <a id="part-a"></a>

1. **Open the PSE Control Panel** and create a new engine  
   - Go to: https://programmablesearchengine.google.com/controlpanel/create  
   - Give it a **Name**.  
   - Under **What to search**, either:  
     - **Search specific sites or pages** (enter your domains), or  
     - **Search the entire web** (broader coverage).  
2. **Copy your Search Engine ID (`cx`)**  
   - Open your engine in the **Control Panel** → **Overview** → **Basics**.  
   - Copy **Search engine ID** — this is the `cx` you will pass to the API.  

> Tip: You can switch between “specific sites” and “entire web (emphasize included sites)” later in **Basics**. This affects the scope and ranking of results.

---

## Part B — Enable the Custom Search JSON API & create an API key <a id="part-b"></a>

1. **Enable the API**  
   - In **Google Cloud Console** → **APIs & Services → Library**  
   - Search for **Custom Search API** (`customsearch.googleapis.com`) and **Enable** it for your project.  
2. **Create an API key**  
   - Go to **APIs & Services → Credentials → Create credentials → API key**  
   - Copy the key (we’ll restrict it in the next section).

---

## Part C — Quick Test (curl + code) <a id="part-c"></a>

### REST with curl

```bash
curl -sG 'https://www.googleapis.com/customsearch/v1'   --data-urlencode 'key=YOUR_API_KEY'   --data-urlencode 'cx=YOUR_SEARCH_ENGINE_ID'   --data-urlencode 'q=site:example.com test'   --data-urlencode 'num=10'
```

### Minimal JavaScript (fetch)

```js
const params = new URLSearchParams({
  key: process.env.GOOGLE_CSE_KEY,   // store securely
  cx:  process.env.GOOGLE_CSE_CX,
  q:   "test query",
  num: "10",
});

fetch(`https://www.googleapis.com/customsearch/v1?${params}`)
  .then(r => r.json())
  .then(console.log)
  .catch(console.error);
```

### Minimal Python (requests)

```python
import os, requests

KEY = os.getenv("GOOGLE_CSE_KEY")
CX  = os.getenv("GOOGLE_CSE_CX")

resp = requests.get("https://www.googleapis.com/customsearch/v1", params={
    "key": KEY,
    "cx": CX,
    "q":  "test query",
    "num": 10
}, timeout=30)
print(resp.json())
```

---

## Part D — Secure the API key (restrictions) <a id="part-d"></a>

After creating the key, **edit** it to add restrictions:

- **Application restriction** (choose one):  
  - **HTTP referrers (websites)** — for browser‑only usage.  
  - **IP addresses** — for server‑side usage (recommended for back‑ends).  
  - *(Mobile app options exist as well, if relevant to your client).*  
- **API restriction**: restrict the key **only** to **Custom Search API**.  

> Rotate keys periodically, and never commit secrets to public repos. Use environment variables or a secret manager.

---

## Part E — Pricing & Quotas <a id="part-e"></a>

- **Custom Search JSON API**: **100 queries/day free**.  
- Beyond free: **$5 per 1,000 queries** (up to **10,000/day**).  
- If your engine searches **≤ 10 sites**, consider **Site‑Restricted JSON API** (separate SKU; typically *no daily limit* but still billable).  
- Enable billing in your Cloud project to exceed the free tier.

---

## Troubleshooting <a id="troubleshooting"></a>

- **“Invalid or missing `cx`”** → Ensure you copied **Search engine ID** from **Overview → Basics** of your PSE.  
- **“API not enabled / 403 / PERMISSION_DENIED”** → Confirm **Custom Search API** is **enabled** in your Cloud project.  
- **Empty or fewer results than google.com** → PSE emphasizes your configured scope and may not mirror full Google Web results. Adjust engine scope in **Basics**.  
- **403 after adding restrictions** → If calling from the browser, use **HTTP referrer** restrictions; for servers, use **IP** restrictions **and** API restriction to **Custom Search API**.

---

## Copy‑Paste Checklist <a id="checklist"></a>

- [ ] Create PSE → copy **Search engine ID (`cx`)**  
- [ ] Enable **Custom Search API** for your Cloud project  
- [ ] Create an **API key**  
- [ ] Add **application** restriction (HTTP referrer *or* IP)  
- [ ] Add **API** restriction → **Custom Search API** only  
- [ ] Test with `curl` / JS / Python  
- [ ] Review **pricing & quotas**

---

### License

You can reuse this README in your project. ✨
