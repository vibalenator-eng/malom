"""A deliberately small, explainable computer player."""

from __future__ import annotations

import random

from .game import BLUE, Game, MILLS


def potential_mills(game: Game, player: int) -> int:
    """Count rows where the player has two pieces and one empty point."""
    return sum(
        sum(game.board[i] == player for i in line) == 2
        and sum(game.board[i] is None for i in line) == 1
        for line in MILLS
    )


def choose_move(game: Game, level: int = 3) -> tuple[int | None, int]:
    """Choose a legal blue move.

    Higher levels use the same readable heuristic with less randomness.  This
    is a good first AI to inspect before replacing it with minimax later.
    """
    moves = game.legal_moves()
    if not moves:
        raise ValueError("No legal moves available")
    if level == 1:
        return random.choice(moves)

    def value(move: tuple[int | None, int]) -> float:
        source, target = move
        copy = Game(board=game.board.copy(), reserve=game.reserve.copy(), turn=game.turn)
        copy.play(source, target)
        score = potential_mills(copy, BLUE) * 20
        score -= potential_mills(copy, 0) * 14
        score += copy.piece_count(BLUE) * 2
        # Tiny variation prevents repeated games from always looking identical.
        return score + random.random() * (6 - level)

    return max(moves, key=value)


def choose_capture(game: Game) -> int:
    """Prefer removing a piece that contributes to many potential mills."""
    choices = game.captures()
    return max(choices, key=lambda point: sum(point in line for line in MILLS))
