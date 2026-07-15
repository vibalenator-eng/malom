"""The rules for a small, teachable Nine Men's Morris (Malom) game.

This module deliberately contains no Flask or browser code.  Keeping rules
separate makes them easy to test, reuse, and understand.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

Player = Literal[0, 1]  # 0 is red; 1 is blue.

# Board locations are numbered from top-left to bottom-right in the UI.
MILLS = (
    (0, 1, 2), (3, 4, 5), (6, 7, 8), (9, 10, 11),
    (12, 13, 14), (15, 16, 17), (18, 19, 20), (21, 22, 23),
    (0, 9, 21), (3, 10, 18), (6, 11, 15), (1, 4, 7),
    (16, 19, 22), (8, 12, 17), (5, 13, 20), (2, 14, 23),
)

ADJACENT = {
    0: (1, 9), 1: (0, 2, 4), 2: (1, 14), 3: (4, 10),
    4: (1, 3, 5, 7), 5: (4, 13), 6: (7, 11), 7: (4, 6, 8),
    8: (7, 12), 9: (0, 10, 21), 10: (3, 9, 11, 18),
    11: (6, 10, 15), 12: (8, 13, 17), 13: (5, 12, 14, 20),
    14: (2, 13, 23), 15: (11, 16), 16: (15, 17, 19),
    17: (12, 16), 18: (10, 19), 19: (16, 18, 20, 22),
    20: (13, 19), 21: (9, 22), 22: (19, 21, 23), 23: (14, 22),
}


class InvalidMove(ValueError):
    """Raised when a client asks the engine to perform an illegal action."""


@dataclass
class GameState:
    """All information needed to play one game.

    ``board`` contains ``None`` for an empty position, 0 for red, and 1 for
    blue. A player with exactly three pieces may fly to any empty location.
    """

    board: list[int | None] = field(default_factory=lambda: [None] * 24)
    reserve: list[int] = field(default_factory=lambda: [9, 9])
    turn: Player = 0
    must_remove: bool = False
    winner: Player | None = None
    move_count: int = 0

    def opponent(self, player: Player | None = None) -> Player:
        return 1 - (self.turn if player is None else player)  # type: ignore[return-value]

    def pieces_on_board(self, player: Player) -> int:
        return sum(piece == player for piece in self.board)

    def total_pieces(self, player: Player) -> int:
        return self.pieces_on_board(player) + self.reserve[player]

    def is_mill(self, position: int, player: Player) -> bool:
        """Return True when ``position`` is part of a three-piece mill."""
        return any(
            position in line and all(self.board[index] == player for index in line)
            for line in MILLS
        )

    def removable_positions(self) -> list[int]:
        """Prefer opponent pieces outside mills; use mill pieces if necessary."""
        opponent = self.opponent()
        pieces = [index for index, piece in enumerate(self.board) if piece == opponent]
        outside_mills = [index for index in pieces if not self.is_mill(index, opponent)]
        return outside_mills or pieces

    def legal_targets(self, source: int) -> list[int]:
        """Return destinations for one already-placed piece."""
        if self.board[source] != self.turn:
            return []
        empty = [index for index, piece in enumerate(self.board) if piece is None]
        if self.pieces_on_board(self.turn) == 3:
            return empty  # Flying rule.
        return [index for index in ADJACENT[source] if self.board[index] is None]

    def has_mobility(self, player: Player) -> bool:
        if self.reserve[player]:
            return any(piece is None for piece in self.board)
        return any(
            self.board[index] == player and self.legal_targets_for(index, player)
            for index in range(24)
        )

    def legal_targets_for(self, source: int, player: Player) -> list[int]:
        """Like ``legal_targets`` but usable while checking either player."""
        if self.board[source] != player:
            return []
        empty = [index for index, piece in enumerate(self.board) if piece is None]
        if self.pieces_on_board(player) == 3:
            return empty
        return [index for index in ADJACENT[source] if self.board[index] is None]

    def place(self, destination: int) -> None:
        self._check_position(destination)
        if self.must_remove or self.reserve[self.turn] == 0 or self.board[destination] is not None:
            raise InvalidMove("You cannot place a piece there.")
        self.board[destination] = self.turn
        self.reserve[self.turn] -= 1
        self._after_piece_arrives(destination)

    def move(self, source: int, destination: int) -> None:
        self._check_position(source)
        self._check_position(destination)
        if self.must_remove or self.reserve[self.turn] > 0:
            raise InvalidMove("Finish placing pieces before moving.")
        if destination not in self.legal_targets(source):
            raise InvalidMove("That move is not allowed.")
        self.board[source] = None
        self.board[destination] = self.turn
        self._after_piece_arrives(destination)

    def remove(self, position: int) -> None:
        self._check_position(position)
        if not self.must_remove or position not in self.removable_positions():
            raise InvalidMove("That opponent piece cannot be removed.")
        self.board[position] = None
        self.must_remove = False
        self._end_turn()

    def _after_piece_arrives(self, destination: int) -> None:
        self.move_count += 1
        if self.is_mill(destination, self.turn):
            self.must_remove = True
        else:
            self._end_turn()

    def _end_turn(self) -> None:
        next_player = self.opponent()
        # A player loses only after all nine pieces have entered play.
        if self.reserve[next_player] == 0 and (
            self.pieces_on_board(next_player) < 3 or not self.has_mobility(next_player)
        ):
            self.winner = self.turn
            return
        self.turn = next_player

    @staticmethod
    def _check_position(position: int) -> None:
        if not 0 <= position < 24:
            raise InvalidMove("Board position must be between 0 and 23.")

    def as_dict(self) -> dict[str, object]:
        """Convert internal Python data to browser-friendly JSON data."""
        return {
            "board": self.board,
            "reserve": self.reserve,
            "turn": self.turn,
            "must_remove": self.must_remove,
            "removable": self.removable_positions() if self.must_remove else [],
            "winner": self.winner,
            "move_count": self.move_count,
        }
