from openai import OpenAI
from . import task
from . import plan
from . import tool
from . import chunkMatching
from . import config
import os
import ast
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
# Function to generate a ReAct-based response

def webSearch(lstQ):
    searchText = ""
    urlMappings = {}  # Store URL to text mappings
    
    if not isinstance(lstQ, list):
        return "No search result.."
    
    def perform_search(query):
        try:
            searchEngine = tool.WebSearch()
            urls, result = searchEngine.kick_off_search(query)
            return query, urls, result
        except Exception as exc:
            return query, [], []  # Return empty results on failure
    
    # Using ThreadPoolExecutor for parallel processing
    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(perform_search, query): query for query in lstQ}
        for future in as_completed(futures):
            query = futures[future]  # Get the query associated with this future
            try:
                query_text, urls, result = future.result()  # Get the result from the future
                searchText += '\n'.join(result) + '\n'
                
                # Store URL mappings for source attribution
                for url, text in zip(urls, result):
                    if url and text:
                        urlMappings[text[:100]] = url  # Use first 100 chars as key
                        
            except Exception as exc:
                # Skip failed queries and continue with others
                pass

    return searchText, urlMappings


def extract_list_from_text(text: str):
    # Regular expression pattern to match Python list
    pattern = re.compile(r'\[.*?\]', re.DOTALL)
    
    match = pattern.search(text)
    
    if match:
        # Extract the list string from the match
        list_str = match.group(0)
        try:
            # Convert the string representation of the list into an actual Python list
            extracted_list = ast.literal_eval(list_str)
            return extracted_list, text
        except (SyntaxError, ValueError):
            # If parsing fails, return False and the original text
            return False, text
    else:
        # If no list found, return False and the original text
        return False, text


def generateResponse(UserInput,querytype):

    matchedSearchText = ''
    if isinstance(UserInput, list):
        searchText = webSearch(UserInput)
        for queryPoint in UserInput:
            tempText  = chunkMatching.getRetrievalChunks(searchText,queryPoint, top_n=5)
            tempText = f"""
            ***********************************************
            Topic : {queryPoint}
            Details: {tempText}
            ***********************************************
            """
            matchedSearchText = matchedSearchText +'\n\n'+ tempText

            
    else :
        # First, get search queries using the query plan
        messages = plan.getQueryPlan(UserInput)  
        
        client = OpenAI(base_url=config.LLM_CONFIG["base_url"],
                        api_key=config.LLM_CONFIG["api_key"])
    
        response = client.chat.completions.create(
            model=config.LLM_CONFIG["model"],
            messages=messages,
            max_tokens=config.LLM_CONFIG["max_tokens"],
            temperature=config.LLM_CONFIG["temperature"],
        )
        
        # Extract the model's response
        model_response = response.choices[0].message.content
        lstQ,strQ = extract_list_from_text(model_response)
        
        if lstQ:
            searchText, urlMappings = webSearch(lstQ)
        else:
            searchText, urlMappings = webSearch([UserInput])
            
        # Now generate the final response based on querytype
        matchedSearchText = chunkMatching.getRetrievalChunks(searchText, UserInput, top_n=config.SEMANTIC_CONFIG["top_n"])
        
        # Add URL information to the matched text for source attribution
        matchedSearchTextWithUrls = matchedSearchText + "\n\n" + "URL_SOURCES:\n"
        for text_key, url in urlMappings.items():
            matchedSearchTextWithUrls += f"Source: {url}\n"
        
        # Generate LLM response based on querytype
        if querytype == "precise":
            print("This is precise querytype")
            messages = plan.getPreciseSearchResultPlan(matchedSearchTextWithUrls, UserInput)
        elif querytype == "deepSearch":
            print("This is deepSearch querytype")
            messages = plan.getSearchResultPlan(matchedSearchTextWithUrls, UserInput)
        elif querytype == "presentation":
            print("This is presentation querytype")
            messages = plan.getPresentationPlan(matchedSearchTextWithUrls, UserInput)
        else:
            # Default to deepSearch if querytype is not specified
            print("This is precise querytype")
            messages = plan.getPreciseSearchResultPlan(matchedSearchTextWithUrls, UserInput)
        
        # Generate the final response with query-specific token limits
        token_limit = config.QUERY_TOKEN_LIMITS.get(querytype, config.LLM_CONFIG["max_tokens"])
        response = client.chat.completions.create(
            model=config.LLM_CONFIG["model"],
            messages=messages,
            max_tokens=token_limit,
            temperature=config.LLM_CONFIG["temperature"],
        )
        
        matchedSearchText = response.choices[0].message.content

    return matchedSearchText
   
    # matchedSearchText = webSearch([UserInput])

        


def generateLLMResponse(prompt):
    
    client = OpenAI(base_url = config.LLM_CONFIG["base_url"],
                    api_key=config.LLM_CONFIG["api_key"])
    
    response = client.chat.completions.create(
        model=config.LLM_CONFIG["model"],
        messages=prompt,
        max_tokens=config.LLM_CONFIG["default_max_tokens"],
        temperature=config.LLM_CONFIG["default_temperature"],
    )

    return response.choices[0].message.content


def getCleanScrapedText(UserInput, querytype=None):
    """
    Returns only the clean scraped text from web search without LLM processing
    
    Args:
        UserInput: User's query or input (can be string or list)
    
    Returns:
        Clean scraped text from web search results
    """
    if isinstance(UserInput, list):
        # If input is already a list of queries, search directly
        searchText = webSearch(UserInput)
    else:
        # If input is a single query, break it down into sub-questions first
        messages = plan.getQueryPlan(UserInput)  
        
        client = OpenAI(base_url = config.LLM_CONFIG["base_url"],
                        api_key=config.LLM_CONFIG["api_key"])
    
        response = client.chat.completions.create(
            model=config.LLM_CONFIG["model"],
            messages=messages,
            max_tokens=config.LLM_CONFIG["max_tokens"],
            temperature=config.LLM_CONFIG["temperature"],
        )
        
        # Extract the model's response
        model_response = response.choices[0].message.content
        lstQ, strQ = extract_list_from_text(model_response)
        
        if lstQ:
            searchText = webSearch(lstQ)
        else:
            searchText = webSearch([UserInput])
    
    return searchText

def getBothOutputs(UserInput, querytype):
    """
    Returns both clean scraped text and LLM generated response
    
    Args:
        UserInput: User's query or input
        querytype: Type of query processing
    
    Returns:
        Tuple of (clean_scraped_text, llm_response)
    """
    # Get clean scraped text
    scraped_text = getCleanScrapedText(UserInput, querytype)
    
    # Get LLM response
    llm_response = generateResponse(UserInput, querytype)
    
    return scraped_text, llm_response

