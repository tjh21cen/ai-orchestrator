from __future__ import annotations
from typing import Any, Dict, List, Mapping, Optional


def normalize_pnl(u: Any = None, d: Any = None, trades: Optional[Any] = None) -> Dict[str, Any]:
    """
    Return a stable PnL schema:
        { "uPnL": float, "dPnL": float, "trades": list }
    - Coerces u/d to float (defaults 0.0 on None/invalid)
    - Ensures trades is a list ([] on None / falsy)
    """

    # robust float conversion
    def _f(x: Any) -> float:
        try:
            return float(x)
        except Exception:
            return 0.0

    # normalize trades into a list
    if trades is None:
        trades_list: List[Any] = []
    elif isinstance(trades, list):
        trades_list = trades
    elif isinstance(trades, (tuple, set)):
        trades_list = list(trades)
    else:
        # if a single object sneaks in, wrap it
        trades_list = [trades]

    return {"uPnL": _f(u), "dPnL": _f(d), "trades": trades_list}


def normalize_from_mapping(raw: Any) -> Dict[str, Any]:
    """
    Convenience: accept a dict/obj that *might* have uPnL/dPnL/trades in various shapes.
    Falls back to zeros/[] when absent.
    """
    u = None
    d = None
    t = None
    if isinstance(raw, Mapping):
        u = raw.get("uPnL")
        d = raw.get("dPnL")
        t = raw.get("trades")
    else:
        u = getattr(raw, "uPnL", None)
        d = getattr(raw, "dPnL", None)
        t = getattr(raw, "trades", None)
    return normalize_pnl(u, d, t)
