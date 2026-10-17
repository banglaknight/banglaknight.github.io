"""Copy the CodaBench leaderboards into data/leaderboard.json (run daily by .github/workflows/leaderboard.yml).

Reads the public leaderboard API of the Development and Test phases, keeps each team's entry
(team name and affiliation from the submission form, Defense Score), sorts by score and writes
data/leaderboard.json with the time of the update. build.py turns that file into the two boards.
Test scores stay hidden on CodaBench until Feb 3, 2027, so the test board stays empty until then.
Standard library only. Exits with an error, and leaves the file unchanged, if CodaBench cannot be read.
"""
import json
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "leaderboard.json"
API = "https://www.codabench.org/api/phases/{}/get_leaderboard/"
PHASES = {"dev": (31037, "dev_score"), "test": (31038, "test_score")}


def fetch(phase_id):
    req = urllib.request.Request(API.format(phase_id), headers={"Accept": "application/json",
                                                                "User-Agent": "banglaknight-leaderboard-sync"})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.load(r)
        except Exception as e:                      # network hiccup or CodaBench busy: wait and retry
            if attempt == 3:
                raise
            print(f"phase {phase_id}: {e}; retrying", file=sys.stderr)
            time.sleep(30 * (attempt + 1))


def entries(board, key):
    out = []
    for s in board.get("submissions", []):
        score = next((float(x["score"]) for x in s.get("scores", []) if x.get("column_key") == key), None)
        if score is None:                           # hidden (test phase before Feb 3) or not scored
            continue
        fs = s.get("fact_sheet_answers") or {}
        out.append({"team": (fs.get("team_name") or s.get("owner") or "").strip()[:80],
                    "affiliation": (fs.get("affiliation") or "").strip()[:120],
                    "score": score})
    return sorted(out, key=lambda e: -e["score"])


def main():
    data = {"updated": datetime.now(timezone.utc).isoformat(timespec="seconds")}
    for name, (phase_id, key) in PHASES.items():
        data[name] = entries(fetch(phase_id), key)
        print(f"{name}: {len(data[name])} teams")
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
