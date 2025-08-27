from src.pipeline import Pipeline, SummaryParams

def test_pipeline_mock_summary():
    p = Pipeline()
    text = """Artificial intelligence enables automation and decision support.
It helps summarize documents and extract key points.
This test uses a mock backend for deterministic output."""
    res = p.summarize(text, SummaryParams(length="short", tone="neutral", backend="mock"))
    assert "summary" in res and isinstance(res["summary"], str)
    assert res["stats"]["num_chunks"] >= 1
    assert res["backend"] == "mock"
