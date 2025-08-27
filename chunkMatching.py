from sentence_transformers import SentenceTransformer, util
from . import config
import re

# Global model instance - loaded once when module is imported
_global_model = None

def get_model():
    """Get or create the global SentenceTransformer model instance"""
    global _global_model
    if _global_model is None:
        _global_model = SentenceTransformer(config.SEMANTIC_CONFIG["model"])
        print(f"✅ Loaded SentenceTransformer model: {config.SEMANTIC_CONFIG['model']}")
    return _global_model

def find_top_matches(user_input: str, texts: list, top_n: int = None) -> list:
    if top_n is None:
        top_n = config.SEMANTIC_CONFIG["top_n"]
    
    # Use global model instance instead of loading every time
    model = get_model()

    # Encode the user input and list of texts to get their embeddings
    user_input_embedding = model.encode(user_input, convert_to_tensor=True)
    texts_embeddings = model.encode(texts, convert_to_tensor=True)

    # Compute cosine similarity between user input and each text in the list
    cosine_scores = util.pytorch_cos_sim(user_input_embedding, texts_embeddings)

    # Adjust top_n if it is greater than the number of texts
    top_n = min(top_n, len(texts))
                
    # Get the top N matches based on cosine similarity scores
    top_matches = cosine_scores.topk(top_n)

    # Extracting the top N matched texts and their similarity scores
    top_texts = [(texts[i], cosine_scores[0][i].item()) for i in top_matches.indices[0]]

    return top_texts




def split_text_into_chunks(text: str, max_chunk_size: int = None) -> list:
    if max_chunk_size is None:
        max_chunk_size = config.SCRAPING_CONFIG["chunk_size"]
    
    # Split the text into sentences
    sentences = re.split(r'(?<=[.!?]) +', text)
    
    chunks = []
    current_chunk = ""
    
    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= max_chunk_size:
            # If adding the current sentence to the chunk doesn't exceed the max size, add it
            current_chunk += sentence + " "
        else:
            # If the current chunk size exceeds the max size, add the chunk to the list and start a new chunk
            chunks.append(current_chunk.strip())
            current_chunk = sentence + " "
    
    # Add the last chunk if it's not empty
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks



def getRetrievalChunks(text, usrQuery, top_n=None):
    if top_n is None:
        top_n = config.SEMANTIC_CONFIG["top_n"]
    
    chunks = split_text_into_chunks(text, max_chunk_size=config.SCRAPING_CONFIG["chunk_size"])
    top_matches = find_top_matches(usrQuery, chunks, top_n=top_n)
    matchedText = ""
    for text, score in top_matches:
        matchedText = matchedText +'\n'+text

    return matchedText
    