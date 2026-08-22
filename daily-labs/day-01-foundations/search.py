"""
Day 1: Local search baseline using BM25 scoring.

This module implements an inverted index search engine with BM25 relevance scoring.
Students will complete the implementation following the README guide.
"""

import math
from typing import List, Tuple, Dict, Optional
from collections import defaultdict


class BM25Search:
    """
    A simple BM25 search engine using an inverted index.
    
    BM25 (Best Matching 25) scores documents by term frequency and inverse
    document frequency, normalized for document length.
    """
    
    def __init__(self, documents: List[Dict[str, str]], k1: float = 1.5, b: float = 0.75):
        """
        Initialize the search engine with a list of documents.
        
        Args:
            documents: List of dicts with at minimum 'id' and 'text' keys.
                      Example: [{"id": "doc1", "text": "Python tutorial"}, ...]
            k1: BM25 parameter for term frequency saturation (default 1.5).
            b: BM25 parameter for document length normalization (default 0.75).
        
        Raises:
            ValueError: If documents is empty or any document lacks 'id' or 'text'.
        """
        if not documents:
            raise ValueError("Documents cannot be empty")
        
        for doc in documents:
            if not isinstance(doc, dict) or 'id' not in doc or 'text' not in doc:
                raise ValueError("Each document must have 'id' and 'text' keys")
        
        self.documents = documents
        self.k1 = k1
        self.b = b
        self.index = {}  # term -> [doc_ids]
        self.doc_lengths = {}  # doc_id -> length
        self.avg_doc_length = 0.0
        
        self._build_index()
    
    def _build_index(self) -> None:
        """Build the inverted index from documents."""
        # TODO: Implement this method
        # 1. Tokenize each document's text (split on whitespace, lowercase).
        # 2. For each token, append the document's ID to self.index[token].
        # 3. Store document lengths in self.doc_lengths.
        # 4. Compute self.avg_doc_length as the average of all doc lengths.
        pass
    
    def _tokenize(self, text: str) -> List[str]:
        """
        Tokenize text into terms.
        
        Args:
            text: Input text.
        
        Returns:
            List of lowercase tokens (words).
        """
        # TODO: Implement simple tokenization
        # For now, just split on whitespace and convert to lowercase.
        # Do not remove punctuation or stop words (we'll keep it simple).
        pass
    
    def _idf(self, term: str) -> float:
        """
        Compute inverse document frequency for a term.
        
        Args:
            term: The term to compute IDF for.
        
        Returns:
            IDF as log(N / (1 + df)), where N is total docs and df is doc frequency.
        """
        # TODO: Implement IDF calculation
        # - N = total number of documents
        # - df = number of documents containing the term
        # - IDF = log(N / (1 + df))
        # The +1 in denominator prevents division by zero.
        pass
    
    def _score_document(self, doc_id: str, query_terms: List[str]) -> float:
        """
        Compute BM25 score for a document given query terms.
        
        Args:
            doc_id: Document ID.
            query_terms: Tokenized query terms.
        
        Returns:
            BM25 score (float).
        """
        # TODO: Implement BM25 scoring
        # BM25 = sum over all query terms of:
        #   IDF(term) * (TF(term, doc) * (k1 + 1)) / 
        #             (TF(term, doc) + k1 * (1 - b + b * (doc_length / avg_doc_length)))
        # where:
        #   - TF(term, doc) = how many times the term appears in doc
        #   - IDF(term) = inverse document frequency
        #   - k1, b are parameters (already set in __init__)
        pass
    
    def retrieve(self, query: str, k: int = 10) -> List[Tuple[str, float]]:
        """
        Retrieve top-k documents for a query, ranked by BM25 score.
        
        Args:
            query: Query string (e.g., "python tutorial").
            k: Number of top results to return (default 10).
        
        Returns:
            List of (doc_id, score) tuples, sorted by score descending.
            Returns empty list if query is empty or no documents match.
        
        Raises:
            ValueError: If k is negative.
        """
        if k < 0:
            raise ValueError("k must be non-negative")
        
        # TODO: Implement retrieval
        # 1. If query is empty, return empty list.
        # 2. Tokenize the query.
        # 3. Score all documents using _score_document.
        # 4. Sort by score descending.
        # 5. Return top k (doc_id, score) tuples.
        pass


# Example usage (for testing):
if __name__ == "__main__":
    import json
    
    # Load sample documents
    with open("fixtures/documents.json") as f:
        docs = json.load(f)
    
    # Create search engine
    engine = BM25Search(docs)
    
    # Try a query
    query = "python tutorial"
    results = engine.retrieve(query, k=3)
    
    print(f"Query: '{query}'")
    print(f"Top {min(3, len(results))} results:")
    for doc_id, score in results:
        doc = next(d for d in docs if d["id"] == doc_id)
        print(f"  {doc_id} (score={score:.2f}): {doc['text'][:50]}...")
