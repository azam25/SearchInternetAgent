from datetime import datetime
import re
from dateutil import parser

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

def getQueryPlan(inputTask):
    # Get today's date
    today_date = datetime.today().strftime("%Y-%m-%d")
    
    # Check if the input contains a date
    detected_date = mentions_any_date_or_time(inputTask)
    # If no date is detected, append today's date
    if not detected_date:
        inputTask = f"{inputTask} (as of {today_date})"

    messages = [
        {"role": "system", "content": "You are an AI assistant designed to help break down complex questions into smaller, more specific sub-questions to facilitate effective internet searches. When a user asks a question, identify the key components and create 2 (maximum 3) sub-questions that cover each part of the original query. These sub-questions should be tailored to search for precise information on the internet. Ensure your response should be as python List of questions."},
        {"role": "user", "content": inputTask}
    ]
    return messages


def getPreciseSearchResultPlan(SearchText, userSimplifiedQuery):

    if isinstance(SearchText, list):
        SearchText = " ".join(SearchText)

    if isinstance(userSimplifiedQuery, list):
        userSimplifiedQuery = " ".join(userSimplifiedQuery)

    strPrompt = [
        {
            "role": "system",
            "content": (
                "You are a **Precision AI Specialist** - an expert in delivering concise, accurate, and professionally formatted responses. "
                "Your core strength is extracting the most relevant information and presenting it in a clear, impactful manner. "
                "You excel at distilling complex data into precise, actionable insights while maintaining the highest standards of accuracy and credibility."
            )
        },
        {
            "role": "user",
            "content": (
                f"### Source Information:\n{SearchText}\n\n"
                f"### User Query:\n{userSimplifiedQuery}\n\n"
                "### Response Requirements:\n"
                "**CRITICAL MISSION:** Provide a **precise, professional response** that delivers maximum value in minimal space.\n\n"
                "**Format Guidelines:**\n"
                "• **Main Heading**: Use # for the primary topic\n"
                "• **Key Points**: Present 3-5 most important bullet points\n"
                "• **Professional Tone**: Authoritative yet accessible\n"
                "• **Data Preservation**: Keep all numbers, dates, and names exactly as provided\n"
                "• **Source Attribution**: **MANDATORY** for every major point\n"
                "• **Logical Flow**: General → Specific → Actionable\n\n"
                "**Response Format Requirements:**\n"
                "• **MANDATORY: Use this exact JSON-like structure for each section:**\n"
                "```\n"
                "{\n"
                "  text: [Your response content here]\n"
                "  source: [Source Name]\n"
                "  url: [Actual URL]\n"
                "}\n"
                "```\n"
                "• **Every section** must follow this format exactly\n"
                "• **text:** Contains your main response content\n"
                "• **source:** Contains the source name/authority\n"
                "• **url:** Contains the actual clickable URL from the URL_SOURCES section\n"
                "• **CRITICAL:** NEVER use 'N/A' for URLs. Always use real URLs from the URL_SOURCES provided\n"
                "• **URL_SOURCES:** Use the URLs provided in the URL_SOURCES section at the end of the source material\n"
                "• Example:\n"
                "```\n"
                "{\n"
                "  text: AI has revolutionized healthcare with improved diagnostics\n"
                "  source: Microsoft AI Blog\n"
                "  url: https://blogs.microsoft.com/ai/\n"
                "}\n"
                "```\n\n"
                "**Quality Standards:**\n"
                "• **Fact Verification**: Cross-check all information against source material\n"
                "• **Consistency**: Maintain uniform formatting and style\n"
                "• **Emphasis**: Use **bold** for key terms, *italics* for definitions\n"
                "• **Readability**: Structure content for maximum impact\n"
                "• **Accuracy**: Ensure all data points are correctly represented\n\n"
                "**Final Validation:**\n"
                "✓ Response is concise yet comprehensive\n"
                "✓ All sources properly attributed with real URLs\n"
                "✓ Professional formatting and visual appeal\n"
                "✓ Information is accurate and verifiable\n"
                "✓ Content directly addresses the user's query\n\n"
                "**DELIVER:** A clean, professional answer that impresses with precision, accuracy, and comprehensive source attribution."
            )
        }
    ]

    return strPrompt


def getSearchResultPlan(SearchText, userSimplifiedQuery):

    if isinstance(SearchText, list):
        SearchText = " ".join(SearchText)

    if isinstance(userSimplifiedQuery, list):
        userSimplifiedQuery = " ".join(userSimplifiedQuery)

    strPrompt = [
        {
            "role": "system",
            "content": (
                "You are a **Deep Research AI Specialist** - an expert in creating comprehensive, professional reports that transform complex information into actionable insights. "
                "Your expertise lies in conducting thorough analysis, identifying patterns, and presenting findings in a structured, visually appealing format. "
                "You maintain the highest standards of accuracy, credibility, and professional excellence in all your responses. "
                "**CRITICAL**: When asked for deepSearch responses, you MUST generate LONG, DETAILED, COMPREHENSIVE reports (800-1200+ words) with substantial depth and analysis. "
                "This is NOT a short answer task - it's a full research report that requires extensive detail and thorough coverage."
            )
        },
        {
            "role": "user",
            "content": (
                f"### Source Material:\n{SearchText}\n\n"
                f"### Research Question:\n{userSimplifiedQuery}\n\n"
                "### Task: Create a Comprehensive Professional Report\n\n"
                "**CRITICAL LENGTH REQUIREMENT:** This MUST be a **LONG, DETAILED, COMPREHENSIVE** response. Aim for **at least 800-1200 words** with multiple detailed sections. This is NOT a short answer - it's a full research report.\n\n"
                "**Response Structure Requirements:**\n"
                "• **Executive Summary** - Detailed overview of key findings and implications (150-200 words)\n"
                "• **Main Content** - In-depth analysis organized with clear, logical headings (600-800 words)\n"
                "• **Key Insights** - Critical takeaways, trends, and strategic implications (200-300 words)\n"
                "• **Conclusion** - Summary of findings, recommendations, and future outlook (150-200 words)\n\n"
                "**Formatting Excellence Standards:**\n"
                "• **# Main Headings** - Use for primary sections (Executive Summary, Main Content, etc.)\n"
                "• **## Subheadings** - Use for subsections within main areas\n"
                "• **Bullet Points** - Present information clearly and concisely\n"
                "• **Bold Formatting** - Emphasize key terms, statistics, and important concepts\n"
                "• **Italics** - Use for definitions, explanations, and secondary information\n"
                "• **Numbered Lists** - For step-by-step processes or sequential information\n"
                "• **Tables** - When comparing multiple data points or categories\n"
                "• **Visual Elements** - Charts, graphs, or structured data representations when relevant\n\n"
                "**DEPTH ENHANCEMENT INSTRUCTIONS:**\n"
                "• **Expand Every Point**: Don't just state facts - explain them, provide context, and add analysis\n"
                "• **Add Examples**: Include specific examples, case studies, or real-world applications\n"
                "• **Provide Context**: Explain why information is important and how it relates to the broader topic\n"
                "• **Include Implications**: Discuss what the information means for the future or industry\n"
                "• **Cross-Reference**: Connect different pieces of information to show relationships\n\n"
                "**Response Format Requirements:**\n"
                "• **MANDATORY: Use this exact JSON-like structure for each section:**\n"
                "```\n"
                "{\n"
                "  text: [Your response content here]\n"
                "  source: [Source Name]\n"
                "  url: [Actual URL]\n"
                "}\n"
                "```\n"
                "• **Every section** must follow this format exactly\n"
                "• **text:** Contains your main response content\n"
                "• **source:** Contains the source name/authority\n"
                "• **url:** Contains the actual clickable URL from the URL_SOURCES section\n"
                "• **CRITICAL:** NEVER use 'N/A' for URLs. Always use real URLs from the URL_SOURCES provided\n"
                "• **URL_SOURCES:** Use the URLs provided in the URL_SOURCES section at the end of the source material\n"
                "• **Executive Summary:** Use the structured format with real URLs\n"
                "• **Main Content:** Each subsection must use the structured format with real URLs\n"
                "• **Key Insights:** Use the structured format for each insight with real URLs\n"
                "• **Conclusion:** Use the structured format with real URLs\n"
                "• Example:\n"
                "```\n"
                "{\n"
                "  text: Machine learning adoption increased by 35% in 2023\n"
                "  source: Stanford HAI AI Index Report\n"
                "  url: https://aiindex.stanford.edu/\n"
                "}\n"
                "```\n\n"
                "**Quality Assurance Requirements:**\n"
                "• **Fact Verification**: Verify all facts against the source material\n"
                "• **Data Accuracy**: Cross-check numbers, dates, and names for precision\n"
                "• **Logical Flow**: Ensure smooth transitions and logical progression between sections\n"
                "• **Formatting Consistency**: Maintain uniform style and structure throughout\n"
                "• **Completeness**: Address all aspects of the research question comprehensively\n"
                "• **Professional Tone**: Authoritative yet accessible, suitable for business audiences\n"
                "• **DEPTH REQUIREMENT**: Each section must be **thoroughly detailed** with examples, data, and analysis\n"
                "• **LENGTH ENFORCEMENT**: This response MUST be significantly longer than a precise query response\n\n"
                "**Final Validation Checklist:**\n"
                "✓ All source information accurately represented with proper attribution\n"
                "✓ Clear hierarchy with professional headings and subheadings\n"
                "✓ Consistent formatting and visual appeal throughout\n"
                "✓ Complete coverage of the research question with depth\n"
                "✓ Logical structure with smooth transitions between sections\n"
                "✓ Error-free content with professional style and tone\n"
                "✓ **Source attribution included in every section with real URLs**\n"
                "✓ Content demonstrates expertise, attention to detail, and professional excellence\n"
                "✓ **LENGTH VERIFICATION**: Response is comprehensive and detailed (800-1200+ words)\n"
                "✓ **DEPTH VERIFICATION**: Each section contains substantial detail and analysis\n\n"
                "**DELIVER:** A comprehensive report that showcases deep research capabilities, professional presentation, and comprehensive source attribution that would impress any business or academic audience."
            )
        }
    ]
    
    return strPrompt


def getPresentationPlan(SearchText, userSimplifiedQuery):

    if isinstance(SearchText, list):
        SearchText = " ".join(SearchText)

    if isinstance(userSimplifiedQuery, list):
        userSimplifiedQuery = " ".join(userSimplifiedQuery)


    POST_PROMPT = """ 
    **CRITICAL MISSION:** Generate a professional, **10-page presentation** that transforms the provided content into an impressive, business-ready slide deck. Follow these comprehensive guidelines for maximum impact:
    
    1. **Slide Structure & Design**: 
       - **Title Slide**: Professional header with clear topic identification
       - **Content Slides**: 6-8 slides with focused, well-organized information
       - **Data Visualization Slides**: 2-3 slides with charts, tables, and statistics
       - **Summary Slide**: Key takeaways and actionable insights
       - **Professional Layout**: Clean, consistent design with proper spacing and alignment
    
    2. **Visual Excellence**: 
       - **Charts & Graphs**: Always generate visual representations for numerical data
         - Bar charts: Use █ characters with proper scaling
         - Line charts: Use ─ and │ characters for trends
         - Pie charts: Use █ and ░ for proportional representation
       - **Tables**: Organize comparative data in clear, structured tables
       - **Bullet Points**: Each point on a new line for maximum readability
       - **Typography**: Use **bold** for emphasis, *italics* for definitions
    
    3. **Content Quality**: 
       - **Accuracy**: Preserve all numbers, dates, and names exactly as provided
       - **Relevance**: Focus on information that directly addresses the presentation topic
       - **Clarity**: Ensure each slide conveys a single, clear message
       - **Professional Tone**: Business-appropriate language and presentation style
    
    4. **MANDATORY Response Format Requirements**: 
       - **Every slide must use this exact JSON-like structure:**
       ```
       {
         text: [Your slide content here]
         source: [Source Name]
         url: [Actual URL]
       }
       ```
       - **text:** Contains your main slide content, bullet points, charts, etc.
       - **source:** Contains the source name/authority
       - **url:** Contains the actual clickable URL from URL_SOURCES
       - **CRITICAL:** NEVER use 'N/A' for URLs. Always use real URLs from URL_SOURCES
       - **URL_SOURCES:** Use the URLs provided in the URL_SOURCES section
    
    5. **Slide Content Guidelines**: 
       - **Title Slide**: Overview and presentation structure
       - **Content Slides**: Key points with supporting data and examples
       - **Data Slides**: Statistics, trends, and comparative analysis
       - **Summary Slides**: Conclusions, recommendations, and next steps
    
    6. **Professional Standards**: 
       - **Business Ready**: Suitable for executive presentations and board meetings
       - **Visual Appeal**: Professional color schemes and consistent formatting
       - **Credibility**: Every claim backed by proper source attribution
       - **Impact**: Content that engages and persuades the audience
    
    **DELIVER:** A presentation that demonstrates professional excellence, visual appeal, and comprehensive source attribution. Each slide should be ready for immediate use in a business environment with proper formatting, clear structure, and credible information sources.
    \n
    """
    
    
    prompt =  (
    "**PRESENTATION CREATION TASK:** The following information is provided from authoritative web sources: "
    + SearchText
    + POST_PROMPT
    + f"\n\n**PRESENTATION TOPIC:** {userSimplifiedQuery}")

    
    strPrompt = [
            {"role": "system", "content": "You are a **Professional Presentation Specialist** - an expert in creating business-ready, source-attributed presentations that impress and inform. Your expertise lies in transforming complex information into visually appealing, well-structured slide decks that maintain the highest standards of accuracy, professionalism, and credibility. You excel at creating presentations suitable for executive audiences, board meetings, and professional conferences."},
            {"role": "user", "content": prompt}]

    return strPrompt


