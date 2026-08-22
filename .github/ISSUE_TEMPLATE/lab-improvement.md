---
name: Lab Improvement
about: Propose a focused, actionable enhancement to a learning experiment
title: "[Day N or Phase] Improvement: [Brief Title]"
labels: "enhancement, learning"
assignees: ""
---

## Which Day or Phase?
*Select the day or phase this improvement applies to. If general, write "General (all days)".*

- [ ] Day 1: Local search baseline
- [ ] Day 2: SQL persistence
- [ ] Day 3: Embeddings
- [ ] Day 4: Vector similarity
- [ ] Day 5: MongoDB
- [ ] Day 6: MongoDB + vector search
- [ ] Day 7: Model interface
- [ ] Day 8: Basic RAG
- [ ] Day 9: Evaluation metrics
- [ ] Day 10: Cost & latency
- [ ] Phase 6: Enterprise integration (Jira, z/OS, AWS/GCP)
- [ ] General (applies to all days or infrastructure)

## Current Behavior or Gap
*What's the current limitation? What's missing?*

*Example: "BM25 scores aren't visualized; hard to see why one doc ranked higher than another"*

## Proposed Improvement
*What specific, narrow change would help?*

**Be specific:** "Add score visualization" is good. "Make search better" is too vague.

*Example (good): "Create a table showing BM25 component scores (TF, IDF) for each result"*  
*Example (bad): "Add machine learning"*

## Why It Matters for Learning
*How does this improve understanding? Connect to enterprise concepts or the learner's goals.*

*Example: "In enterprise search (Jira, z/OS logs), operators need to understand why results rank as they do. Seeing BM25 components teaches scoring logic."*

## Expected Learning Outcome
*What new concept, skill, or mental model should the learner gain?*

*Example: "Understand the trade-off between term frequency and document rarity in BM25 scoring"*

## Success Criteria
*How will we know this improvement works? List concrete, verifiable criteria.*

- [ ] Can be implemented in a single day
- [ ] All new tests pass
- [ ] Linting passes (`ruff check .`)
- [ ] Learning outcome is validated (learner can explain or demonstrate)
- [ ] Documentation is updated

## Effort Estimate
*How long would this improvement take to implement?*

- [ ] Slice (30–60 minutes; fits in one time block)
- [ ] Full day (3–4 hours; replaces other work)
- [ ] Multiple days (2+ days; blocks other progress)
- [ ] Large project (week+; should become a separate day topic)

**Note:** If larger than a full day, consider whether this should become an official day topic instead.

## Dependencies
*Does this improvement depend on completing another day or concept first?*

*Example: "Depends on Day 5 (MongoDB) being complete" or "No dependencies; can add anytime"*

## Security & Provider Considerations
**⚠️ IMPORTANT: All data must be synthetic. No real data, credentials, or production information.**

- [ ] Data is synthetic only (no real Jira tickets, z/OS records, customer data)
- [ ] No new credentials or secrets are introduced
- [ ] No external API or provider access required (or fully documented if needed)
- [ ] No PII or sensitive information included
- [ ] Costs are documented (free tier? quota impact? cloud resources?)

*Example: "Uses 10 synthetic documents; no APIs; free tier only"*

## Anything Else?
*Additional context, concerns, or notes?*
