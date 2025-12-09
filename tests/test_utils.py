from app.utils import clean_text

def test_clean_text_basic():
    assert clean_text(" hello   world ") == "hello world"
