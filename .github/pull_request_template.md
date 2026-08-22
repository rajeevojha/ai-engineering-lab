## Daily Learning Record: Day [N] — [Topic Name]

### 🎯 Question or Objective
What were we investigating? What was the learning goal?

*Example: "How does BM25 scoring rank documents by relevance? Can we implement it locally with just standard library?"*

### 📚 Concept Learned
What is the key concept or principle you learned today?

*Example: "BM25 combines term frequency (TF) with inverse document frequency (IDF) to score document relevance. Terms that are rare across the corpus have higher impact than common terms."*

### 🏃 Reproduction Command
How would someone reproduce this experiment end-to-end?

```bash
# Example:
cd daily-labs/day-01-foundations
python -m pytest test_search.py -v
python -c "from search import BM25Search; print(BM25Search.__doc__)"
```

### ✅ What Worked
What succeeded? What validates that the concept is understood?

- [x] All unit tests pass (30/30)
- [x] BM25 scores computed correctly (verified with manual example)
- [x] Top-k retrieval ranks by score descending
- [x] Case-insensitive query matching works
- [x] Linter (`ruff check`) passes

### ❌ What Failed or Was Tricky
What didn't work? What was counterintuitive?

- IDF formula: Initially forgot the +1 in the denominator; trace-through with pen and paper helped.
- Tokenization: Realized early that we don't need stop-word removal for this baseline; kept it simple.
- Document length normalization: Had to read the BM25 paper's formula three times.

### 🧪 Failure Cases Tested
What edge cases did you verify?

- [x] Empty query → returns empty list
- [x] Query with no matches → returns empty list
- [x] k > total documents → returns all docs sorted
- [x] Single document corpus → works correctly
- [x] Case variations (PYTHON, Python, python) → all equivalent
- [x] Multi-word query → scores sum correctly

### 📊 Limitations and Next Steps
What doesn't work? What would improve this baseline?

**Limitations:**
- No semantic understanding (can't match "Python" to "programming language")
- No handling of special characters or punctuation
- No caching of IDF scores (recalculated every retrieval)
- Doesn't preserve document metadata (only returns id and score)

**For Day 2:**
- Persist the index to SQLite
- Add metadata (title, source) to results
- Implement filtering by document source or date

### 🔒 Security & Cost Notes
Any credentials, API usage, or implications?

- **Data:** All documents are synthetic (education examples only)
- **Credentials:** None used
- **Cost:** None (local-only, standard library only)
- **Performance:** ~5 documents scored per second on laptop (not optimized; fine for baseline)

### 📝 What I'd Do Differently
Reflection on the learning process.

- I'd spend more time understanding the BM25 formula before coding
- Tokenization is deceptively simple; I over-engineered it initially
- The tests were very helpful as a specification; I followed them closely

---

## Checklist Before Merging

- [ ] All tests pass: `python -m pytest`
- [ ] No linting errors: `ruff check .`
- [ ] No uncommitted changes: `git status` is clean
- [ ] Commit message is clear: `git log -1 --oneline`
- [ ] This PR template is filled in completely
- [ ] Branch is ready to merge to `main`

## After Merge

- [ ] Tag the merge commit: `git tag day-[N]-complete`
- [ ] Update `/memories/repo/ai-engineering-lab-progress.md` with completed concept
- [ ] Plan tomorrow's topic in the memory file
