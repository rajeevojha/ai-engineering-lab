# ⚡ Quick Reference Card

## Daily Commands

```bash
# Set up (one time only)
python -m venv venv
venv\Scripts\activate  # Windows: or source venv/bin/activate
pip install -r requirements-dev.txt

# Start a day (e.g., Day 1)
git switch -c day-01-foundations
cd daily-labs/day-01-foundations
cat README.md

# While coding (after each implementation)
python -m pytest test_search.py -v          # Run tests
ruff check daily-labs/day-01-foundations/   # Lint
python                                      # Interactive testing
>>> from search import BM25Search
>>> engine = BM25Search(docs)
>>> results = engine.retrieve("query", k=5)

# Before committing
python -m pytest                            # Run all tests
ruff check .                                # Lint all
git status                                  # Check clean
git add daily-labs/day-01-foundations/
git commit -m "day 01: add local search baseline"

# After day is done
git switch main
git merge day-01-foundations
git tag day-01-complete
git push origin main --tags

# Review yesterday's work
git log --oneline -5
git show day-01-complete
```

## Day 1 Implementation Order

1. **`_tokenize(text)`** → Split and lowercase
2. **`_build_index()`** → Term → [doc_ids] mapping
3. **`_idf(term)`** → Math: `log(N / (1 + df))`
4. **`_score_document(doc_id, query_terms)`** → Sum BM25 scores
5. **`retrieve(query, k)`** → Top-k by score

## When Tests Fail

```bash
# Run one test class
python -m pytest test_search.py::TestTokenization -v

# Run one test
python -m pytest test_search.py::TestTokenization::test_tokenize_simple -v

# Show print statements
python -m pytest test_search.py -v -s

# See full traceback
python -m pytest test_search.py -v --tb=long
```

## Key Files at a Glance

| File | What | When |
|------|------|------|
| `daily-labs/day-01-foundations/README.md` | Day 1 guide | Start here |
| `daily-labs/day-01-foundations/search.py` | Your code | Implement 5 methods |
| `daily-labs/day-01-foundations/test_search.py` | Test specification | Run `pytest` |
| `memories/repo/ai-engineering-lab-progress.md` | Progress tracker | Update daily |
| `.github/agents/ai-engineering-lab-mentor.agent.md` | Teaching philosophy | Reference |

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Tests fail but code looks right | Print inputs/outputs: `print(f"Query: {query}")` |
| Can't understand BM25 | Draw it out; trace through a small example by hand |
| Lost context | Read `memories/repo/ai-engineering-lab-progress.md` |
| Stuck 20+ minutes | Review the README's "Learn and Inspect" section |
| Linting fails | Run `ruff check --fix .` (automatic fixes) |

## Test Failure Messages

```
test_retrieve_empty_query FAILED
├─ This test: engine.retrieve("", k=10) should return []
├─ Expected: []
└─ Got: [("doc1", 5.2), ...]
   → Your retrieve() method needs to check for empty query first

test_idf_rare_term FAILED
├─ This test: _idf("javascript") should be > _idf("python")
├─ Expected: IDF("javascript") > IDF("python")
└─ Got: IDF("javascript") < IDF("python")
   → "python" is actually more rare; check your document corpus
```

## Git Cheat Sheet

```bash
# Create and switch to branch
git switch -c day-01-foundations

# See what's changed
git diff

# Stage changes
git add daily-labs/day-01-foundations/

# Commit
git commit -m "day 01: add local search baseline"

# View recent commits
git log --oneline -5

# Push
git push -u origin day-01-foundations

# Merge to main
git switch main
git merge day-01-foundations

# Tag
git tag day-01-complete -m "local search baseline"
git push origin --tags
```

## Python Debugging Tips

```python
# Print variable contents
print(f"Index keys: {list(self.index.keys())}")
print(f"Doc lengths: {self.doc_lengths}")

# Check types
print(f"Type of results: {type(results)}")
print(f"First result: {results[0] if results else 'None'}")

# Trace through manually
query = "python"
tokens = self._tokenize(query)  # Should be ['python']
print(f"Tokens: {tokens}")

for doc_id in self.documents:
    score = self._score_document(doc_id, tokens)
    print(f"  {doc_id}: {score:.2f}")
```

## Success Checklist

- [ ] Read `GETTING_STARTED.md`
- [ ] Environment setup complete (`pytest --version` works)
- [ ] Branch created: `git branch` shows `day-01-foundations`
- [ ] Read `daily-labs/day-01-foundations/README.md`
- [ ] Understand BM25 concept (can explain in one sentence)
- [ ] Implement `_tokenize()` first; run `pytest test_search.py::TestTokenization`
- [ ] Implement `_build_index()`; run `pytest test_search.py::TestIndexing`
- [ ] Implement `_idf()`; run `pytest test_search.py::TestIDF`
- [ ] Implement `_score_document()`; run `pytest test_search.py::TestScoring`
- [ ] Implement `retrieve()`; run `pytest test_search.py::TestRetrieval`
- [ ] All tests pass: `pytest` (100%)
- [ ] No linting errors: `ruff check .`
- [ ] Write reflections in README
- [ ] Commit: `git commit -m "day 01: add local search baseline"`
- [ ] Push: `git push -u origin day-01-foundations`
- [ ] Merge and tag (when ready for Day 2)

---

**Print this card or bookmark it. You'll use it every day! 📌**
