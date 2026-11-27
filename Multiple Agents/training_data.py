"""Bounded JSONL archive of completed human-versus-computer games."""
from __future__ import annotations

from datetime import datetime, timezone
import json
import os
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent / "data" / "ai_training_games.jsonl"
try:
    MAX_GAMES = int(os.environ.get("SNAPSZER_MAX_TRAINING_GAMES", "1000"))
except ValueError:
    MAX_GAMES = 1000
if MAX_GAMES not in {1000, 10000}:
    MAX_GAMES = 1000


def _count_lines() -> int:
    if not DATA_FILE.exists():
        return 0
    try:
        with DATA_FILE.open("r", encoding="utf-8") as archive:
            return sum(1 for line in archive if line.strip())
    except OSError:
        return 0


def stats() -> dict:
    return {"saved_games": _count_lines(), "capacity": MAX_GAMES, "format": "JSONL"}


def save_game(record: dict) -> int:
    """Append one completed game, retaining only the newest MAX_GAMES records."""
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(record, ensure_ascii=False, separators=(",", ":"))
    count = _count_lines()
    if count < MAX_GAMES:
        with DATA_FILE.open("a", encoding="utf-8", newline="\n") as archive:
            archive.write(line + "\n")
        return count + 1

    existing = [item for item in DATA_FILE.read_text(encoding="utf-8").splitlines() if item.strip()]
    kept = existing[-(MAX_GAMES - 1):] if MAX_GAMES > 1 else []
    temp = DATA_FILE.with_suffix(DATA_FILE.suffix + ".tmp")
    temp.write_text("\n".join([*kept, line]) + "\n", encoding="utf-8")
    temp.replace(DATA_FILE)
    return min(count + 1, MAX_GAMES)


def make_record(difficulty: int, samples: list[dict], winner: int, scores: list[int], end_reason: str) -> dict:
    return {
        "version": 1,
        "finished_at": datetime.now(timezone.utc).isoformat(),
        "difficulty": difficulty,
        "winner": "computer" if winner == 1 else "human",
        "scores": scores,
        "end_reason": end_reason,
        "decisions": [
            {"observation": sample["observation"], "action": sample["action"],
             "reward": 1 if winner == 1 else -1}
            for sample in samples
        ],
    }
