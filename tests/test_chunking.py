from src.utils import chunk_by_words

def test_chunking_basic():
    txt = "\n".join(["para " * 50 for _ in range(5)])  # 5 paragraphs
    chunks = chunk_by_words(txt, target_words=120)
    assert len(chunks) >= 2
    assert all(len(c.strip()) > 0 for c in chunks)
