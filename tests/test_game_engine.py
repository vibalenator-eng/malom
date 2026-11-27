import unittest

from game_engine import GameState, InvalidMove


class GameEngineTests(unittest.TestCase):
    def test_placing_three_in_a_row_requires_removal(self):
        game = GameState()
        game.place(0)  # Red
        game.place(3)  # Blue
        game.place(1)  # Red
        game.place(4)  # Blue
        game.place(2)  # Red forms a mill
        self.assertTrue(game.must_remove)
        self.assertEqual(game.turn, 0)

    def test_piece_in_a_mill_can_remove_when_every_piece_is_a_mill(self):
        game = GameState(board=[None] * 24, reserve=[0, 0], turn=0, must_remove=True)
        game.board[3:6] = [1, 1, 1]
        self.assertEqual(game.removable_positions(), [3, 4, 5])

    def test_cannot_move_before_placement_phase_ends(self):
        game = GameState()
        game.board[0] = 0
        with self.assertRaises(InvalidMove):
            game.move(0, 1)


if __name__ == "__main__":
    unittest.main()
