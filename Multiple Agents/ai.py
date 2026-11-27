"""Computer opponent strategies for the húzós snapszer demo."""
from __future__ import annotations

from copy import deepcopy
import random

from rules import CARD_POINTS, RANK_STRENGTH, Game, SUITS, make_deck

LEVELS = {
    1: "Kezdő",
    2: "Könnyű",
    3: "Közepes",
    4: "Nehéz",
    5: "Mester",
}


def _takes(game: Game, card: dict) -> bool:
    lead = game.lead_card
    if lead is None:
        return False
    return (card["suit"] == game.trump and lead["suit"] != game.trump) or (
        card["suit"] == lead["suit"]
        and RANK_STRENGTH[card["rank"]] > RANK_STRENGTH[lead["rank"]]
    )


def _simple_card(game: Game, player: int) -> dict:
    """Level 2: spend a cheap winner, otherwise discard the cheapest card."""
    legal = game.legal_cards(player)
    if game.lead_card:
        winners = [card for card in legal if _takes(game, card)]
        if winners:
            return min(winners, key=lambda card: (CARD_POINTS[card["rank"]], RANK_STRENGTH[card["rank"]]))
        return min(legal, key=lambda card: (CARD_POINTS[card["rank"]], RANK_STRENGTH[card["rank"]]))
    return max(legal, key=lambda card: (CARD_POINTS[card["rank"]], RANK_STRENGTH[card["rank"]]))


def _declarations(game: Game, player: int) -> list[tuple[dict, str | None]]:
    legal_ids = {card["id"] for card in game.legal_cards(player)}
    moves: list[tuple[dict, str | None]] = [(card, None) for card in game.legal_cards(player)]
    if game.lead_card is not None:
        return moves
    hand = game.hands[player]
    for suit in SUITS:
        ranks = {card["rank"] for card in hand if card["suit"] == suit}
        if {"K", "F"}.issubset(ranks):
            for card in hand:
                if card["suit"] == suit and card["rank"] in {"K", "F"} and card["id"] in legal_ids:
                    moves.append((card, suit))
    return moves


def _heuristic_score(game: Game, player: int, card: dict, declare: str | None) -> float:
    points = CARD_POINTS[card["rank"]]
    if game.lead_card:
        wins = _takes(game, card)
        trick_value = points + CARD_POINTS[game.lead_card["rank"]]
        return (9.0 + trick_value * 0.75 - points * 0.35) if wins else -points * 1.1
    score = RANK_STRENGTH[card["rank"]] * 1.25 - points * 0.38
    if card["suit"] == game.trump:
        score -= 1.5  # Preserve trump while the talon is open.
    if declare:
        score += (15 if declare == game.trump else 8)
    return score


def _hand_value(game: Game, player: int) -> float:
    value = 0.0
    for card in game.hands[player]:
        value += {"A": 2.3, "10": 1.65, "K": 0.9, "F": 0.45, "Alo": 0.15}[card["rank"]]
        if card["suit"] == game.trump:
            value += 0.55
    return value


def _sample_outcome(game: Game, player: int, move: tuple[dict, str | None]) -> float:
    """Deal unseen cards randomly, then score this move through the current trick.

    The opponent's real hand and the real talon order are deliberately replaced
    with a random legal unseen assignment. This keeps search levels from peeking.
    """
    other = 1 - player
    unseen_ids = set(game.played_ids)
    unseen_ids.update(card["id"] for card in game.hands[player])
    if game.trump_card:
        unseen_ids.add(game.trump_card["id"])
    pool = [card for card in make_deck() if card["id"] not in unseen_ids]
    random.shuffle(pool)
    opponent_count = len(game.hands[other])
    stock_count = len(game.stock)
    if len(pool) < opponent_count + stock_count:
        return _heuristic_score(game, player, move[0], move[1])

    sim = deepcopy(game)
    sim.hands[other] = pool[:opponent_count]
    sim.stock = pool[opponent_count:opponent_count + stock_count]
    starting_points = sim.points[:]
    sim.play(player, move[0]["id"], move[1])
    if not sim.finished and sim.turn == other and sim.lead_card:
        reply = _simple_card(sim, other)
        sim.play(other, reply["id"])

    swing = (sim.points[player] - starting_points[player]) - (sim.points[other] - starting_points[other])
    trick_bonus = 3.5 if sim.last_trick_winner == player else (-3.5 if sim.last_trick_winner == other else 0)
    return swing + trick_bonus + 0.28 * (_hand_value(sim, player) - _hand_value(sim, other))


def choose_move(game: Game, difficulty: int) -> tuple[dict, str | None]:
    """Return a legal card and optional marriage declaration for levels 1–5."""
    if difficulty not in LEVELS:
        difficulty = 3
    player = game.turn
    moves = _declarations(game, player)
    if difficulty == 1:
        return random.choice(moves[:len(game.legal_cards(player))])
    if difficulty == 2:
        card = _simple_card(game, player)
        if game.lead_card is None:
            marriage = next((suit for suit in SUITS if any(c["suit"] == suit and c["rank"] == "K" for c in game.hands[player]) and any(c["suit"] == suit and c["rank"] == "F" for c in game.hands[player])), None)
            if marriage:
                card = next(c for c in game.hands[player] if c["suit"] == marriage and c["rank"] in {"K", "F"})
                return card, marriage
        return card, None
    if difficulty == 3:
        return max(moves, key=lambda move: _heuristic_score(game, player, *move))

    # Search more hidden-card distributions at higher levels. Level 4 samples
    # 24 plausible deals; level 5 samples 96 for a steadier decision.
    sample_count = 24 if difficulty == 4 else 96
    best_move = moves[0]
    best_score = float("-inf")
    for move in moves:
        total = sum(_sample_outcome(game, player, move) for _ in range(sample_count))
        score = total / sample_count + 0.12 * _heuristic_score(game, player, *move)
        if score > best_score:
            best_move, best_score = move, score
    return best_move


def observation(game: Game, player: int) -> dict:
    """Compact, privacy-safe features recorded for future offline learning."""
    return {
        "hand": sorted(card["id"] for card in game.hands[player]),
        "lead": game.lead_card["id"] if game.lead_card else None,
        "trump": game.trump,
        "talon": len(game.stock) + (1 if game.trump_card else 0),
        "talon_open": game.talon_open,
        "seen": list(game.played_ids),
        "score": [game.points[player] + (game.meld_points[player] if game.won_trick[player] else 0),
                  game.points[1 - player] + (game.meld_points[1 - player] if game.won_trick[1 - player] else 0)],
        "tricks": list(game.tricks),
        "legal": sorted(card["id"] for card in game.legal_cards(player)),
    }
