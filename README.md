## cf-stats — Codeforces Personal Quick Stats CLI

Get a quick snapshot of a Codeforces user's stats from your terminal.

### Features
- Shows current rating, max rating, rank, solved problem count, and contest count
- Beautiful output using `rich`
- Optional JSON output with `--json`
- Local caching with configurable TTL (default 10 minutes)

### Run directly from source (no installer)

You can clone the repo and run the CLI without installing anything system-wide.

```bash
# 1) Clone the repository
git clone https://github.com/anikdeyshaon/cf-stats.git
cd cf-stats

# 2) Run the CLI module directly
# Windows (PowerShell):
py -m cfstats <handle>
# macOS/Linux:
python3 -m cfstats <handle>
```

### Usage

```bash
cf-stats <handle>
```

Examples:

```bash
# Pretty table
python -m cfstats _Comfortably_Numb__

# JSON output
python -m cfstats _Comfortably_Numb__ --json

# Disable cache
python -m cfstats _Comfortably_Numb__ --no-cache

# Set cache TTL to 30 minutes
python -m cfstats _Comfortably_Numb__ --ttl 30
```

Note: This project requires Python 3.9+ and the dependencies listed in `pyproject.toml` (`requests`, `rich`, `platformdirs`). If you are missing them, install using your preferred method or environment manager.

### Output

Table example:

```
┏━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━┓
┃ Handle               ┃ Rank  ┃ Rating  ┃ Max Rating ┃ Solved ┃ Contests ┃
┡━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━┩
│ _Comfortably_Numb__  │ expert│ 1700    │ 1800       │ 1234   │ 57       │
└──────────────────────┴───────┴─────────┴────────────┴────────┴──────────┘
```

JSON example:

```json
{
  "handle": "_Comfortably_Numb__",
  "rank": "expert",
  "rating": 1700,
  "maxRank": "candidate master",
  "maxRating": 1900,
  "solvedCount": 1234,
  "contestCount": 57
}
```

### Configuration

- `--ttl <minutes>`: cache time-to-live in minutes (default: 10)
- `--json`: print raw JSON instead of a table
- `--no-cache`: bypass cache and fetch fresh data

### Notes

- Data is fetched from the free Codeforces API (`https://codeforces.com/api`).
- Solved count is computed as the number of unique problems with accepted submissions.
- Contest count is the number of contests in the user's rating history.

### License

MIT


