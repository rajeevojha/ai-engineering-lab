python -m pytest daily_labs/day_03_embeddings -v
ruff check . --fix
git status
git add -A
git commit -m "day 03: local embeddings with sentence-transformers, brute-force cosine similarity vs BM25"
git push -u origin day-03-embeddings