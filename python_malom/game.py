"""The rules and state of a Malom game.

This module has no Tkinter code.  Keeping rules separate from the interface
makes the game easier to test, reuse, and understand.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

RED, BLUE = 0, 1
PLAYER_NAMES = {RED: "Red", BLUE: "Blue"}

# The 24 board points.  A mill is one row of three point indexes.
MILLS = (
    (0, 1, 2), (3, 4, 5), (6, 7, 8), (9, 10, 11),
    (12, 13, 14), (15, 16, 17), (18, 19, 20), (21, 22, 23),
    (0, 9, 21), (3, 10, 18), (6, 11, 15), (1, 4, 7),
    (16, 19, 22), (8, 12, 17), (5, 13, 20), (2, 14, 23),
)


def make_neighbours() -> tuple[tuple[int, ...], ...]:
    """Build the connections between adjacent points from the mill rows."""
    neighbours = [set() for _ in range(24)]
    for line in MILLS:
        for left, right in zip(line, line[1:]):
            neighbours[left].add(right)
            neighbours[right].add(left)
    return tuple(tuple(sorted(points)) for points in neighbours)


NEIGHBOURS = make_neighbours()


@dataclass
class Game:
    """A mutable game state.

    ``board`` holds ``None``, ``RED``, or ``BLUE`` for each of the 24 points.
    """

    board: list[Optional[int]] = field(default_factory=lambda: [None] * 24)
    reserve: list[int] = field(default_factory=lambda: [9, 9])
    turn: int = RED
    removal_required: bool = False
    no_mill_moves: int = 0
    winner: Optional[int] = None
    draw: bool = False

    def reset(self) -> None:
        self.board = [None] * 24
        self.reserve = [9, 9]
        self.turn = RED
        self.removal_required = False
        self.no_mill_moves = 0
        self.winner = None
        self.draw = False

    def piece_count(self, player: int) -> int:
        return self.board.count(player)

    def total_count(self, player: int) -> int:
        """Pieces on the board plus pieces not placed yet."""
        return self.piece_count(player) + self.reserve[player]

    def forms_mill(self, point: int, player: int) -> bool:
        return any(
            point in line and all(self.board[index] == player for index in line)
            for line in MILLS
        )

    def in_mill(self, point: int) -> bool:
        player = self.board[point]
        return player is not None and self.forms_mill(point, player)

    def legal_targets(self, source: Optional[int] = None) -> list[int]:
        """Return legal destinations for the current player.

        With a reserve piece, ``source`` must be None.  With exactly three
        pieces on the board, every empty point is a legal target (flying).
        """
        if self.reserve[self.turn] > 0:
            return [index for index, piece in enumerate(self.board) if piece is None] if source is None else []
        if source is None or self.board[source] != self.turn:
            return []
        if self.piece_count(self.turn) == 3:
            return [index for index, piece in enumerate(self.board) if piece is None]
        return [index for index in NEIGHBOURS[source] if self.board[index] is None]

    def legal_moves(self, player: Optional[int] = None) -> list[tuple[Optional[int], int]]:
        """List placement/movement pairs for a player (used by the computer)."""
        player = self.turn if player is None else player
        if player != self.turn or self.removal_required:
            return []
        if self.reserve[player]:
            return [(None, target) for target in self.legal_targets()]
        return [
            (source, target)
            for source, piece in enumerate(self.board)
            if piece == player
            for target in self.legal_targets(source)
        ]

    def captures(self) -> list[int]:
        """Return opposing pieces that may be removed after a mill."""
        opponent = 1 - self.turn
        outside_mills = [i for i, piece in enumerate(self.board) if piece == opponent and not self.in_mill(i)]
        return outside_mills or [i for i, piece in enumerate(self.board) if piece == opponent]

    def play(self, source: Optional[int], target: int) -> bool:
        """Make one placement or move.  Returns False if it is illegal."""
        if self.finished or self.removal_required or target not in self.legal_targets(source):
            return False
        if source is None:
            self.board[target] = self.turn
            self.reserve[self.turn] -= 1
        else:
            self.board[source] = None
            self.board[target] = self.turn
        if self.forms_mill(target, self.turn):
            self.removal_required = True
        else:
            self.no_mill_moves += 1
            self._next_turn()
        return True

    def capture(self, point: int) -> bool:
        """Remove an allowed opposing piece, then finish the turn."""
        if not self.removal_required or point not in self.captures():
            return False
        self.board[point] = None
        self.removal_required = False
        self.no_mill_moves = 0
        self._next_turn()
        return True

    @property
    def finished(self) -> bool:
        return self.winner is not None or self.draw

    def _next_turn(self) -> None:
        opponent = 1 - self.turn
        if self.reserve[opponent] == 0 and (self.piece_count(opponent) < 3 or not self.legal_moves_for(opponent)):
            self.winner = self.turn
        elif self.no_mill_moves >= 100:
            self.draw = True
        else:
            self.turn = opponent

    def legal_moves_for(self, player: int) -> list[tuple[Optional[int], int]]:
        """A version of legal_moves that can inspect either player."""
        if self.reserve[player]:
            return [(None, i) for i, piece in enumerate(self.board) if piece is None]
        pieces = [i for i, piece in enumerate(self.board) if piece == player]
        if len(pieces) == 3:
            empty = [i for i, piece in enumerate(self.board) if piece is None]
            return [(source, target) for source in pieces for target in empty]
        return [(source, target) for source in pieces for target in NEIGHBOURS[source] if self.board[target] is None]
