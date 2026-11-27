"""Basic legality checks for the computer difficulty levels."""
import random
import unittest

from ai import LEVELS, choose_move
from rules import Game


class ComputerDifficultyTests(unittest.TestCase):
    def test_five_selectable_levels_produce_legal_opening_moves(self):
        self.assertEqual(set(LEVELS), {1, 2, 3, 4, 5})
        for level in LEVELS:
            with self.subTest(level=level):
                game = Game.new(seed=100 + level)
                game.turn = 1
                before_hand = [card["id"] for card in game.hands[1]]
                card, declaration = choose_move(game, level)
                self.assertIn(card["id"], {item["id"] for item in game.legal_cards(1)})
                self.assertEqual(before_hand, [item["id"] for item in game.hands[1]])
                if declaration:
                    self.assertIn(declaration, {item["suit"] for item in game.hands[1] if item["rank"] == "K"})

    def test_five_levels_produce_legal_responses_to_a_lead(self):
        for level in LEVELS:
            with self.subTest(level=level):
                game = Game.new(seed=200 + level)
                lead = game.hands[0][0]
                game.play(0, lead["id"])
                card, declaration = choose_move(game, level)
                self.assertIn(card["id"], {item["id"] for item in game.legal_cards(1)})
                self.assertIsNone(declaration)


if __name__ == "__main__":
    unittest.main()
