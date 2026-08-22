# 🎓 AI Engineering Lab — Setup Complete ✅

## What's Been Created

Your AI Engineering Lab repository is now fully scaffolded and ready for Day 1. Here's what's in place:

### ✅ Repository Structure
```
ai-engineering-lab/
├── ✅ README.md                                  (Repo overview)
├── ✅ GETTING_STARTED.md                         (Your entry point)
├── ✅ .gitignore                                 (Safety: .env, __pycache__)
├── ✅ .env.example                               (Template for secrets)
├── ✅ requirements.txt & requirements-dev.txt    (Minimal dependencies)
├── ✅ .github/
│   ├── copilot-instructions.md                  (Updated with full curriculum)
│   ├── pull_request_template.md                 (Daily learning record template)
│   └── agents/
│       └── ai-engineering-lab-mentor.agent.md   (Complete teaching methodology)
├── ✅ daily-labs/
│   └── day-01-foundations/
│       ├── README.md                            (Day 1 objectives & rhythm)
│       ├── search.py                            (Skeleton; 5 methods to implement)
│       ├── test_search.py                       (30+ comprehensive tests)
│       └── fixtures/documents.json              (10 synthetic documents)
├── ✅ src/ai_lab/
│   ├── __init__.py
│   ├── data.py                                  (Shared data utilities)
│   └── utils.py                                 (Shared helpers)
├── ✅ integrations/
│   └── __init__.py                              (Reserved for providers)
└── ✅ memories/
    └── repo/
        └── ai-engineering-lab-progress.md       (Your progress tracker)
```

### ✅ Teaching Resources
- **Agent:** Full mentor methodology with guardrails, error recovery, success criteria, tool inventory, escalation paths, pacing flexibility, completion criteria, and memory management
- **Memory system:** Progress tracking, learner profile, provider roadmap, blocked experiments, learner notes
- **Daily rhythm:** 4-hour structure with 6 focused slices (30–60 min each)
- **Tests:** Comprehensive test suite with 30+ cases covering success paths, edge cases, and failure modes

### ✅ Documentation
- Curriculum roadmap (6 phases, 10+ days)
- Provider progression (local baseline → MongoDB → OpenAI → AWS/GCP)
- Safety constraints (synthetic data, no credentials, read-only-first)
- PR template for daily learning records

---

## 📋 Your Next Steps

### **Immediate (Next 15 minutes)**
1. **Read:** [GETTING_STARTED.md](GETTING_STARTED.md)
2. **Setup:**
   ```bash
   python -m venv venv
   venv\Scripts\activate        # Windows
   # or: source venv/bin/activate  # macOS/Linux
   pip install -r requirements-dev.txt
   ```
3. **Verify:**
   ```bash
   python --version
   pytest --version
   ruff --version
   ```

### **Day 1 (3–4 hours)**
1. **Create branch:** `git switch -c day-01-foundations`
2. **Read:** [daily-labs/day-01-foundations/README.md](daily-labs/day-01-foundations/README.md)
3. **Understand:** What is BM25? Why does it matter for search?
4. **Implement:** 5 methods in `search.py` (follow the order in the README)
5. **Test:** `python -m pytest test_search.py -v`
6. **Lint:** `ruff check daily-labs/day-01-foundations/`
7. **Commit:** `git commit -m "day 01: add local search baseline with BM25 scoring"`
8. **Reflect:** Write notes in the README
9. **Push:** (When complete) `git push -u origin day-01-foundations`

### **After Day 1 is Complete**
1. **Merge:** `git switch main && git merge day-01-foundations`
2. **Tag:** `git tag day-01-complete -m "local search baseline with BM25 scoring"`
3. **Update memory:** Review `/memories/repo/ai-engineering-lab-progress.md`
4. **Next:** Review [daily-labs/day-02-sql-persistence](daily-labs/day-02-sql-persistence) (scaffold coming soon)

---

## 🎯 What You'll Learn

### Phase 1: Local Foundations (Days 1–2)
- **Day 1:** Inverted index + BM25 scoring (search relevance)
- **Day 2:** SQLite persistence + filtering (enterprise data storage)

### Phase 2: Vector Embeddings (Days 3–4)
- **Day 3:** Embedding computation (vector representation)
- **Day 4:** Similarity search (nearest neighbors, top-k retrieval)

### Phase 3: Database Integration (Days 5–6)
- **Day 5:** MongoDB + indexing (document database)
- **Day 6:** MongoDB vector search (Atlas Search, hybrid retrieval)

### Phase 4: RAG Systems (Days 7–8)
- **Day 7:** Model interface (OpenAI or local LLM)
- **Day 8:** Basic RAG (retrieval + generation, citations preserved)

### Phase 5: Evaluation & Optimization (Days 9–10)
- **Day 9:** Metrics (precision, recall, NDCG)
- **Day 10:** Cost & latency analysis (tradeoffs)

### Phase 6: Enterprise Integration (Days 11+, optional)
- Jira as knowledge source (read-only, synthetic data)
- z/OS via Zowe (synthetic job records)
- AWS vs. GCP comparison

---

## 💡 Key Principles

### Teaching Methodology
- **One concept, one validated action at a time**
- Teach before doing (explain, then implement)
- Ask you to observe and reflect
- Small commits with clear messages
- Tests as specification, not afterthought

### Repository Safety
- **Synthetic data only** (no real Jira, z/OS, or credentials)
- **`.env` ignored** (use `.env.example` as template)
- **Read-only first** (start with passive data access)
- **Preserve provenance** (track source IDs, citations, access labels)

### Quality and Testing
- **Comprehensive tests** (success, edge cases, failures)
- **Code quality** (ruff linting, 100% passing tests)
- **Git discipline** (one branch, small commits, clear messages)

---

## 📚 File Reference

| File | Read First | Frequency |
|------|------------|-----------|
| [GETTING_STARTED.md](GETTING_STARTED.md) | ✅ **NOW** | Once (startup) |
| [README.md](README.md) | ✅ Today | Reference |
| [.github/agents/ai-engineering-lab-mentor.agent.md](.github/agents/ai-engineering-lab-mentor.agent.md) | After Day 1 | Once (deep dive) |
| [.github/copilot-instructions.md](.github/copilot-instructions.md) | Anytime | Reference |
| [memories/repo/ai-engineering-lab-progress.md](memories/repo/ai-engineering-lab-progress.md) | **Daily** | Every morning |
| [daily-labs/day-01-foundations/README.md](daily-labs/day-01-foundations/README.md) | ✅ Today | Startup |

---

## 🚀 Ready to Begin?

**Start here:** [GETTING_STARTED.md](GETTING_STARTED.md)

You'll find step-by-step instructions for:
1. Environment setup (venv, dependencies)
2. Git branching strategy
3. Day 1 implementation (BM25 search engine)
4. How to test and debug
5. When to move to Day 2

---

## ❓ Questions?

- **How does BM25 work?** Read the "Learn and Inspect" section in [daily-labs/day-01-foundations/README.md](daily-labs/day-01-foundations/README.md)
- **How should I pace myself?** See [.github/agents/ai-engineering-lab-mentor.agent.md#pacing-flexibility](.github/agents/ai-engineering-lab-mentor.agent.md#pacing-flexibility)
- **What if I get stuck?** See [.github/agents/ai-engineering-lab-mentor.agent.md#error-recovery-and-confusion-handling](.github/agents/ai-engineering-lab-mentor.agent.md#error-recovery-and-confusion-handling)
- **How do I track my progress?** Update [/memories/repo/ai-engineering-lab-progress.md](/memories/repo/ai-engineering-lab-progress.md) daily

---

## ✨ You're Ready

The scaffolding is complete. All you need to do is:
1. Follow [GETTING_STARTED.md](GETTING_STARTED.md)
2. Implement the 5 methods in `search.py`
3. Make sure all tests pass
4. Commit your work
5. Reflect and move to Day 2

Good luck! 🎯
