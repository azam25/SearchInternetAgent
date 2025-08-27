from googleapiclient.discovery import build
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
from dateutil import parser
from dateutil.relativedelta import relativedelta
from . import config

# Global session for connection reuse
_global_session = None

def get_session():
    """Get or create a global requests session for connection reuse"""
    global _global_session
    if _global_session is None:
        _global_session = requests.Session()
        # Configure session for better performance
        _global_session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        # Connection pooling settings
        adapter = requests.adapters.HTTPAdapter(
            pool_connections=10,
            pool_maxsize=20,
            max_retries=3,
            pool_block=False
        )
        _global_session.mount('http://', adapter)
        _global_session.mount('https://', adapter)
        print("✅ Created global HTTP session with connection pooling")
    return _global_session

def mentions_any_date_or_time(query: str) -> bool:
    """
    Returns True if the user's query mentions any kind of date or time,
    including relative expressions like '2 years back', 'last month', etc.
    """
    # Some example patterns to illustrate a range of date/time references
    date_time_patterns = [
        # Absolute date formats (mm/dd/yyyy, dd-mm-yyyy, dd/mm/yy, etc.)
        r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b",
        # Month name + optional day/year (e.g., 'September', 'Sep 10', 'Sep 2023', etc.)
        r"\b(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\.?\s*\d{0,2},?\s*\d{0,4}\b",
        # Relative references
        r"\b(\d+\s*year(s)?\s*(back|ago)|\d+\s*month(s)?\s*(back|ago)|\d+\s*day(s)?\s*(back|ago))\b",
        r"\b(century|week|yesterday|today|tomorrow|tonight|last month|last week|last year)\b",
    ]
    
    # Check each pattern in the user query (case-insensitive)
    for pattern in date_time_patterns:
        if re.search(pattern, query, flags=re.IGNORECASE):
            return True
    return False

def get_date_range(query: str) -> tuple[str, str]:
    """
    Returns (startDate, endDate) in 'YYYYMMDD' format.

    Logic:
    1. If there's any date/time mention in the query:
       - Parse that date (fuzzy).
       - startDate = 1 month before parsed date
       - endDate   = 1 month after parsed date
    2. If no date is mentioned:
       - endDate   = today
       - startDate = 1 month before today
    """
    # Check if the query has a date/time mention
    if mentions_any_date_or_time(query):
        try:
            # Attempt to parse the first date/time mention from the query
            detected_date = parser.parse(query, fuzzy=True)
        except (parser.ParserError, ValueError):
            # If parsing fails (e.g., "19th century" might not parse cleanly),
            # default to today's date
            detected_date = datetime.today()
        
        # 1 month before / after
        start_dt = detected_date - relativedelta(months=1)
        end_dt = detected_date + relativedelta(months=1)
    else:
        # No date mentioned => endDate = today, startDate = 1 month before
        end_dt = datetime.today()
        start_dt = end_dt - relativedelta(months=1)
    
    # Format to 'YYYYMMDD'
    startDate = start_dt.strftime('%Y%m%d')
    endDate = end_dt.strftime('%Y%m%d')

    return startDate, endDate


class WebSearch:
    def __init__(self, num_results=None):
        if num_results is None:
            num_results = config.GOOGLE_SEARCH_CONFIG["num_results"]
        self.num_results = num_results

    def google_search(self, query, api_key, cse_id, **kwargs):  # ✅ Added `self`
        start_date, end_date = get_date_range(query)  # Returns dates as 'YYYYMMDD'
        
        service = build("customsearch", "v1", developerKey=api_key)
        
        # Use 'dateRestrict' to filter by time range (Google supports up to 1 year range)
        if start_date and end_date:
            kwargs['dateRestrict'] = f'date:r:{start_date}:{end_date}'  # ✅ Correct Format
    
        # Execute search query
        res = service.cse().list(q=query, cx=cse_id, **kwargs).execute()
    

        return res.get('items', [])

    def search_google(self, query):
        api_key = config.GOOGLE_SEARCH_CONFIG["api_key"]
        cse_id = config.GOOGLE_SEARCH_CONFIG["cse_id"]
    
        # Get more results initially for better filtering
        initial_count = config.SCRAPING_CONFIG["initial_search_results"]
        search_results = self.google_search(query, api_key, cse_id, num=initial_count)
        
        # Filter and rank URLs by relevance to query
        ranked_urls = self._rank_urls_by_relevance(query, search_results)
        
        # Return top N most relevant URLs
        max_urls = config.SCRAPING_CONFIG["max_urls_to_process"]
        return ranked_urls[:max_urls]
    
    def _rank_urls_by_relevance(self, query, search_results):
        """Rank URLs by relevance to the query using title and snippet analysis"""
        if not search_results:
            return []
        
        # Extract query keywords
        query_keywords = set(query.lower().split())
        
        ranked_results = []
        
        for result in search_results:
            if 'link' not in result:
                continue
                
            url = result.get('link')
            title = result.get('title', '').lower()
            snippet = result.get('snippet', '').lower()
            
            # Calculate relevance score
            score = 0
            
            # Title relevance (higher weight)
            for keyword in query_keywords:
                if keyword in title:
                    score += 3
                if keyword in snippet:
                    score += 1
            
            # Domain relevance (prefer authoritative sources)
            domain = self._extract_domain(url)
            if self._is_authoritative_domain(domain):
                score += 2
            
            # Freshness (prefer recent content)
            if 'date' in result:
                score += 1
            
            ranked_results.append((url, score))
        
        # Sort by score (highest first) and return URLs
        ranked_results.sort(key=lambda x: x[1], reverse=True)
        return [url for url, score in ranked_results]
    
    def _extract_domain(self, url):
        """Extract domain from URL"""
        try:
            from urllib.parse import urlparse
            return urlparse(url).netloc
        except:
            return url
    
    def _is_authoritative_domain(self, domain):
        """Check if domain is considered authoritative"""
        authoritative_domains = {
            'wikipedia.org', 'stanford.edu', 'mit.edu', 'harvard.edu', 'berkeley.edu',
            'microsoft.com', 'google.com', 'openai.com', 'anthropic.com', 'nvidia.com',
            'ieee.org', 'acm.org', 'nature.com', 'science.org', 'arxiv.org',
            'github.com', 'stackoverflow.com', 'medium.com', 'techcrunch.com'
        }
        return any(auth_domain in domain.lower() for auth_domain in authoritative_domains)
        

    def fetch_url_content(self, url):
        try:
            # Use global session for connection reuse
            session = get_session()
            response = session.get(url, timeout=config.SCRAPING_CONFIG["timeout"])
            response.raise_for_status()
            return response.text
        except (requests.RequestException, requests.Timeout):
            return None
        except Exception:
            return None

    def extract_text_from_html(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        for script in soup(["script", "style"]):
            script.decompose()  # Remove JavaScript and CSS from the HTML
        text = soup.get_text(separator=' ', strip=True)
        return ' '.join(text.split())

    def kick_off_search(self, query):
        urls = self.search_google(query)
        url_list = []
        text_list = []

        # Use ThreadPoolExecutor for parallel processing
        from concurrent.futures import ThreadPoolExecutor, as_completed
        
        def process_url(url):
            """Process a single URL and return (url, text) tuple"""
            html_content = self.fetch_url_content(url)
            if html_content:
                text = self.extract_text_from_html(html_content)
                return url, text[:config.SCRAPING_CONFIG["max_text_length"]]
            return url, None
        
        # Process URLs in parallel with timeout
        max_workers = config.SCRAPING_CONFIG["max_workers"]
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all URL processing tasks
            future_to_url = {executor.submit(process_url, url): url for url in urls}
            
            # Collect results as they complete
            for future in as_completed(future_to_url):
                url, text = future.result()
                if text:  # Only add URLs that were successfully processed
                    url_list.append(url)
                    text_list.append(text)
        
        return url_list, text_list
