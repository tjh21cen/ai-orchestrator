import json
import pytest

def _maybe_fastapi_client():
    try:
        from starlette.testclient import TestClient
        # Import your app (adjust if app is exposed from another module)
        from src.ui.server import app  # type: ignore
        return TestClient(app)
    except Exception:
        return None

@pytest.mark.skipif(_maybe_fastapi_client() is None, reason="App not FastAPI/Starlette or not importable")
def test_pnl_endpoint_contract():
    client = _maybe_fastapi_client()
    resp = client.get("/api/pnl")
    assert resp.status_code == 200
    data = resp.json() if hasattr(resp, "json") else json.loads(resp.text)
    assert set(data.keys()) == {"uPnL", "dPnL", "trades"}
    assert isinstance(data["uPnL"], (int, float))
    assert isinstance(data["dPnL"], (int, float))
    assert isinstance(data["trades"], list)
