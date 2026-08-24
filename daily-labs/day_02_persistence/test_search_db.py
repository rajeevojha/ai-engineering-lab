import sqlite3

import pytest

from search_db import build_index, retrieve_filtered


def init_db(path):
    conn = sqlite3.connect(path)
    conn.execute("""CREATE TABLE documents (
        id TEXT PRIMARY KEY, text TEXT NOT NULL, module_type TEXT NOT NULL)""")
    conn.execute("""CREATE TABLE postings (
        term TEXT NOT NULL, doc_id TEXT NOT NULL, term_frequency INTEGER NOT NULL,
        FOREIGN KEY (doc_id) REFERENCES documents(id))""")
    conn.commit()
    conn.close()


@pytest.fixture
def db_path(tmp_path):
    path = str(tmp_path / "test.db")
    init_db(path)
    return path


@pytest.fixture
def sample_docs():
    return [
        {"id": "ORDPROC", "module_type": "RPG",
         "text": "order processing validates customer calculates discount calls calcdisc"},
        {"id": "CALCDISC", "module_type": "RPG",
         "text": "discount calculation reads vip indicator applies percentage discount"},
        {"id": "ORDREC", "module_type": "COPYBOOK",
         "text": "order record layout customer id discount code vip indicator"},
        {"id": "CUSTMAST", "module_type": "COBOL",
         "text": "customer master file maintenance updates customer record"},
    ]


def test_retrieve_on_empty_db(db_path):
    assert retrieve_filtered(db_path, "discount", k=5) == []


def test_filter_excludes_other_types(db_path, sample_docs):
    build_index(db_path, sample_docs)
    doc_ids = [d for d, _ in retrieve_filtered(db_path, "discount vip", module_type="RPG", k=10)]
    assert "CUSTMAST" not in doc_ids
    assert "ORDREC" not in doc_ids  # copybook, not RPG


def test_filter_matches_nothing(db_path, sample_docs):
    build_index(db_path, sample_docs)
    assert retrieve_filtered(db_path, "discount", module_type="JCL", k=10) == []


def test_reindex_overwrites_not_duplicates(db_path):
    build_index(db_path, [{"id": "ORDPROC", "module_type": "RPG", "text": "old version text"}])
    build_index(db_path, [{"id": "ORDPROC", "module_type": "RPG", "text": "new version updated"}])

    conn = sqlite3.connect(db_path)
    doc_count = conn.execute("SELECT COUNT(*) FROM documents WHERE id='ORDPROC'").fetchone()[0]
    stale_terms = conn.execute(
        "SELECT COUNT(*) FROM postings WHERE doc_id='ORDPROC' AND term='old'"
    ).fetchone()[0]
    conn.close()

    assert doc_count == 1          # documents table: overwritten correctly
    assert stale_terms == 0        # postings table: this is the bug we just fixed