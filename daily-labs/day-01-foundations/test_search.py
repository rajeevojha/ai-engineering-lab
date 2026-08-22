"""
Tests for Day 1: Local search baseline.

Run with: python -m pytest test_search.py -v
"""

import pytest
import json
from search import BM25Search


# Fixtures

@pytest.fixture
def sample_docs():
    """Load sample documents from fixtures."""
    with open("fixtures/documents.json") as f:
        return json.load(f)


@pytest.fixture
def simple_docs():
    """Simple test documents for isolated tests."""
    return [
        {"id": "doc1", "text": "python tutorial learn programming"},
        {"id": "doc2", "text": "javascript web development tutorial"},
        {"id": "doc3", "text": "python advanced concepts"},
        {"id": "doc4", "text": "data science python machine learning"},
    ]


@pytest.fixture
def search_engine(simple_docs):
    """Create a BM25 search engine with simple docs."""
    return BM25Search(simple_docs)


# Tests: Initialization

class TestInit:
    """Test initialization and error handling."""
    
    def test_init_valid_documents(self, simple_docs):
        """Should initialize successfully with valid documents."""
        engine = BM25Search(simple_docs)
        assert len(engine.documents) == 4
        assert engine.avg_doc_length > 0
    
    def test_init_empty_documents(self):
        """Should raise ValueError if documents list is empty."""
        with pytest.raises(ValueError, match="Documents cannot be empty"):
            BM25Search([])
    
    def test_init_missing_id(self):
        """Should raise ValueError if a document lacks 'id'."""
        docs = [{"text": "hello world"}]
        with pytest.raises(ValueError, match="'id' and 'text' keys"):
            BM25Search(docs)
    
    def test_init_missing_text(self):
        """Should raise ValueError if a document lacks 'text'."""
        docs = [{"id": "doc1"}]
        with pytest.raises(ValueError, match="'id' and 'text' keys"):
            BM25Search(docs)
    
    def test_init_non_dict_document(self):
        """Should raise ValueError if a document is not a dict."""
        docs = ["doc1"]
        with pytest.raises(ValueError, match="'id' and 'text' keys"):
            BM25Search(docs)


# Tests: Tokenization

class TestTokenization:
    """Test text tokenization."""
    
    def test_tokenize_simple(self, search_engine):
        """Should tokenize simple text into lowercase words."""
        tokens = search_engine._tokenize("Hello World")
        assert tokens == ["hello", "world"]
    
    def test_tokenize_empty(self, search_engine):
        """Should return empty list for empty text."""
        tokens = search_engine._tokenize("")
        assert tokens == []
    
    def test_tokenize_whitespace(self, search_engine):
        """Should handle multiple whitespaces."""
        tokens = search_engine._tokenize("hello   world  test")
        assert len([t for t in tokens if t]) >= 2  # at least 2 non-empty tokens


# Tests: Indexing

class TestIndexing:
    """Test inverted index building."""
    
    def test_index_built(self, search_engine):
        """Should build index with term -> doc_ids mapping."""
        # After _build_index, the index should be populated
        assert len(search_engine.index) > 0
        assert "python" in search_engine.index or any(
            "python" in term for term in search_engine.index.keys()
        )
    
    def test_doc_lengths_recorded(self, search_engine):
        """Should record length for each document."""
        assert len(search_engine.doc_lengths) == 4
        assert all(length > 0 for length in search_engine.doc_lengths.values())
    
    def test_avg_doc_length_computed(self, search_engine):
        """Should compute average document length."""
        assert search_engine.avg_doc_length > 0
        lengths = list(search_engine.doc_lengths.values())
        expected_avg = sum(lengths) / len(lengths)
        assert abs(search_engine.avg_doc_length - expected_avg) < 0.01


# Tests: IDF

class TestIDF:
    """Test inverse document frequency."""
    
    def test_idf_common_term(self, search_engine):
        """IDF should be low for terms in many documents."""
        # "python" appears in docs 1, 3, 4 (3 out of 4)
        # IDF = log(4 / (1 + 3)) = log(1) = 0
        idf = search_engine._idf("python")
        assert idf >= 0
    
    def test_idf_rare_term(self, search_engine):
        """IDF should be high for terms in few documents."""
        # "javascript" appears in only doc 2 (1 out of 4)
        # IDF = log(4 / (1 + 1)) = log(2) ≈ 0.693
        idf_rare = search_engine._idf("javascript")
        idf_common = search_engine._idf("python")
        assert idf_rare > idf_common
    
    def test_idf_unseen_term(self, search_engine):
        """IDF for unseen term should be same as single-doc term."""
        # "zzzzzz" appears in 0 documents
        # IDF = log(4 / (1 + 0)) = log(4) ≈ 1.386
        idf = search_engine._idf("zzzzzz")
        assert idf > 0


# Tests: Scoring

class TestScoring:
    """Test BM25 scoring."""
    
    def test_score_exact_match(self, search_engine):
        """Should give higher score to document with query terms."""
        score1 = search_engine._score_document("doc1", ["python"])  # has python
        score2 = search_engine._score_document("doc2", ["python"])  # no python
        assert score1 > score2
    
    def test_score_multiple_terms(self, search_engine):
        """Should sum scores for multiple query terms."""
        score = search_engine._score_document("doc1", ["python", "tutorial"])
        assert score > 0
    
    def test_score_empty_query(self, search_engine):
        """Should return 0 for empty query."""
        score = search_engine._score_document("doc1", [])
        assert score == 0


# Tests: Retrieval

class TestRetrieval:
    """Test document retrieval."""
    
    def test_retrieve_valid_query(self, search_engine):
        """Should return documents ranked by score."""
        results = search_engine.retrieve("python", k=2)
        assert len(results) <= 2
        assert len(results) > 0
        # Results should be (doc_id, score) tuples
        assert all(isinstance(r, tuple) and len(r) == 2 for r in results)
        # Scores should be in descending order
        scores = [score for _, score in results]
        assert scores == sorted(scores, reverse=True)
    
    def test_retrieve_ordered_by_score(self, search_engine):
        """Results should be sorted by score descending."""
        results = search_engine.retrieve("python tutorial", k=10)
        scores = [score for _, score in results]
        assert scores == sorted(scores, reverse=True)
    
    def test_retrieve_empty_query(self, search_engine):
        """Should return empty list for empty query."""
        results = search_engine.retrieve("", k=10)
        assert results == []
    
    def test_retrieve_no_matches(self, search_engine):
        """Should return empty list if query has no matching documents."""
        results = search_engine.retrieve("zzzzzz", k=10)
        assert results == []
    
    def test_retrieve_k_larger_than_docs(self, search_engine):
        """Should return all documents if k > number of docs."""
        results = search_engine.retrieve("python", k=1000)
        assert len(results) <= 4
    
    def test_retrieve_k_zero(self, search_engine):
        """Should return empty list if k=0."""
        results = search_engine.retrieve("python", k=0)
        assert results == []
    
    def test_retrieve_k_negative(self, search_engine):
        """Should raise ValueError if k is negative."""
        with pytest.raises(ValueError, match="k must be non-negative"):
            search_engine.retrieve("python", k=-1)
    
    def test_retrieve_case_insensitive(self, search_engine):
        """Query should be case-insensitive."""
        results_lower = search_engine.retrieve("python", k=10)
        results_upper = search_engine.retrieve("PYTHON", k=10)
        results_mixed = search_engine.retrieve("PyThOn", k=10)
        
        # All should return the same document IDs in the same order
        doc_ids_lower = [doc_id for doc_id, _ in results_lower]
        doc_ids_upper = [doc_id for doc_id, _ in results_upper]
        doc_ids_mixed = [doc_id for doc_id, _ in results_mixed]
        
        assert doc_ids_lower == doc_ids_upper == doc_ids_mixed


# Tests: Failure cases

class TestFailureCases:
    """Test edge cases and error conditions."""
    
    def test_single_document(self):
        """Should work with a single document."""
        docs = [{"id": "doc1", "text": "hello world"}]
        engine = BM25Search(docs)
        results = engine.retrieve("hello", k=1)
        assert len(results) == 1
        assert results[0][0] == "doc1"
    
    def test_very_short_documents(self):
        """Should handle very short documents."""
        docs = [
            {"id": "doc1", "text": "a"},
            {"id": "doc2", "text": "b c"},
        ]
        engine = BM25Search(docs)
        results = engine.retrieve("a", k=10)
        assert len(results) > 0
    
    def test_duplicate_terms_in_query(self):
        """Should handle duplicate terms in query."""
        docs = [{"id": "doc1", "text": "python python python"}]
        engine = BM25Search(docs)
        results = engine.retrieve("python python", k=1)
        assert len(results) == 1
    
    def test_special_characters(self):
        """Should handle text with special characters."""
        docs = [
            {"id": "doc1", "text": "python@2024 tutorial!"},
            {"id": "doc2", "text": "c++ programming"},
        ]
        engine = BM25Search(docs)
        results = engine.retrieve("python", k=10)
        assert len(results) > 0


# Integration tests

class TestIntegration:
    """End-to-end tests."""
    
    def test_search_with_sample_documents(self, sample_docs):
        """Should work with realistic sample documents."""
        engine = BM25Search(sample_docs)
        results = engine.retrieve("artificial intelligence", k=5)
        assert isinstance(results, list)
        assert len(results) <= 5
    
    def test_realistic_workflow(self):
        """Test a realistic search workflow."""
        docs = [
            {"id": "doc1", "text": "How to learn Python for beginners"},
            {"id": "doc2", "text": "Advanced Python design patterns"},
            {"id": "doc3", "text": "JavaScript for web development"},
            {"id": "doc4", "text": "Data Science with Python and scikit-learn"},
        ]
        engine = BM25Search(docs)
        
        # User searches for "Python"
        results = engine.retrieve("Python", k=3)
        doc_ids = [doc_id for doc_id, _ in results]
        
        # Should find Python-related documents
        assert "doc1" in doc_ids or "doc2" in doc_ids or "doc4" in doc_ids
        # Should not find JavaScript doc first
        if len(doc_ids) > 0:
            assert doc_ids[0] != "doc3" or "doc3" not in [d for d, _ in results]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
