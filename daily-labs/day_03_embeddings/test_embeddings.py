import numpy as np

from embeddings import cosine_sim, embed_texts, embedding_retrieve


def test_embed_single_text_shape():
    vecs = embed_texts(["hello world"])
    assert vecs.shape == (1, 384)


def test_cosine_sim_identical_vectors():
    v = np.array([1.0, 2.0, 3.0])
    assert abs(cosine_sim(v, v) - 1.0) < 1e-6


def test_embedding_retrieve_empty_documents():
    results = embedding_retrieve("query", [], k=5)
    assert results == []