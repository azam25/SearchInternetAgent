"""
SearchInternetAgent - An AI-powered Internet Search and Information Retrieval Agent

This package provides intelligent web search and content processing capabilities
with multiple output format options.
"""

import warnings

# Try to import the full SearchAgent, fall back to simple version if dependencies missing
try:
    from .InternetSearchAgent import SearchAgent
except ImportError as e:
    warnings.warn(f"Could not load full SearchAgent due to missing dependencies: {e}")
    
    try:
        from .simple_search_agent import SimpleSearchAgent_func as SearchAgent
    except ImportError as fallback_error:
        # Last resort: create a basic function
        def SearchAgent(UserInput, querytype="deepSearch", output_type="llm"):
            error_msg = f"""
SearchInternetAgent Error: Missing Dependencies

Query: {UserInput}
Error: Could not load SearchInternetAgent due to missing dependencies.

To fix this issue:
1. Install required packages:
   pip install openai google-api-python-client beautifulsoup4 sentence-transformers python-dateutil requests nltk

2. Or fix environment conflicts:
   conda update typing_extensions
   pip install --upgrade typing_extensions

Original error: {e}
Fallback error: {fallback_error}
"""
            if output_type == "both":
                return error_msg, error_msg
            return error_msg

__version__ = "1.0.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

# Make the main function easily accessible
__all__ = ["SearchAgent"]
