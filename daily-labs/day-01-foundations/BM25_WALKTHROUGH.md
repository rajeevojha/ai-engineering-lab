# BM25 Implementation Walkthrough

A step-by-step guide to implementing BM25 with debugging help, examples, and validation.

---

## 📋 Prerequisites

Before starting this walkthrough, read:
1. [BM25_EXPLAINED.md](BM25_EXPLAINED.md) — Understand the concepts
2. [README.md](README.md) — Understand the daily rhythm and structure
3. `search.py` — Review the skeleton code and docstrings

---

## 🎯 Implementation Order

**Why this order matters:** Each method builds on the previous one, so tests work incrementally.

```
1. _tokenize()        → Break text into words
   ↓ (uses)
2. _build_index()     → Create term → [docs] mapping
   ↓ (uses)
3. _idf()             → Score term rarity
   ↓ (uses)
4. _score_document()  → Calculate BM25 for one doc
   ↓ (uses)
5. retrieve()         → Score all docs and return top-k
```

---

## Method 1: `_tokenize(text: str) -> List[str]`

### What It Should Do
Convert text into a list of lowercase words.

### Example
```python
tokenize("Hello World!") → ["hello", "world!"]
tokenize("Python Tutorial") → ["python", "tutorial"]
tokenize("") → []
tokenize("   ") → [] or ["", "", ""]  (depends on split behavior)
```

### Implementation Strategy

```python
def _tokenize(self, text: str) -> List[str]:
    """
    Simple tokenization: split on whitespace, convert to lowercase.
    """
    if not text:
        return []
    
    # Split on whitespace and convert to lowercase
    tokens = text.lower().split()
    
    # Filter out empty strings (in case of multiple spaces)
    tokens = [t for t in tokens if t]
    
    return tokens
```

### Validation Checklist
- [ ] `tokenize("hello world")` returns `["hello", "world"]`
- [ ] `tokenize("PYTHON")` returns `["python"]` (lowercase)
- [ ] `tokenize("")` returns `[]` (empty)
- [ ] `tokenize("   ")` returns `[]` (multiple spaces)
- [ ] Run: `python -m pytest test_search.py::TestTokenization -v`

### Common Mistakes
| Mistake | Problem | Fix |
|---------|---------|-----|
| Forget `.lower()` | Tests fail on case sensitivity | Add `.lower()` before split |
| Return text as-is | Doesn't break into words | Use `.split()` |
| Keep empty strings | Affects index building | Filter with `if t` |

---

## Method 2: `_build_index(self) -> None`

### What It Should Do
Create an inverted index mapping terms to document IDs.

### Example
```
Documents:
  {"id": "doc1", "text": "python tutorial"}
  {"id": "doc2", "text": "python advanced"}
  {"id": "doc3", "text": "javascript tutorial"}

Index should be:
  {
    "python": ["doc1", "doc2"],
    "tutorial": ["doc1", "doc3"],
    "advanced": ["doc2"],
    "javascript": ["doc3"]
  }

Doc lengths:
  {"doc1": 2, "doc2": 2, "doc3": 2}

Avg doc length:
  (2 + 2 + 2) / 3 = 2.0
```

### Implementation Strategy

```python
def _build_index(self) -> None:
    """Build inverted index and record document lengths."""
    self.index = {}  # term → [doc_ids]
    self.doc_lengths = {}  # doc_id → word count
    
    # Step 1: Tokenize each document and build index
    for doc in self.documents:
        doc_id = doc["id"]
        text = doc["text"]
        
        # Tokenize
        tokens = self._tokenize(text)
        
        # Record document length (number of tokens)
        self.doc_lengths[doc_id] = len(tokens)
        
        # Add each unique token to index
        # Use a set to avoid duplicates (only record doc once per token)
        for token in set(tokens):
            if token not in self.index:
                self.index[token] = []
            self.index[token].append(doc_id)
    
    # Step 2: Calculate average document length
    if self.doc_lengths:
        total_length = sum(self.doc_lengths.values())
        self.avg_doc_length = total_length / len(self.doc_lengths)
    else:
        self.avg_doc_length = 0.0
```

### Validation Checklist
- [ ] `self.index` has all unique terms as keys
- [ ] `self.index[term]` is a list of doc IDs
- [ ] Each doc ID appears only once per term (use `set()`)
- [ ] `self.doc_lengths[doc_id]` equals the token count for that doc
- [ ] `self.avg_doc_length` equals the mean of all doc lengths
- [ ] Run: `python -m pytest test_search.py::TestIndexing -v`

### Debugging Helpers
```python
# Print the index
print(f"Index: {self.index}")

# Print document lengths
print(f"Doc lengths: {self.doc_lengths}")

# Print average length
print(f"Avg length: {self.avg_doc_length}")

# Check a specific term
term = "python"
if term in self.index:
    print(f"'{term}' appears in: {self.index[term]}")
else:
    print(f"'{term}' not in index")
```

### Common Mistakes
| Mistake | Problem | Fix |
|---------|---------|-----|
| Duplicate doc IDs in index | Affects IDF calculation | Use `set(tokens)` when adding |
| Wrong doc length | Breaks length normalization | Use `len(tokens)`, not word count |
| Forget to tokenize | Index has raw text | Call `_tokenize()` first |
| Avg length = 0 | Division by zero later | Calculate after index is built |

---

## Method 3: `_idf(self, term: str) -> float`

### What It Should Do
Calculate inverse document frequency: how rare is a term?

### Formula
```
IDF(term) = log(N / (1 + df))

where:
  N = total number of documents
  df = number of documents containing the term
  (1 + df) prevents division by zero
```

### Example
```python
Corpus: 100 documents

Term "python" appears in 30 docs:
  IDF("python") = log(100 / (1 + 30)) = log(100/31) ≈ 1.16

Term "the" appears in 95 docs:
  IDF("the") = log(100 / (1 + 95)) = log(100/96) ≈ 0.04

Term "zzzzzz" appears in 0 docs:
  IDF("zzzzzz") = log(100 / (1 + 0)) = log(100) ≈ 4.61
```

### Implementation Strategy

```python
def _idf(self, term: str) -> float:
    """Calculate inverse document frequency."""
    # Count how many documents contain this term
    if term in self.index:
        doc_frequency = len(self.index[term])
    else:
        doc_frequency = 0
    
    # Total number of documents
    N = len(self.documents)
    
    # IDF formula: log(N / (1 + df))
    idf = math.log(N / (1 + doc_frequency))
    
    return idf
```

### Validation Checklist
- [ ] `_idf("common_term")` is smaller than `_idf("rare_term")`
- [ ] `_idf("unseen_term")` is positive (not negative or zero)
- [ ] Rare terms have higher IDF scores
- [ ] Run: `python -m pytest test_search.py::TestIDF -v`

### Debugging Helpers
```python
import math

# Manually calculate IDF for a term
term = "python"
if term in self.index:
    df = len(self.index[term])
else:
    df = 0
N = len(self.documents)
idf = math.log(N / (1 + df))
print(f"IDF('{term}'): df={df}, N={N}, IDF={idf:.3f}")

# Compare two terms
term1, term2 = "python", "the"
idf1 = self._idf(term1)
idf2 = self._idf(term2)
print(f"IDF('{term1}'): {idf1:.3f}")
print(f"IDF('{term2}'): {idf2:.3f}")
print(f"Rarer (higher IDF): {term1 if idf1 > idf2 else term2}")
```

### Common Mistakes
| Mistake | Problem | Fix |
|---------|---------|-----|
| Forget `(1 + df)` | Division by zero for unseen terms | Use `1 + doc_frequency` |
| Use wrong log | Can't compare across runs | Use `math.log()` (natural log) |
| Forget `math.log()` | Returns raw fraction, not IDF | Import `math` and use `math.log()` |

---

## Method 4: `_score_document(self, doc_id: str, query_terms: List[str]) -> float`

### What It Should Do
Calculate BM25 score for a document given a list of query terms.

### Formula
$$\text{Score} = \sum_{term} \text{IDF}(term) \times \frac{TF(term) \times (k_1 + 1)}{TF(term) + k_1 \times (1 - b + b \times \frac{L}{L_{avg}})}$$

### Example
```python
Document: {"id": "doc1", "text": "python python tutorial"}
Query terms: ["python", "tutorial"]
k1 = 1.5, b = 0.75

Step 1: Count term frequencies
  TF("python") = 2 (appears twice)
  TF("tutorial") = 1

Step 2: Get IDF for each term
  IDF("python") = 1.16 (example)
  IDF("tutorial") = 0.95 (example)

Step 3: Calculate length normalization factor
  L = 3 (doc has 3 tokens)
  L_avg = 5 (example)
  length_factor = 1 - 0.75 + 0.75 * (3/5) = 0.7

Step 4: Apply BM25 formula for each term
  Score("python") = 1.16 * (2 * 2.5) / (2 + 1.5 * 0.7) ≈ 2.08
  Score("tutorial") = 0.95 * (1 * 2.5) / (1 + 1.5 * 0.7) ≈ 1.37

Total score: 2.08 + 1.37 = 3.45
```

### Implementation Strategy

```python
def _score_document(self, doc_id: str, query_terms: List[str]) -> float:
    """Calculate BM25 score for a document."""
    if not query_terms:
        return 0.0
    
    score = 0.0
    
    # Get document properties
    doc_length = self.doc_lengths.get(doc_id, 0)
    if self.avg_doc_length == 0:
        return 0.0
    
    # Score for each query term
    for term in query_terms:
        # Count how many times this term appears in the document
        doc = next(d for d in self.documents if d["id"] == doc_id)
        tokens = self._tokenize(doc["text"])
        term_frequency = tokens.count(term)
        
        # Skip if term doesn't appear
        if term_frequency == 0:
            continue
        
        # Get IDF for this term
        idf = self._idf(term)
        
        # Calculate length normalization factor
        # length_factor = 1 - b + b * (L / L_avg)
        length_factor = 1 - self.b + self.b * (doc_length / self.avg_doc_length)
        
        # Apply BM25 formula
        # score += IDF * (TF * (k1 + 1)) / (TF + k1 * length_factor)
        bm25_component = idf * (term_frequency * (self.k1 + 1)) / (
            term_frequency + self.k1 * length_factor
        )
        
        score += bm25_component
    
    return score
```

### Validation Checklist
- [ ] `_score_document("doc1", [])` returns 0.0
- [ ] `_score_document("doc1", ["unseen"])` returns 0.0 or small value
- [ ] Doc with more matching terms has higher score
- [ ] Doc with query term has higher score than doc without
- [ ] Run: `python -m pytest test_search.py::TestScoring -v`

### Debugging Helpers
```python
# Score a single document
doc_id = "doc1"
query_terms = ["python", "tutorial"]
score = self._score_document(doc_id, query_terms)
print(f"Score for '{doc_id}': {score:.2f}")

# Break down by component
for term in query_terms:
    doc = next(d for d in self.documents if d["id"] == doc_id)
    tokens = self._tokenize(doc["text"])
    tf = tokens.count(term)
    idf = self._idf(term)
    print(f"  '{term}': TF={tf}, IDF={idf:.3f}, Component={tf * idf:.2f}")

# Check length normalization
doc_length = self.doc_lengths.get(doc_id, 0)
length_factor = 1 - self.b + self.b * (doc_length / self.avg_doc_length)
print(f"Length factor: {length_factor:.3f}")
```

### Common Mistakes
| Mistake | Problem | Fix |
|---------|---------|-----|
| Forget to tokenize | TF always 0 or wrong | Call `_tokenize(doc["text"])` |
| Use wrong TF count | Scores incorrect | Use `.count(term)` on tokens |
| Forget IDF multiplication | Missing the rarity signal | Multiply by `_idf(term)` |
| Wrong length factor | Normalization doesn't work | Use `1 - b + b * (L / L_avg)` |
| TF = 0 handling | Crashes or wrong score | Use `if term_frequency == 0: continue` |

---

## Method 5: `retrieve(self, query: str, k: int = 10) -> List[Tuple[str, float]]`

### What It Should Do
1. Tokenize the query
2. Score all documents
3. Sort by score descending
4. Return top-k (doc_id, score) tuples

### Example
```python
query = "python tutorial"
k = 3

Results:
  [("doc1", 3.45), ("doc3", 2.12), ("doc2", 1.89)]
```

### Implementation Strategy

```python
def retrieve(self, query: str, k: int = 10) -> List[Tuple[str, float]]:
    """Retrieve top-k documents for a query."""
    # Validation
    if k < 0:
        raise ValueError("k must be non-negative")
    
    # Empty query returns empty list
    if not query or not query.strip():
        return []
    
    # Tokenize query
    query_terms = self._tokenize(query)
    if not query_terms:
        return []
    
    # Score all documents
    scores = []
    for doc in self.documents:
        doc_id = doc["id"]
        score = self._score_document(doc_id, query_terms)
        scores.append((doc_id, score))
    
    # Sort by score descending
    scores.sort(key=lambda x: x[1], reverse=True)
    
    # Return top-k
    return scores[:k]
```

### Validation Checklist
- [ ] `retrieve("", k=5)` returns `[]`
- [ ] `retrieve("unseen_term", k=5)` returns `[]` or results with 0 score
- [ ] `retrieve("query", k=0)` returns `[]`
- [ ] `retrieve("query", k=1000)` returns all docs sorted
- [ ] Results are sorted by score descending
- [ ] Case-insensitive: "Python", "python", "PYTHON" give same results
- [ ] Run: `python -m pytest test_search.py::TestRetrieval -v`

### Debugging Helpers
```python
# Retrieve and print results
query = "python tutorial"
results = self.retrieve(query, k=5)

print(f"Query: '{query}'")
print(f"Top {len(results)} results:")
for doc_id, score in results:
    doc = next(d for d in self.documents if d["id"] == doc_id)
    print(f"  {doc_id} (score={score:.2f}): {doc['text'][:50]}...")

# Check that results are sorted
scores = [score for _, score in results]
is_sorted = scores == sorted(scores, reverse=True)
print(f"Results sorted descending: {is_sorted}")

# Test edge cases
print(f"Empty query: {self.retrieve('', k=5)}")
print(f"Unseen term: {self.retrieve('zzzzzz', k=5)}")
print(f"k=0: {self.retrieve('python', k=0)}")
```

### Common Mistakes
| Mistake | Problem | Fix |
|---------|---------|-----|
| Forget to tokenize query | Query passed as raw string to score | Call `_tokenize(query)` |
| Sort ascending instead of descending | Best results appear last | Use `reverse=True` |
| Return all docs instead of top-k | Ignores k parameter | Use `scores[:k]` |
| Forget to validate k | Crashes on negative k | Check `if k < 0: raise ValueError` |
| Forget empty query check | Crashes or returns all | Check `if not query` at start |

---

## 🧪 Full Testing Workflow

### Run Tests in Order

```bash
# Test tokenization first
python -m pytest test_search.py::TestTokenization -v

# Then indexing (uses tokenization)
python -m pytest test_search.py::TestIndexing -v

# Then IDF (uses indexing)
python -m pytest test_search.py::TestIDF -v

# Then scoring (uses indexing, IDF, and tokenization)
python -m pytest test_search.py::TestScoring -v

# Finally retrieval (uses everything)
python -m pytest test_search.py::TestRetrieval -v

# Run all tests together
python -m pytest test_search.py -v

# Run a specific failing test with output
python -m pytest test_search.py::TestTokenization::test_tokenize_simple -v -s
```

### Interactive Testing

```python
python

# Import and test
>>> from search import BM25Search
>>> import json
>>> with open('fixtures/documents.json') as f:
...     docs = json.load(f)
>>> engine = BM25Search(docs)

# Test retrieval
>>> results = engine.retrieve("python tutorial", k=3)
>>> for doc_id, score in results:
...     doc = next(d for d in docs if d["id"] == doc_id)
...     print(f"{doc_id} ({score:.2f}): {doc['text'][:60]}...")

# Test edge cases
>>> engine.retrieve("", k=5)  # Empty query
>>> engine.retrieve("zzzzzz", k=5)  # No matches
>>> engine.retrieve("python", k=1000)  # k > docs
```

---

## 🐛 Debugging Strategy

### If a Test Fails

1. **Read the test name:** It tells you what should work
   - `test_retrieve_empty_query` → empty query should return []
   - `test_idf_rare_term` → rare term IDF should be > common term IDF

2. **Read the test code:** It shows what's expected
   ```python
   results = engine.retrieve("", k=10)
   assert results == []
   ```

3. **Add print statements to your code:**
   ```python
   def retrieve(self, query, k):
       print(f"Query: '{query}'")
       query_terms = self._tokenize(query)
       print(f"Tokens: {query_terms}")
       # ... rest of code
   ```

4. **Run the specific test with output:**
   ```bash
   python -m pytest test_search.py::TestRetrieval::test_retrieve_empty_query -v -s
   ```

5. **Trace through manually:**
   - Write down the inputs
   - Work through the formula step by step
   - Compare expected output

### Common Debugging Patterns

**Pattern 1: Test fails but code looks right**
```python
# Print intermediate values
print(f"query_terms: {query_terms}")
print(f"doc_lengths: {self.doc_lengths}")
print(f"avg_doc_length: {self.avg_doc_length}")
print(f"index: {self.index}")
```

**Pattern 2: Score is always 0**
- Check: Is term in index? → `term in self.index`
- Check: Is term in document? → `term in query_terms`
- Check: Is TF > 0? → `tokens.count(term)`

**Pattern 3: Results aren't sorted**
- Check: Is sort descending? → `reverse=True`
- Check: Are scores calculated? → Run scoring debug

**Pattern 4: Case sensitivity issues**
- Check: Is tokenization lowercasing? → `.lower()`
- Check: Is index building lowercased? → trace through `_build_index()`

---

## ✅ Final Validation

Before committing, run this full checklist:

```bash
# 1. All tests pass
python -m pytest test_search.py -v

# 2. No linting errors
ruff check daily-labs/day-01-foundations/

# 3. Interactive test
python -c "
from search import BM25Search
import json
with open('daily-labs/day-01-foundations/fixtures/documents.json') as f:
    docs = json.load(f)
engine = BM25Search(docs)
results = engine.retrieve('python tutorial', k=3)
print(f'Found {len(results)} results')
for doc_id, score in results:
    print(f'  {doc_id}: {score:.2f}')
"

# 4. Git status
git status

# 5. Commit
git add daily-labs/day-01-foundations/
git commit -m "day 01: add local search baseline with BM25 scoring"
```

---

## 📖 Reference

- [BM25_EXPLAINED.md](BM25_EXPLAINED.md) — Full BM25 explanation
- [README.md](README.md) — Day 1 goals and rhythm
- `search.py` — Skeleton with docstrings
- `test_search.py` — Test cases (your specification)

---

**You've got this! Implement one method at a time, test each one, and you'll have a working BM25 search engine by the end of the day. 🚀**
