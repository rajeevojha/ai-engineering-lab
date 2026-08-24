import json
import math
import re
import sqlite3
from collections import Counter
from pathlib import Path

# FIXTURES_DIR = Path(__file__).parent / "fixtures"

# from day_01_foundations import *

def db_setup(mydb: str = "mydb.db") -> None:
    # 1. Connect (creates file if it doesn't exist)
    sql1 = '''
    CREATE TABLE documents (
        id TEXT PRIMARY KEY,
        text TEXT NOT NULL,
        module_type TEXT NOT NULL   -- 'RPG', 'COBOL', or 'COPYBOOK'
    );
    '''

    sql2='''
    CREATE TABLE postings (
        term TEXT NOT NULL,
        doc_id TEXT NOT NULL,
        term_frequency INTEGER NOT NULL,
        FOREIGN KEY (doc_id) REFERENCES documents(id)
    );
    '''
    conn = sqlite3.connect(mydb)
    cursor = conn.cursor()

    # 2. Create a tble
    cursor.execute(sql1)
    cursor.execute(sql2)
    conn.commit()


    # # 4. Query data
    # cursor.execute("SELECT id, name, email FROM users")
    # rows = cursor.fetchall()
    # print(rows)

    # 5. Close connection
    conn.close()

def _tokenize(text: str) -> list[str]:
    """Same regex tokenizer as Day 1 — splits on word boundaries, lowercases."""
    return re.findall(r"\w+", text.lower())

def build_index(db_path: str, documents: list[dict]) -> None:
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    for doc in documents:
        cur.execute(
            "INSERT OR REPLACE INTO documents (id, text, module_type) VALUES (?, ?, ?)",
            (doc["id"], doc["text"], doc["module_type"]),
        )
        cur.execute("DELETE FROM postings WHERE doc_id = ?", (doc["id"],))  # ← new line

        term_counts = Counter(_tokenize(doc["text"]))
        for term, freq in term_counts.items():
            cur.execute(
                "INSERT INTO postings (term, doc_id, term_frequency) VALUES (?, ?, ?)",
                (term, doc["id"], freq),
            )

    conn.commit()
    conn.close()

def retrieve_filtered(
    db_path: str,
    query: str,
    module_type: str | None = None,
    k: int = 10,
    k1: float = 1.5,
    b: float = 0.75,
) -> list[tuple[str, float]]:
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    query_terms = _tokenize(query)
    if not query_terms:
        conn.close()
        return []

    placeholders = ",".join("?" * len(query_terms))
    if module_type:
        cur.execute(
            f"""SELECT DISTINCT p.doc_id FROM postings p
                JOIN documents d ON p.doc_id = d.id
                WHERE p.term IN ({placeholders}) AND d.module_type = ?""",
            (*query_terms, module_type),
        )
    else:
        cur.execute(
            f"SELECT DISTINCT doc_id FROM postings WHERE term IN ({placeholders})",
            query_terms,
        )
    candidates = [row[0] for row in cur.fetchall()]
    if not candidates:
        conn.close()
        return []

    cur.execute("SELECT COUNT(*) FROM documents")
    n_docs = cur.fetchone()[0]
    cur.execute("SELECT id, text FROM documents")
    doc_lengths = {row[0]: len(_tokenize(row[1])) for row in cur.fetchall()}
    avg_doc_length = sum(doc_lengths.values()) / len(doc_lengths)


    def idf(term: str) -> float:
        cur.execute("SELECT COUNT(DISTINCT doc_id) FROM postings WHERE term = ?", (term,))
        df = cur.fetchone()[0]
        return math.log((n_docs - df + 0.5) / (df + 0.5) + 1)
    idf_cache = {term: idf(term) for term in set(query_terms)}

    scored = []
    for doc_id in candidates:
        score, doc_len = 0.0, doc_lengths[doc_id]
        for term in query_terms:
            cur.execute(
                "SELECT term_frequency FROM postings WHERE term = ? AND doc_id = ?",
                (term, doc_id),
            )
            row = cur.fetchone()
            tf = row[0] if row else 0
            if tf == 0:
                continue
            numerator = tf * (k1 + 1)
            denominator = tf + k1 * (1 - b + b * (doc_len / avg_doc_length))
            score += idf_cache[term] * (numerator / denominator)
        scored.append((doc_id, score))

    conn.close()
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]

if __name__ == "__main__":
    import json
    from pathlib import Path

    FIXTURES_DIR = Path(__file__).parent / "fixtures"
    DB_FILE = Path(__file__).parent / "mydb.db"
    if not DB_FILE.exists():
        print("No existing database found — building index...")
        db_setup(str(DB_FILE))
        with open(FIXTURES_DIR / "pgms.json", "r") as f:
            documents = json.load(f)
        build_index(str(DB_FILE), documents)
    else:
        print("Using existing database.")


    with open(FIXTURES_DIR / "pgms.json", "r") as f:
        documents = json.load(f)

    build_index(DB_FILE, documents)

    print("Query: 'vip discount', filtered to RPG only")
    for doc_id, score in retrieve_filtered(DB_FILE, "vip discount", module_type="RPG", k=5):
        print(f"  {doc_id}: {score:.4f}")

    print("\nSame query, no filter")
    for doc_id, score in retrieve_filtered(DB_FILE, "vip discount", k=5):
        print(f"  {doc_id}: {score:.4f}")
