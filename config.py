"""
Configuration file for SearchInternetAgent
Centralizes all API keys, URLs, and settings
"""

# LLM Server Configuration
LLM_CONFIG = {
    "base_url": "https://llm-server.llmhub.t-systems.net/v2",
    "api_key": "gen-9KZiEHf7VBpajUN5cfGyF4oSLBbzownmpob12gBCTl4kafrT",
    "model": "claude-sonnet-4",
    "max_tokens": 5000,
    "temperature": 0.0,
    "default_max_tokens": 3000,  # Default tokens for generateLLMResponse
    "default_temperature": 0.0   # Default temperature for generateLLMResponse
}

# Google Custom Search Configuration
GOOGLE_SEARCH_CONFIG = {
    "api_key": "AIzaSyDryk1uOsEFLiFAJ6yMgpIkHHjDHFMvHJg",
    "cse_id": "c2626a01866a0441b",
    "num_results": 5
}

# Not recommended to change any values below this line until you are not clear the outcome

# Query Type Specific Token Limits
QUERY_TOKEN_LIMITS = {
    "precise": 2000,        # Shorter responses for precise queries
    "deepSearch": 8000,     # Much longer responses for deepSearch
    "presentation": 10000   # Very long responses for presentations
}

# Web Scraping Configuration
SCRAPING_CONFIG = {
    "timeout": 5,
    "max_text_length": 4000,
    "chunk_size": 2000,
    "max_urls_to_process": 5,      # Maximum URLs to scrape
    "max_workers": 5,              # Parallel processing workers
    "initial_search_results": 10    # Initial search results before filtering
}

# Semantic Search Configuration
SEMANTIC_CONFIG = {
    "model": "all-MiniLM-L6-v2",
    "top_n": 15
}

# Output Types
OUTPUT_TYPES = {
    "SCRAPED": "scraped",      # Only clean scraped text
    "LLM": "llm",             # Only LLM generated answer
    "BOTH": "both"            # Both scraped text and LLM answer
}

# Query Types
QUERY_TYPES = {
    "PRECISE": "precise",      # 2-line concise answers
    "DEEPSEARCH": "deepSearch",    # DeepSearch reports with charts
    "PRESENTATION": "presentation"  # 10-page presentations
}
