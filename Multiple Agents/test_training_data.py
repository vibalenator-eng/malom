"""Checks the JSONL learning archive and its rolling size limit."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import training_data


class TrainingArchiveTests(unittest.TestCase):
    def test_archive_keeps_only_the_newest_games_at_capacity(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as folder:
            archive = Path(folder) / "games.jsonl"
            with patch.object(training_data, "DATA_FILE", archive), patch.object(training_data, "MAX_GAMES", 2):
                training_data.save_game({"number": 1})
                training_data.save_game({"number": 2})
                training_data.save_game({"number": 3})

                records = [json.loads(line) for line in archive.read_text(encoding="utf-8").splitlines()]
                self.assertEqual(records, [{"number": 2}, {"number": 3}])
                self.assertEqual(training_data.stats()["saved_games"], 2)


if __name__ == "__main__":
    unittest.main()
