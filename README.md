## cf-stats — Codeforces Personal Quick Stats CLI

Get a quick snapshot of a Codeforces user's stats from your terminal.

### Features
- Shows current rating, max rating, rank, solved problem count, and contest count
- Beautiful output using `rich`
- Optional JSON output with `--json`
- Local caching with configurable TTL (default 10 minutes)

### Dependencies

- Python 3.9+ (required for built-in typing like `list[str]`)
- Python packages: `requests`, `rich`, `platformdirs`

### Run directly from source (no installer)

You can clone the repo and run the CLI without installing anything system-wide. Create a virtual environment in the project folder and install the few dependencies locally.

Windows (PowerShell):

```powershell
# 1) Clone the repository
git clone https://github.com/anikdeyshaon/cf-stats.git
cd cf-stats

# 2) Create and activate a virtual environment (local to this folder)
py -m venv .venv
./.venv/Scripts/Activate.ps1

# 3) Install dependencies
py -m pip install --upgrade pip
py -m pip install requests rich platformdirs

# 4) Run the CLI module
py -m cfstats <handle>
```

macOS/Linux:

```bash
# 1) Clone the repository
git clone https://github.com/anikdeyshaon/cf-stats.git
cd cf-stats

# 2) Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 3) Install dependencies
python3 -m pip install --upgrade pip
python3 -m pip install requests rich platformdirs

# 4) Run the CLI module
python3 -m cfstats <handle>
```

### Usage

```bash
cf-stats <handle>
```

Note: The `cf-stats` console script is only available when installed as a package. When running from source as shown above, use `python -m cfstats` (or `py -m cfstats` on Windows).

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

Note: This project requires Python 3.9+ and the following dependencies: `requests`, `rich`, and `platformdirs`. If they are missing, install them with pip as shown above (preferably in a virtual environment).

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


