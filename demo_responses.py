"""
Demo response formats for SearchInternetAgent Streamlit Chatbot
This file shows the different response structures the app can handle
"""

# Example 1: Single JSON object response
SINGLE_RESPONSE = {
    "text": "The global AI market is valued at $391 billion in 2024",
    "source": "Grand View Research",
    "url": "https://www.grandviewresearch.com/ai-market"
}

# Example 2: Multiple sections response (Deep Search)
MULTI_SECTION_RESPONSE = [
    {
        "text": "The global AI market size was valued at USD 136.55 billion in 2022 and is projected to grow from USD 164.99 billion in 2023 to USD 1,811.75 billion by 2030.",
        "source": "Fortune Business Insights",
        "url": "https://www.fortunebusinessinsights.com/artificial-intelligence-market-102114"
    },
    {
        "text": "Machine learning dominates the AI market with 38% share, followed by natural language processing at 25% and computer vision at 20%.",
        "source": "Markets and Markets",
        "url": "https://www.marketsandmarkets.com/Market-Reports/artificial-intelligence-market-74851580.html"
    },
    {
        "text": "North America leads the AI market with 42% share, while Asia-Pacific is the fastest-growing region with 35% CAGR expected through 2030.",
        "source": "Grand View Research",
        "url": "https://www.grandviewresearch.com/industry-analysis/artificial-intelligence-ai-market"
    }
]

# Example 3: Presentation format response
PRESENTATION_RESPONSE = [
    {
        "text": "Slide 1: AI Market Overview\n• Current market size: $391 billion (2024)\n• Expected growth: 37.3% CAGR through 2030\n• Key drivers: Automation, Big Data, Cloud Computing",
        "source": "McKinsey & Company",
        "url": "https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-economic-potential-of-generative-ai"
    },
    {
        "text": "Slide 2: Market Segmentation\n• By Technology: Machine Learning (38%), NLP (25%), Computer Vision (20%)\n• By Industry: Healthcare, Finance, Automotive, Retail\n• By Region: North America (42%), Asia-Pacific (35% CAGR)",
        "source": "PwC",
        "url": "https://www.pwc.com/gx/en/issues/data-and-analytics/artificial-intelligence.html"
    },
    {
        "text": "Slide 3: Future Outlook\n• 2030 projection: $1.8 trillion market size\n• Emerging trends: Edge AI, AI Ethics, Responsible AI\n• Investment focus: R&D, Talent acquisition, Infrastructure",
        "source": "Gartner",
        "url": "https://www.gartner.com/en/newsroom/press-releases/2023-08-16-gartner-identifies-four-emerging-technologies-that-will-transform-business-outcomes"
    }
]

# Example 4: Web context response (raw scraped text)
WEB_CONTEXT_RESPONSE = """
Artificial Intelligence Market Size & Share Analysis - Growth Trends & Forecasts (2024 - 2029)

The Artificial Intelligence Market size is estimated at USD 196.63 billion in 2024, and is expected to reach USD 1,811.75 billion by 2030, growing at a CAGR of 37.3% during the forecast period (2024-2030).

Key Market Insights:
- The global AI market is experiencing unprecedented growth driven by increasing adoption across industries
- Machine learning and deep learning technologies are leading the market expansion
- North America dominates the market with significant investments in AI research and development
- Healthcare, finance, and automotive sectors are major adopters of AI technologies

Market Drivers:
1. Increasing demand for automation and efficiency
2. Growing big data generation and need for analysis
3. Rising adoption of cloud-based AI solutions
4. Government initiatives and funding for AI development

Source: Markets and Markets Research
URL: https://www.marketsandmarkets.com/Market-Reports/artificial-intelligence-market-74851580.html
"""

# Example 5: Error response format
ERROR_RESPONSE = {
    "error": "Failed to process query",
    "message": "Unable to connect to search service",
    "suggestion": "Please check your internet connection and try again"
}

def format_response_for_display(response):
    """
    Format response for display in the Streamlit app
    This function shows how the app processes different response types
    """
    if isinstance(response, dict):
        if 'error' in response:
            return f"❌ Error: {response['message']}\n💡 Suggestion: {response['suggestion']}"
        elif 'text' in response and 'source' in response and 'url' in response:
            return f"📝 {response['text']}\n🔗 Source: {response['source']}\n🌐 URL: {response['url']}"
    
    elif isinstance(response, list):
        formatted = []
        for i, section in enumerate(response, 1):
            if isinstance(section, dict) and 'text' in section:
                formatted.append(f"📋 Section {i}:\n{section['text']}")
                if 'source' in section:
                    formatted.append(f"🔗 Source: {section['source']}")
                if 'url' in section:
                    formatted.append(f"🌐 URL: {section['url']}")
                formatted.append("---")
        return "\n".join(formatted)
    
    elif isinstance(response, str):
        return response
    
    return "❓ Unable to format response"

# Test the formatting
if __name__ == "__main__":
    print("🔍 SearchInternetAgent Response Format Examples")
    print("=" * 60)
    
    print("\n1️⃣ Single Response:")
    print(format_response_for_display(SINGLE_RESPONSE))
    
    print("\n2️⃣ Multi-Section Response:")
    print(format_response_for_display(MULTI_SECTION_RESPONSE))
    
    print("\n3️⃣ Presentation Response:")
    print(format_response_for_display(PRESENTATION_RESPONSE))
    
    print("\n4️⃣ Web Context Response:")
    print(format_response_for_display(WEB_CONTEXT_RESPONSE))
    
    print("\n5️⃣ Error Response:")
    print(format_response_for_display(ERROR_RESPONSE))
