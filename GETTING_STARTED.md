# Next Steps: Getting Started with AI Engineering Lab

Congratulations! The repository is now scaffolded with Day 1 ready to go. Here's your path forward.

## 🎯 Immediate Actions (Next 15 minutes)

### 1. **Set up your environment**

```bash
# Navigate to the repository
cd c:\Users\Rajeev\Desktop\2026\ai-enginnering-lab2

# Create a Python virtual environment
python -m venv venv

# Activate it (Windows)
venv\Scripts\activate

# Or (macOS/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements-dev.txt
```

**Verify:**
```bash
python --version          # Should be 3.11+
pytest --version         # Should be installed
ruff --version           # Should be installed
git --version            # Should be installed
```

### 2. **Initialize git and create the Day 1 branch**

```bash
# If not already a git repo
git init

# Create and switch to Day 1 branch
git switch -c day-01-foundations

# Verify you're on the right branch
git branch
```

### 3. **Review Day 1 objectives**

```bash
cd daily-labs/day-01-foundations
cat README.md
```

Read the README carefully. It outlines the 4-hour rhythm and what you'll learn.

---

## 📚 What You Need to Understand Before Coding

Before you start implementing, ask yourself:

1. **What is BM25 scoring?** (Hint: It combines term frequency and document rarity.)
2. **Why does it matter for search?** (Hint: Enterprise systems like Jira and ServiceNow use it to rank results.)
3. **What should happen if I search for a word that appears in every document?** (Should it have low impact?)

**Mentor prompt:** *"Can you explain in one sentence why a term that appears in every document should score lower than a term that appears in just a few?"*

---

## 🧪 Start Day 1: Local Search Baseline

### Step 1: Inspect the skeleton code
```bash
cd daily-labs/day-01-foundations
cat search.py
```

Read the docstrings and `TODO` comments. You'll implement:
- `_build_index()` – Create an inverted index
- `_tokenize()` – Split text into words
- `_idf()` – Compute inverse document frequency
- `_score_document()` – Compute BM25 score for a document
- `retrieve()` – Return top-k documents ranked by score

### Step 2: Run the tests (they will fail)
```bash
python -m pytest test_search.py -v
```

You'll see ~30 test failures. That's expected. Each test is a learning guide.

### Step 3: Implement one method at a time

**Order matters:** Implement in this order:
1. `_tokenize()` – Simplest; just split and lowercase.
2. `_build_index()` – Next; build the term → [doc_ids] mapping.
3. `_idf()` – Math-heavy but short; use the docstring formula.
4. `_score_document()` – Complex; implement BM25 formula from docstring.
5. `retrieve()` – Uses everything above; sort and return top-k.

**After each implementation:**
```bash
python -m pytest test_search.py::TestTokenization -v    # Test _tokenize
python -m pytest test_search.py::TestIndexing -v         # Test _build_index
python -m pytest test_search.py::TestIDF -v              # Test _idf
python -m pytest test_search.py::TestScoring -v          # Test _score_document
python -m pytest test_search.py::TestRetrieval -v        # Test retrieve
```

### Step 4: Run all tests and fix failures

```bash
python -m pytest test_search.py -v
```

Aim for 100% passing.

### Step 5: Lint your code

```bash
ruff check daily-labs/day-01-foundations/
```

Fix any style issues.

### Step 6: Test interactively

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

You should see Python-related docs ranked first.

### Step 7: Write reflections and commit

Edit `README.md` under the "Reflections" section:
- What was trickiest about implementing BM25?
- What surprised you?
- What's one limitation of this baseline?

Then commit:
```bash
git add daily-labs/day-01-foundations/
git commit -m "day 01: add local search baseline with BM25 scoring"
```

Verify:
```bash
git log --oneline -3
```

---

## 🚀 When You're Ready for Day 2

After you've completed Day 1 and all tests pass:

1. **Merge to main:**
   ```bash
   git switch main
   git pull --ff-only
   git merge day-01-foundations
   git tag day-01-complete -m "local search baseline with BM25 scoring"
   git push origin main --tags
   ```

2. **Update memory:**
   - Open `/memories/repo/ai-engineering-lab-progress.md`
   - Move Day 1 from "Active Topic" to "Completed Concepts"
   - Record any blockers or insights

3. **Start Day 2:**
   ```bash
   git switch -c day-02-sql-persistence
   cd daily-labs/day-02-sql-persistence
   cat README.md
   ```

   Day 2 will teach you **SQLite persistence and filtering**, building on the search engine from Day 1.

---

## 📋 Key Files to Know

| File | Purpose |
|------|---------|
| `README.md` | Repo overview and structure |
| `.github/agents/ai-engineering-lab-mentor.agent.md` | Full teaching methodology and guardrails |
| `/memories/repo/ai-engineering-lab-progress.md` | Your progress tracker |
| `daily-labs/day-01-foundations/README.md` | Day 1 objectives and steps |
| `daily-labs/day-01-foundations/search.py` | Your implementation (skeleton provided) |
| `daily-labs/day-01-foundations/test_search.py` | Tests (your guide for correctness) |

---

## ⚠️ Important Reminders

1. **One step at a time.** Don't implement all methods at once; follow the order above.
2. **Use tests as a guide.** Tests are not just validation; they teach you what's expected.
3. **Preserve provenance.** (You won't need this until later, but it's a theme: every data item should track its source.)
4. **No credentials.** Only edit `.env` locally; never commit it.
5. **Commit early and often.** After each method, you can commit: `git commit -m "wip: implement _tokenize"`

---

## 🎓 If You Get Stuck

### **Stuck on the math?**
Read the docstring in `search.py` carefully. Draw it out on paper. Look at the test cases in `test_search.py`—they show what outputs are expected.

### **Tests are failing?**
1. Read the test name (e.g., `test_retrieve_empty_query`).
2. Read the test code (what input does it give, what does it expect?).
3. Trace through your implementation with that input.
4. Add print statements to debug.

### **Lost context?**
Check `/memories/repo/ai-engineering-lab-progress.md`—it summarizes what you're doing and why.

### **Still stuck after 20 minutes?**
Write down:
- What are you trying to do?
- What input did you give?
- What did you expect?
- What actually happened?

Then revisit the Day 1 README "Learn and Inspect" section for the concept explanation.

---

## 🔄 Daily Workflow Template

For every day (not just Day 1), use this rhythm:

```
00:00–00:30  Review yesterday, read today's README
00:30–01:30  Learn concept, inspect example, understand the "why"
01:30–02:30  Implement one narrow feature
02:30–03:15  Test, measure, debug failures
03:15–03:45  Document insights in README
03:45–04:00  Commit and prepare tomorrow's question
```

---

## ✅ Success Criteria for Day 1

You'll know you're done when:

- [ ] All tests in `test_search.py` pass
- [ ] `ruff check .` shows no violations
- [ ] You can explain BM25 in one sentence
- [ ] You've tested "no matches" and "empty query" cases manually
- [ ] Reflections are written in the README
- [ ] Branch is pushed and PR is opened

---

## 💡 Pro Tips

1. **Run one test at a time.** Focus on one failing test, fix it, move to the next.
2. **Use the REPL.** After implementing a method, test it interactively in Python.
3. **Measure before optimizing.** Use `time.time()` to see how fast your search is; we'll optimize later.
4. **Keep it simple.** Your tokenizer doesn't need to be fancy; just split on whitespace and lowercase.

---

**You're ready to start. Pick up at "Start Day 1: Local Search Baseline" above and let's go! 🚀**

For deeper guidance on teaching philosophy, error recovery, and the full curriculum roadmap, see [`.github/agents/ai-engineering-lab-mentor.agent.md`](.github/agents/ai-engineering-lab-mentor.agent.md).
