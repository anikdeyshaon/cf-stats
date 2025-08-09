from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any, Dict, Optional

from platformdirs import user_cache_dir

APP_NAME = "cf-stats"
APP_AUTHOR = "cf-stats"


def _cache_dir() -> Path:
    return Path(user_cache_dir(APP_NAME, APP_AUTHOR))


def _cache_path_for_handle(handle: str) -> Path:
    cache_dir = _cache_dir()
    cache_dir.mkdir(parents=True, exist_ok=True)
    safe = handle.lower().strip().replace("/", "_")
    return cache_dir / f"{safe}.json"


def read_cached_stats(handle: str, ttl_seconds: int) -> Optional[Dict[str, Any]]:
    path = _cache_path_for_handle(handle)
    if not path.exists():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None

    fetched_at = payload.get("fetched_at")
    data = payload.get("data")
    if not isinstance(fetched_at, (int, float)) or data is None:
        return None
    if (time.time() - float(fetched_at)) > ttl_seconds:
        return None
    return data


def write_cached_stats(handle: str, data: Dict[str, Any]) -> None:
    path = _cache_path_for_handle(handle)
    payload = {"fetched_at": time.time(), "data": data}
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


