from __future__ import annotations

from typing import Any, Dict, Iterable, Optional, Set, Tuple

import requests

from .types import UserStats
from . import __version__


API_BASE = "https://codeforces.com/api"
DEFAULT_TIMEOUT_SEC = 10
USER_AGENT = f"cf-stats/{__version__} (+https://codeforces.com/apiHelp)"


class CodeforcesApiError(RuntimeError):
    pass


def _get(endpoint: str, params: Optional[Dict[str, Any]] = None) -> Any:
    url = f"{API_BASE}/{endpoint}"
    try:
        resp = requests.get(url, params=params, timeout=DEFAULT_TIMEOUT_SEC, headers={"User-Agent": USER_AGENT})
    except requests.RequestException as exc:
        raise CodeforcesApiError(f"Network error while calling {endpoint}: {exc}") from exc

    if resp.status_code != 200:
        raise CodeforcesApiError(f"HTTP {resp.status_code} from Codeforces for {endpoint}")

    payload = resp.json()
    status = payload.get("status")
    if status != "OK":
        comment = payload.get("comment", "Unknown error")
        raise CodeforcesApiError(f"API error: {comment}")
    return payload.get("result")


def fetch_user_info(handle: str) -> Dict[str, Any]:
    result = _get("user.info", {"handles": handle})
    if not result:
        raise CodeforcesApiError("Empty user.info result")
    return result[0]


def fetch_user_rating_history(handle: str) -> Iterable[Dict[str, Any]]:
    return _get("user.rating", {"handle": handle})


def fetch_user_submissions(handle: str, count: int = 10000) -> Iterable[Dict[str, Any]]:
    params = {"handle": handle, "from": 1, "count": min(count, 10000)}
    return _get("user.status", params)


def _unique_problem_key(problem: Dict[str, Any]) -> Tuple[str, str]:
    contest_id = str(problem.get("contestId", "-"))
    index = str(problem.get("index", problem.get("name", "?")))
    return contest_id, index


def compute_solved_count(submissions: Iterable[Dict[str, Any]]) -> int:
    seen: Set[Tuple[str, str]] = set()
    for sub in submissions:
        if sub.get("verdict") == "OK":
            problem = sub.get("problem") or {}
            seen.add(_unique_problem_key(problem))
    return len(seen)


def fetch_user_stats(handle: str) -> UserStats:
    info = fetch_user_info(handle)
    rating_history = list(fetch_user_rating_history(handle))
    submissions = list(fetch_user_submissions(handle))

    rank = info.get("rank")
    rating = info.get("rating")
    max_rank = info.get("maxRank")
    max_rating = info.get("maxRating")
    contest_count = len(rating_history)
    solved_count = compute_solved_count(submissions)

    return UserStats(
        handle=handle,
        rank=rank,
        rating=rating,
        maxRank=max_rank,
        maxRating=max_rating,
        solvedCount=solved_count,
        contestCount=contest_count,
    )


