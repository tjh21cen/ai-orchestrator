from src.ui.pnl_normalize import normalize_pnl, normalize_from_mapping

def test_normalize_pnl_basic():
    out = normalize_pnl(1, 2, [{"id": 1}])
    assert set(out.keys()) == {"uPnL", "dPnL", "trades"}
    assert isinstance(out["uPnL"], (int, float))
    assert isinstance(out["dPnL"], (int, float))
    assert isinstance(out["trades"], list)

def test_normalize_pnl_defaults_and_coercion():
    out = normalize_pnl(None, "3.5", None)
    assert out["uPnL"] == 0.0
    assert out["dPnL"] == 3.5
    assert out["trades"] == []

def test_normalize_from_mapping_handles_obj_like():
    class Obj:
        uPnL = "1.25"
        dPnL = None
        trades = [{"id": 7}]
    out = normalize_from_mapping(Obj())
    assert out["uPnL"] == 1.25
    assert out["dPnL"] == 0.0
    assert isinstance(out["trades"], list)
