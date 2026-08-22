# AI Engineering Lab Progress

## Learner Profile
- **Background:** Seasoned z/OS programmer with Python 3.11+ and AWS knowledge
- **Learning goal:** AI concepts, embeddings, vector databases, RAG, MCP servers, agent orchestration
- **Pace:** 4 hours/day (6 focused slices of 30–60 minutes)
- **Preferred style:** Hands-on examples, reference to enterprise/z/OS concepts, small code samples
- **Known strengths:** Structured thinking, AWS familiarity, enterprise system patterns
- **Known blockers:** (To be discovered; add notes as you learn)

## Current Status
- **Date:** 2026-08-22
- **Active branch:** (To be created: `day-01-foundations`)
- **Current topic:** Local search baseline (inverted index + BM25 scoring)
- **Progress:** Repository and Day 1 scaffold created; waiting for learner to implement

## Completed Concepts
*(None yet; will update as days are merged)*

## Active Topic (Day 1)
- **Branch:** `day-01-foundations` (ready to create)
- **Objective:** Build a local search engine using inverted index and BM25 scoring
- **Key concept:** Term frequency (TF) + Inverse document frequency (IDF) → relevance scoring
- **Why it matters:** Foundation for understanding vector search, semantic similarity, and RAG retrieval
- **Expected output:** 
  - `search.py` implemented with `BM25Search` class
  - `test_search.py` passing all 20+ tests (including empty query, no matches, k > docs)
  - Commit: `day 01: add local search baseline with BM25 scoring`
- **Estimated duration:** 3–4 hours (learner-paced)
- **Next step (Day 2):** Persistence and SQL (SQLite, schema design, filtering)

## Provider Progression Roadmap

- [x] **Repository scaffolding** — Complete
- [ ] **Phase 1: Local Foundations** (Days 1–2)
  - [ ] Day 1: Local search baseline (inverted index, BM25)
  - [ ] Day 2: Persistence and SQL (SQLite, schema, filtering)
- [ ] **Phase 2: Vector Embeddings** (Days 3–4)
  - [ ] Day 3: Compute embeddings locally (pretrained model)
  - [ ] Day 4: Vector similarity and nearest-neighbor search
- [ ] **Phase 3: Database Integration** (Days 5–6)
  - [ ] Day 5: MongoDB and Atlas (document storage, indexing)
  - [ ] Day 6: MongoDB + vector search (Atlas Search, hybrid)
- [ ] **Phase 4: Model Integration and RAG** (Days 7–8)
  - [ ] Day 7: Model interface (OpenAI or local LLM)
  - [ ] Day 8: Basic RAG (retrieval + generation, citations)
- [ ] **Phase 5: Evaluation and Optimization** (Days 9–10)
  - [ ] Day 9: Evaluation metrics (precision, recall, NDCG)
  - [ ] Day 10: Cost and latency analysis
- [ ] **Phase 6: Enterprise Integration** (Optional, learner-driven)
  - [ ] Jira as read-only source (synthetic tickets)
  - [ ] z/OS job submission via Zowe (synthetic records)
  - [ ] AWS or GCP comparison

## Security and Cost Decisions
- **Data:** Synthetic only (no real Jira, z/OS, production logs)
- **Credentials:** `.env` ignored; `.env.example` documents names only
- **Cloud:** None yet (local baseline through Day 4)
- **Models:** Starting with local/free tier; will evaluate OpenAI vs. local LLM before Day 7
- **Read-only access:** Yes, for all external systems

## Blocked or Failed Experiments
*(None yet)*

## Learner Notes and Patterns
*(To be filled in as you discover preferences, blockers, surprises)*

---

## How to Use This File

**For the mentor/Copilot:**
1. Review this file at the start of each day.
2. Update "Active Topic" with the current day's objective.
3. After each day, move the completed concept to "Completed Concepts" with a link to the merged PR.
4. Record any blockers or patterns in "Learner Notes".

**For the learner:**
1. Reference this file to see what's next after merging a day's work.
2. Add your own notes about what you found tricky or surprising.
3. Use it as a quick checkpoint before each day.

**Example entry for a completed day:**
```
- **Day 1: Local search baseline** (day-01-complete)
  - PR: #1 merged 2026-08-22
  - Concept: Inverted index + BM25 scoring
  - Notes: "Struggled with IDF normalization; found it helpful to trace through with pen and paper. Ready for Day 2."
```
