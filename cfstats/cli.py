from __future__ import annotations

import argparse
import json
import sys
from typing import Any, Dict

from rich.console import Console
from rich.table import Table

from . import __version__
from .api import CodeforcesApiError, fetch_user_stats
from .cache import read_cached_stats, write_cached_stats


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="cf-stats",
        description="Codeforces Personal Quick Stats CLI",
    )
    parser.add_argument("handle", help="Codeforces handle, e.g., tourist")
    parser.add_argument("--json", action="store_true", help="Output as JSON instead of a table")
    parser.add_argument("--ttl", type=int, default=10, metavar="MINUTES", help="Cache TTL in minutes (default: 10)")
    parser.add_argument("--no-cache", action="store_true", help="Bypass cache and fetch fresh data")
    parser.add_argument("--version", action="version", version=f"cf-stats {__version__}")
    return parser


def _print_table(console: Console, data: Dict[str, Any]) -> None:
    table = Table(title=f"Codeforces Stats: {data['handle']}")
    table.add_column("Handle")
    table.add_column("Rank")
    table.add_column("Rating")
    table.add_column("Max Rating")
    table.add_column("Solved")
    table.add_column("Contests")

    rank = data.get("rank") or "-"
    rating = data.get("rating")
    rating_str = "-" if rating is None else str(rating)
    max_rating = data.get("maxRating")
    max_rating_str = "-" if max_rating is None else str(max_rating)

    table.add_row(
        data.get("handle", "-"),
        rank,
        rating_str,
        max_rating_str,
        str(data.get("solvedCount", 0)),
        str(data.get("contestCount", 0)),
    )
    console.print(table)


def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    parser = _build_parser()
    args = parser.parse_args(argv)

    console = Console(stderr=False)

    ttl_seconds = max(0, int(args.ttl)) * 60

    data: Dict[str, Any] | None = None
    if not args.no_cache and ttl_seconds > 0:
        data = read_cached_stats(args.handle, ttl_seconds)

    if data is None:
        try:
            data = fetch_user_stats(args.handle)
        except CodeforcesApiError as exc:
            console.print(f"[red]Error:[/red] {exc}")
            return 1
        if not args.no_cache and ttl_seconds > 0:
            try:
                write_cached_stats(args.handle, data)
            except Exception:
                # Cache write failures should not break the CLI
                pass

    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        _print_table(console, data)

    return 0


