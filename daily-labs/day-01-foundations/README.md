# Day 1: Local Search Baseline

## Objective

Build a **local search engine** using an inverted index and BM25 scoring. This is the foundation for later vector search and RAG systems.

- **Concept:** How does a search engine find relevant documents? What role does scoring play?
- **Why it matters:** Enterprise search (Jira, ServiceNow, z/OS logs) relies on scoring to rank results. Understanding this baseline helps you compare vector search later.
- **Success criteria:**
  - BM25 score computed correctly for a query.
  - Top-k retrieval returns documents in score order.
  - All tests pass (including empty input, malformed input, no results).
  - Commit message names the artifact: `day 01: add local search baseline`.

## Daily Rhythm (4 hours, 6 slices)

### 00:00–00:30: Review and Question (Mentor's prep)
*Before you start coding:*
- [ ] You've read this README.
- [ ] You understand the goal: score documents by relevance to a query, return top-k results.
- [ ] You can name one limitation: (e.g., "BM25 doesn't understand synonyms").

**Mentor checkpoint:** *"What does 'relevance' mean? If I ask for 'Python code', which of these is most relevant: (a) 'Python snake', (b) 'How to write Python for loops', (c) 'I like snakes'? Why?"*

### 00:30–01:30: Learn and Inspect (Concept + Example)

**Concept: Inverted Index**

An inverted index maps terms (words) to documents. Think of a book's index at the back: when you look up "z/OS", it tells you pages 42, 67, 120.

```
Term      → Documents
"search"  → [doc1, doc3]
"engine"  → [doc2, doc3]
"python"  → [doc1]
```

**Concept: BM25 Scoring**

BM25 (Best Matching 25) scores relevance based on:
- How often a term appears in the document (term frequency, TF)
- How rare the term is across all documents (inverse document frequency, IDF)
- Document length normalization

Example: If you search "python", a short tutorial with 5 mentions scores higher than a novel with 1 mention.

**Inspect the starter code:**
```bash
cd daily-labs/day-01-foundations
cat search.py
python -c "from search import BM25Search; help(BM25Search.score)"
```

Read the docstrings. Can you explain what each method does?

### 01:30–02:30: Implement and Experiment

1. **Implement the inverted index:**
   - Add a method to build an index from documents.
   - Each document is a dict with `id` and `text`.
   - Store term → [doc_ids] mapping.

2. **Implement BM25 scoring:**
   - Compute TF (term frequency in document).
   - Compute IDF (log of inverse document frequency).
   - Multiply and sum across query terms.
   - Return a single float score.

3. **Implement top-k retrieval:**
   - Score all documents for a query.
   - Sort by score descending.
   - Return top-k document IDs and scores.

**Expected results:**
```python
search = BM25Search(docs)
results = search.retrieve("python tutorial", k=2)
# results = [("doc1", 3.45), ("doc3", 1.20)]
```

### 02:30–03:15: Test and Measure

**Run the test suite:**
```bash
python -m pytest test_search.py -v
```

**Failure cases to test:**
- Empty query: `retrieve("", k=5)` → should return empty list or raise clear error.
- Query with no matches: `retrieve("zzzzzz", k=5)` → should return empty list.
- k > number of documents: `retrieve("python", k=1000)` → should return all docs, sorted.
- Single word and multi-word queries: both should work.
- Case insensitivity: "Python", "python", "PYTHON" should behave the same.

**Measure:**
- How many documents can you score in 1 second? (Rough estimate; we'll optimize later.)
- What's the memory footprint of the index for 100 documents?

### 03:15–03:45: Document and Reflect

**Write a note in this README:**
- What was the trickiest part of implementing BM25? (Term frequency? IDF normalization?)
- What surprised you? (e.g., "Removing stop words made a big difference")
- What's one way this baseline is limited? (e.g., "Can't handle synonyms", "Doesn't understand word order")

Add your notes below under "Reflections".

### 03:45–04:00: Commit

```bash
git add daily-labs/day-01-foundations/
git commit -m "day 01: add local search baseline with BM25 scoring"
git log --oneline -3
```

## Files in This Day

```
daily-labs/day-01-foundations/
├── README.md                  # This file
├── search.py                  # Your implementation
├── test_search.py             # Test suite
└── fixtures/
    └── documents.json         # Sample data (synthetic)
```

## Quick Start

1. **Install dev tools:**
   ```bash
   cd /path/to/ai-engineering-lab
   pip install -r requirements-dev.txt
   ```

2. **Run tests:**
   ```bash
   cd daily-labs/day-01-foundations
   python -m pytest test_search.py -v
   ```

3. **Try it interactively:**
   ```bash
   python
   >>> from search import BM25Search
   >>> import json
   >>> with open('fixtures/documents.json') as f:
   ...     docs = json.load(f)
   >>> engine = BM25Search(docs)
   >>> results = engine.retrieve("python tutorial", k=3)
   >>> for doc_id, score in results:
   ...     print(f"{doc_id}: {score:.2f}")
   ```

## Reflections

*To be filled in after the day's work:*

### What was trickiest?

### What surprised me?

### One limitation of this baseline:

### Next question for Day 2:

---

**Mentor tip:** If you get stuck on the math, ask yourself: *"What should happen if I search for a term that appears in every document?"* (It should have low impact because it's not distinctive.) If your implementation does that, the logic is sound.

**Ready to move to Day 2?** Day 2 focuses on **persistence and SQL**: saving your index to SQLite, filtering by metadata, and combining text search with structured queries.
