from . import llm

def SearchAgent(UserInput, querytype, output_type="llm"):
    """
    Main search agent function with output type selection
    
    Args:
        UserInput: User's query or input
        querytype: Type of query processing
        output_type: 
            - "scraped" for clean scraped text only
            - "llm" for AI-generated answer only (default)
            - "both" for both scraped text and LLM response
    
    Returns:
        Based on output_type:
        - "scraped": Clean scraped text
        - "llm": LLM generated response
        - "both": Tuple of (scraped_text, llm_response)
    """
    
    if output_type == "scraped":
        # Return only clean scraped text
        return llm.getCleanScrapedText(UserInput)
    elif output_type == "both":
        # Return both scraped text and LLM response
        return llm.getBothOutputs(UserInput, querytype)
    else:
        # Return LLM generated answer (default behavior)
        response = llm.generateResponse(UserInput, querytype)
        
        if isinstance(response, tuple):
            return response[0]
        else:
            return response
