"""
Data loading and validation utilities.

Used to load synthetic documents, validate schemas, and manage test fixtures.
"""


def load_documents(filepath: str) -> list:
    """
    Load documents from a JSON file.
    
    Args:
        filepath: Path to JSON file containing list of documents.
    
    Returns:
        List of documents (each a dict with 'id' and 'text' keys).
    
    Raises:
        FileNotFoundError: If file does not exist.
        ValueError: If documents are malformed.
    """
    import json
    with open(filepath) as f:
        docs = json.load(f)
    
    if not isinstance(docs, list):
        raise ValueError("Documents must be a JSON array")
    
    for doc in docs:
        if not isinstance(doc, dict) or 'id' not in doc or 'text' not in doc:
            raise ValueError("Each document must have 'id' and 'text' keys")
    
    return docs
