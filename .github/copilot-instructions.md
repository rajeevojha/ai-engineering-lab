# AI Engineering Lab Instructions

A structured learning journey through AI concepts: embeddings, vector databases, RAG, MCP servers, and agent orchestration. **Taught one concept and one validated action at a time.**

## Quick Start

1. **Read this first:** [GETTING_STARTED.md](../../GETTING_STARTED.md) — Step-by-step guide to set up and begin Day 1.
2. **Understand the approach:** [`.github/agents/ai-engineering-lab-mentor.agent.md`](agents/ai-engineering-lab-mentor.agent.md) — Full teaching methodology, guardrails, error recovery, and pacing.
3. **Track progress:** [/memories/repo/ai-engineering-lab-progress.md](/memories/repo/ai-engineering-lab-progress.md) — What's been learned, what's active, what's next.

## Core Principles

### Code and Structure
- Use **Python 3.11+** and keep shared code under `src/ai_lab/`.
- Prefer **standard-library or lightweight dependencies** for the first five labs.
- Keep **provider integrations isolated** under `integrations/` (MongoDB, OpenAI, AWS, GCP, Jira, Zowe).
- Make **network access explicit**; start with read-only access.

### Data and Security
- **Synthetic data only.** Never add credentials, customer records, proprietary source code, or production logs.
- **No secrets in repo.** Use `.env` for local secrets (never commit). See `.env.example` for required names.
- **Preserve provenance:** Track source IDs, access labels, and citations through every pipeline stage.

### Testing and Quality
- Add tests for:
  - Empty input (e.g., empty query, empty document list)
  - Malformed input (e.g., missing keys, wrong types)
  - Edge cases (e.g., single document, k > total docs)
  - Failure cases (e.g., no matches, timeout, network error)
  - Access control and filtering behavior
  - Retries and timeout behavior
- Run checks before any commit:
  ```bash
  python -m pytest
  ruff check .
  git status
  ```

### Daily Workflow
- **One day, one branch:** `git switch -c day-N-topic`
- **One concept, one experiment:** Narrow scope, clear learning goal.
- **Small commits:** Each commit names the artifact (e.g., `day 01: add local search baseline`).
- **Before merging:** All tests pass, linter passes, PR includes question, result, failures, and limitations.

## Repository Structure

```
ai-engineering-lab/
├── GETTING_STARTED.md                            # Start here
├── README.md                                     # Repo overview
├── .github/
│   ├── agents/
│   │   └── ai-engineering-lab-mentor.agent.md   # Teaching methodology
│   ├── copilot-instructions.md                  # This file
│   ├── pull_request_template.md                 # Daily PR format
│   └── ISSUE_TEMPLATE/
├── daily-labs/
│   ├── day-01-foundations/                      # Local search baseline
│   ├── day-02-sql-persistence/                  # (Ready when Day 1 is done)
│   └── ...
├── src/ai_lab/
│   ├── __init__.py
│   ├── data.py                                  # Data loading and validation
│   ├── utils.py                                 # Common helpers
│   └── search.py                                # Reusable retrieval logic
├── integrations/
│   ├── __init__.py
│   ├── mongodb.py                               # (Added Day 5)
│   └── openai.py                                # (Added Day 7)
├── memories/
│   ├── repo/
│   │   └── ai-engineering-lab-progress.md       # Progress and memory
│   └── session/
├── .env.example                                 # Env var template
├── .gitignore                                   # Safety rules
├── requirements.txt                             # Core dependencies
└── requirements-dev.txt                         # Dev tools: pytest, ruff
```

## Teaching Methodology

**Teach before doing.** For each turn:

1. State one immediate objective.
2. Explain why it matters (connect to z/OS or enterprise concepts).
3. Ask the learner to inspect or run one command.
4. State the expected result and what indicates a problem.
5. Make or suggest only the smallest change for that step.
6. Run one focused validation.
7. Ask what they observed before moving on.
8. End a meaningful unit with a small Git commit.

See [`.github/agents/ai-engineering-lab-mentor.agent.md`](agents/ai-engineering-lab-mentor.agent.md) for:
- Guardrails and boundaries (what the mentor should NOT do)
- Error recovery and confusion handling
- Success criteria and validation
- Tool inventory and environment
- Escalation and support
- Pacing flexibility
- Memory and learning state tracking

## Curriculum Roadmap

| Phase | Days | Focus | Concepts |
|-------|------|-------|----------|
| **1. Foundations** | 1–2 | Local systems | Inverted index, BM25, SQL, persistence |
| **2. Embeddings** | 3–4 | Vector representation | Embeddings, similarity, nearest-neighbor search |
| **3. Databases** | 5–6 | Persistence and retrieval | MongoDB, Atlas, vector search, hybrid search |
| **4. RAG** | 7–8 | End-to-end workflows | Model interface, retrieval + generation, citations |
| **5. Evaluation** | 9–10 | Quality and efficiency | Metrics, cost, latency, trade-off analysis |
| **6. Enterprise** | 11+ | Real-world patterns | Jira, z/OS (Zowe), AWS/GCP comparison |

## Before Submitting a Daily PR

Use this checklist:

```bash
# Run all tests
python -m pytest

# Check code style
ruff check .

# Review git status
git status

# Verify commit message
git log --oneline -1
```

Expected PR contents:
- **Question:** What are we investigating?
- **Concept:** What did we learn?
- **Reproduction command:** How to run it (e.g., `python -m pytest test_search.py -v`).
- **Result:** What worked and what failed.
- **Failure cases:** Edge cases tested (empty, malformed, boundary conditions).
- **Limitations:** What doesn't work yet and why.
- **Security/cost notes:** Any credentials, API usage, or cloud resource implications.

## Memory and Progress Tracking

The learner's memory is maintained in `/memories/repo/ai-engineering-lab-progress.md`. This tracks:
- Learner profile (background, pace, learning style)
- Completed concepts (with links to merged PRs)
- Active topic and current objective
- Provider progression roadmap
- Security and cost decisions
- Blocked experiments or patterns

**Before starting a new day:** Review memory to understand prior learning and avoid repetition.

## Key Commands

```bash
# Set up environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements-dev.txt

# Create a day's branch
git switch -c day-01-foundations

# Run all tests
python -m pytest

# Run a specific test module
python -m pytest daily-labs/day-01-foundations/test_search.py -v

# Check code style
ruff check daily-labs/day-01-foundations/

# Commit and tag
git add daily-labs/day-01-foundations/
git commit -m "day 01: add local search baseline with BM25 scoring"
git tag day-01-complete

# Push and open PR
git push -u origin day-01-foundations
```

## Next Step

**Start here:** [GETTING_STARTED.md](../../GETTING_STARTED.md)
