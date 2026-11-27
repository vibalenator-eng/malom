"""A small computer opponent with five deliberately understandable levels."""

from __future__ import annotations

from copy import deepcopy
from random import choice, uniform

from game_engine import GameState


def legal_actions(game: GameState) -> list[dict[str, int | str]]:
    """List every action the player whose turn it is may take."""
    if game.must_remove:
        return [{"kind": "remove", "position": position} for position in game.removable_positions()]
    if game.reserve[game.turn]:
        return [
            {"kind": "place", "destination": position}
            for position, piece in enumerate(game.board) if piece is None
        ]
    return [
        {"kind": "move", "source": source, "destination": destination}
        for source, piece in enumerate(game.board) if piece == game.turn
        for destination in game.legal_targets(source)
    ]


def apply_action(game: GameState, action: dict[str, int | str]) -> None:
    """Apply one action dictionary. This keeps the AI code pleasantly small."""
    if action["kind"] == "place":
        game.place(int(action["destination"]))
    elif action["kind"] == "move":
        game.move(int(action["source"]), int(action["destination"]))
    else:
        game.remove(int(action["position"]))


def score(game: GameState, computer: int = 1) -> float:
    """Score a board from the computer's viewpoint.

    It favours having more pieces and forming mills. The function is simple on
    purpose: learners can tune these weights and observe the AI change.
    """
    human = 1 - computer
    computer_mills = sum(game.is_mill(index, computer) for index in range(24))
    human_mills = sum(game.is_mill(index, human) for index in range(24))
    return (
        (game.total_pieces(computer) - game.total_pieces(human)) * 100
        + (computer_mills - human_mills) * 25
        + len([action for action in legal_actions(game) if action["kind"] != "remove"]) * 2
    )


def choose_action(game: GameState, level: int) -> dict[str, int | str]:
    """Return a legal computer move.

    Level 1 chooses randomly. Higher levels use the same one-move look-ahead,
    but with less randomness; level 5 is therefore the most consistent.
    """
    actions = legal_actions(game)
    if level == 1:
        return choice(actions)

    noise = {2: 120, 3: 55, 4: 20, 5: 0}[level]
    best_action = actions[0]
    best_score = float("-inf")
    for action in actions:
        future = deepcopy(game)
        apply_action(future, action)
        candidate_score = score(future) + uniform(-noise, noise)
        if candidate_score > best_score:
            best_action, best_score = action, candidate_score
    return best_action
