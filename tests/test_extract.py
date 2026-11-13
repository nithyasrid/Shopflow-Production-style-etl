import pytest
import requests
from shopflow.extract import extract_carts

class FakeResponse:
    def __init__(self, payload): self.payload = payload
    def raise_for_status(self): pass
    def json(self): return self.payload

class FakeSession:
    def __init__(self): self.calls = []
    def get(self, url, params, timeout):
        self.calls.append(params.copy())
        if params["skip"] == 0:
            return FakeResponse({"carts": [{"id": 1}, {"id": 2}], "total": 3})
        return FakeResponse({"carts": [{"id": 3}], "total": 3})

def test_pagination():
    session = FakeSession()
    assert len(extract_carts("https://example.test/carts", page_size=2, session=session)) == 3
    assert [call["skip"] for call in session.calls] == [0, 2]

def test_bad_payload():
    class BadSession:
        def get(self, *args, **kwargs): return FakeResponse({"unexpected": []})
    with pytest.raises(ValueError, match="Unexpected API"):
        extract_carts("https://example.test", session=BadSession())
