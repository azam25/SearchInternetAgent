#!/usr/bin/env python3
"""
Test script for the enhanced parsing logic in streamlit_app.py
"""

import json
import re

def extract_json_from_markdown(text):
    """Extract JSON code blocks from markdown text"""
    json_blocks = []
    
    # Pattern to match ```json ... ``` blocks
    json_pattern = r'```json\s*([\s\S]*?)\s*```'
    matches = re.findall(json_pattern, text, re.IGNORECASE)
    
    for match in matches:
        json_str = match.strip()
        if json_str:
            json_blocks.append(json_str)
    
    # Also look for ``` ... ``` blocks (without json specifier)
    generic_pattern = r'```\s*([\s\S]*?)\s*```'
    generic_matches = re.findall(generic_pattern, text)
    
    for match in generic_matches:
        json_str = match.strip()
        # Check if it looks like JSON
        if (json_str.startswith('{') and json_str.endswith('}')) or \
           (json_str.startswith('[') and json_str.endswith(']')):
            json_blocks.append(json_str)
    
    return json_blocks

def parse_response_for_sources(response_text):
    """Parse response text to extract sections with sources from markdown + JSON responses"""
    sections = []
    
    if not isinstance(response_text, str):
        return sections
    
    # First, try to extract JSON code blocks from markdown
    json_blocks = extract_json_from_markdown(response_text)
    
    if json_blocks:
        # Process each extracted JSON block
        for json_str in json_blocks:
            try:
                data = json.loads(json_str)
                if isinstance(data, dict) and 'text' in data and 'source' in data and 'url' in data:
                    sections.append({
                        'text': data['text'],
                        'source': data['source'],
                        'url': data['url']
                    })
                elif isinstance(data, list):
                    # Handle array of objects
                    for item in data:
                        if isinstance(item, dict) and 'text' in item and 'source' in item and 'url' in item:
                            sections.append({
                                'text': item['text'],
                                'source': item['source'],
                                'url': item['url']
                            })
            except (json.JSONDecodeError, TypeError) as e:
                print(f"⚠️ Failed to parse JSON block: {str(e)[:100]}...")
                continue
    
    return sections

# Test with the actual response you received
test_response = """# AI Industry Adoption in 2025: Executive Report

## Market Growth & Investment Landscape
```json
{
  "text": "The **Generative AI market** is projected to reach **$62.72 billion in 2025** with an exceptional **CAGR of 41.53% (2025-2030)**. Global GenAI spending is expected to total **$644 billion in 2025**, representing a **76.4% increase** from 2024. Private investment reached **$33.9 billion globally in 2024**, up 18.7% from the previous year.",
  "source": "Sequencr AI Insights",
  "url": "https://www.sequencr.ai/insights/key-generative-ai-statistics-and-trends-for-2025"
}
```

## Enterprise Adoption Rates
```json
{
  "text": "**85% of organizations** already have a GenAI strategy in place, with **55% actively implementing** their strategies. In the EU, **13.48% of enterprises** with 10+ employees used AI technologies in 2024, representing a **5.45 percentage point increase** from 2023. Large enterprises lead adoption at **41.17%**, compared to **20.97%** for medium enterprises and **11.21%** for small enterprises.",
  "source": "Deloitte State of Generative AI & Eurostat",
  "url": "https://www.deloitte.com/us/en/what-we-do/capabilities/applied-artificial-intelligence/content/state-of-generative-ai-in-enterprise.html"
}
```"""

if __name__ == "__main__":
    print("🧪 Testing Enhanced Parsing Logic")
    print("=" * 50)
    
    print("\n📝 Test Response:")
    print(test_response)
    
    print("\n🔍 Extracted JSON Blocks:")
    json_blocks = extract_json_from_markdown(test_response)
    for i, block in enumerate(json_blocks):
        print(f"\nBlock {i+1}:")
        print(block)
    
    print("\n📊 Parsed Sections:")
    sections = parse_response_for_sources(test_response)
    for i, section in enumerate(sections):
        print(f"\nSection {i+1}:")
        print(f"  Text: {section['text'][:100]}...")
        print(f"  Source: {section['source']}")
        print(f"  URL: {section['url']}")
    
    print(f"\n✅ Successfully parsed {len(sections)} sections!")
