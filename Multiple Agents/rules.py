"""Rules and authoritative game state for the two-player draw-pile Snapszer demo."""
from __future__ import annotations

from dataclasses import dataclass, field
import random

SUITS = ("piros", "tok", "zold", "makk")
SUIT_LABELS = {"piros": "Piros", "tok": "Tök", "zold": "Zöld", "makk": "Makk"}
RANKS = ("A", "10", "K", "F", "Alo")
RANK_LABELS = {"A": "Ász", "10": "Tízes", "K": "Király", "F": "Felső", "Alo": "Alsó"}
RANK_STRENGTH = {"A": 5, "10": 4, "K": 3, "F": 2, "Alo": 1}
CARD_POINTS = {"A": 11, "10": 10, "K": 4, "F": 3, "Alo": 2}


def card_id(card: dict) -> str:
    return f"{card['suit']}.{card['rank']}"


def make_deck() -> list[dict]:
    return [{"suit": s, "rank": r, "id": f"{s}.{r}"} for s in SUITS for r in RANKS]


@dataclass
class Game:
    hands: list[list[dict]]
    stock: list[dict]
    trump_card: dict | None
    trump: str
    turn: int = 0
    lead_card: dict | None = None
    lead_player: int | None = None
    last_trick: list[dict] | None = None
    points: list[int] | None = None
    meld_points: list[int] | None = None
    won_trick: list[bool] | None = None
    tricks: list[int] | None = None
    closed_by: int | None = None
    finished: bool = False
    winner: int | None = None
    end_reason: str = ""
    last_trick_winner: int | None = None
    message: str = ""
    played_ids: list[str] = field(default_factory=list)

    @classmethod
    def new(cls, seed: int | None = None) -> "Game":
        deck = make_deck()
        random.Random(seed).shuffle(deck)
        # Five cards each, one face-up trump, then nine hidden cards.
        hands = [deck[:5], deck[5:10]]
        trump_card = deck[10]
        return cls(hands, deck[11:], trump_card, trump_card["suit"], points=[0, 0],
                   meld_points=[0, 0], won_trick=[False, False], tricks=[0, 0], last_trick=[],
                   message="Piros kezd. Sok sikert!")

    @property
    def talon_open(self) -> bool:
        return self.closed_by is None and (bool(self.stock) or self.trump_card is not None)

    def legal_cards(self, player: int) -> list[dict]:
        hand = self.hands[player]
        if self.talon_open:
            return hand[:]
        if self.lead_card is None:
            return hand[:]
        same = [c for c in hand if c["suit"] == self.lead_card["suit"]]
        higher = [c for c in same if RANK_STRENGTH[c["rank"]] > RANK_STRENGTH[self.lead_card["rank"]]]
        if higher:
            return higher
        if same:
            return same
        trumps = [c for c in hand if c["suit"] == self.trump]
        return trumps or hand[:]

    def play(self, player: int, identifier: str, declare_suit: str | None = None) -> None:
        if self.finished:
            raise ValueError("A leosztás már véget ért.")
        if player != self.turn:
            raise ValueError("Most nem te következel.")
        legal = self.legal_cards(player)
        card = next((c for c in legal if c["id"] == identifier), None)
        if card is None:
            raise ValueError("Ez a lap most nem játszható ki.")
        if declare_suit:
            if self.lead_card is not None or declare_suit not in SUITS:
                raise ValueError("Bemondani csak híváskor lehet.")
            pair = {c["rank"] for c in self.hands[player] if c["suit"] == declare_suit}
            if not {"K", "F"}.issubset(pair):
                raise ValueError("Ehhez a bemondáshoz Király és Felső kell.")
            if card["suit"] != declare_suit or card["rank"] not in {"K", "F"}:
                raise ValueError("A bemondott pár Királyát vagy Felsőjét kell kijátszani.")
            meld = 40 if declare_suit == self.trump else 20
            self.meld_points[player] += meld
            self.message = f"{meld} bemondás!"
            if self.won_trick[player]:
                self.points[player] += meld
                self.meld_points[player] -= meld
                if self.points[player] >= 66:
                    self._finish(player, "bemondással elérte a 66 pontot")
                    return
        elif declare_suit is not None:
            raise ValueError("Érvénytelen bemondás.")

        self.played_ids.append(card["id"])
        self.hands[player].remove(card)
        if self.lead_card is None:
            self.last_trick = []
            self.lead_card = card
            self.lead_player = player
            self.turn = 1 - player
            return

        first, second = self.lead_card, card
        self.last_trick = [first, card]
        lead_player = self.lead_player
        if second["suit"] == first["suit"]:
            trick_winner = player if RANK_STRENGTH[second["rank"]] > RANK_STRENGTH[first["rank"]] else lead_player
        elif second["suit"] == self.trump:
            trick_winner = player
        else:
            trick_winner = lead_player
        self.points[trick_winner] += CARD_POINTS[first["rank"]] + CARD_POINTS[second["rank"]]
        self.won_trick[trick_winner] = True
        self.tricks[trick_winner] += 1
        self.last_trick_winner = trick_winner
        self.message = f"{('Piros' if trick_winner == 0 else 'Kék')} vitte az ütést."
        if self.meld_points[trick_winner]:
            self.points[trick_winner] += self.meld_points[trick_winner]
            self.meld_points[trick_winner] = 0
        self.lead_card = None
        self.lead_player = None

        if self.points[trick_winner] >= 66:
            self._finish(trick_winner, "elérte a 66 pontot")
            return
        if not self.hands[0] and not self.hands[1]:
            if self.closed_by is None:
                self._finish(trick_winner, "az utolsó ütést vitte")
            else:
                winner = self.closed_by if self.points[self.closed_by] >= 66 else 1 - self.closed_by
                self._finish(winner, "takarás után elérte a 66 pontot" if winner == self.closed_by else "a takaró nem érte el a 66 pontot")
            return
        self._draw(trick_winner)
        self._draw(1 - trick_winner)
        self.turn = trick_winner

    def _draw(self, player: int) -> None:
        if self.closed_by is not None:
            return
        if self.stock:
            self.hands[player].append(self.stock.pop(0))
        elif self.trump_card is not None:
            self.hands[player].append(self.trump_card)
            self.trump_card = None

    def close_talon(self, player: int) -> None:
        if self.finished or player != self.turn or self.lead_card is not None:
            raise ValueError("A talont csak híváskor lehet betakarni.")
        if self.closed_by is not None or len(self.stock) < 2 or not any(self.tricks):
            raise ValueError("Betakarni az első ütés után, legalább két húzólapnál lehet.")
        self.closed_by = player
        self.message = "A talon betakarva. Most már szín- és ütéskényszer van."

    def exchange_trump(self, player: int) -> None:
        if self.finished or player != self.turn or self.lead_card is not None or not self.talon_open or self.trump_card is None:
            raise ValueError("Most nem lehet adut cserélni.")
        jack = next((c for c in self.hands[player] if c["suit"] == self.trump and c["rank"] == "Alo"), None)
        if jack is None:
            raise ValueError("Nincs nálad adu Alsó.")
        self.hands[player].remove(jack)
        self.hands[player].append(self.trump_card)
        self.trump_card = jack
        self.message = "Kicserélted az adu Alsót."

    def _finish(self, winner: int, reason: str) -> None:
        self.finished = True
        self.winner = winner
        self.end_reason = reason

    def view(self, player: int, token: str, code: str, mode: str, names: list[str]) -> dict:
        can_close = not self.finished and player == self.turn and self.lead_card is None and self.closed_by is None and len(self.stock) >= 2 and any(self.tricks)
        if self.finished:
            close_reason = "A leosztás már véget ért."
        elif player != self.turn:
            close_reason = "Csak a te körödben teheted."
        elif self.lead_card is not None:
            close_reason = "Csak híváskor, az első lap kijátszása előtt takarhatsz."
        elif self.closed_by is not None:
            close_reason = "A talon már be van takarva."
        elif not any(self.tricks):
            close_reason = "A takarás csak legalább egy lejátszott ütés után engedélyezett."
        elif len(self.stock) < 2:
            close_reason = "Legalább két lefordított lap maradjon a felfordított adu fölött."
        else:
            close_reason = ""

        has_trump_lower = any(c["suit"] == self.trump and c["rank"] == "Alo" for c in self.hands[player])
        can_exchange = not self.finished and player == self.turn and self.lead_card is None and self.talon_open and self.trump_card is not None and has_trump_lower
        if self.finished:
            exchange_reason = "A leosztás már véget ért."
        elif player != self.turn:
            exchange_reason = "Csak a te körödben cserélhetsz adut."
        elif self.lead_card is not None:
            exchange_reason = "Aducsere csak híváskor, az első lap kijátszása előtt lehetséges."
        elif self.closed_by is not None:
            exchange_reason = "A talon már be van takarva."
        elif self.trump_card is None:
            exchange_reason = "A felfordított adut már felhúzták."
        elif not self.talon_open:
            exchange_reason = "A talon már nem nyitott."
        elif not has_trump_lower:
            exchange_reason = "A kezedben nincs adu Alsó."
        else:
            exchange_reason = ""

        marriages = []
        if not self.finished and player == self.turn and self.lead_card is None:
            for suit in SUITS:
                pair = [c for c in self.hands[player] if c["suit"] == suit and c["rank"] in {"K", "F"}]
                if len(pair) == 2:
                    marriages.append({"suit": suit, "points": 40 if suit == self.trump else 20,
                                      "cards": [{"id": c["id"], "rank": c["rank"]} for c in pair
                                                if c["id"] in {legal["id"] for legal in self.legal_cards(player)}]})
        return {
            "code": code, "mode": mode, "player": player, "names": names,
            "hand": self.hands[player], "hand_counts": [len(self.hands[0]), len(self.hands[1])],
            "legal_ids": [c["id"] for c in self.legal_cards(player)] if not self.finished else [],
            "turn": self.turn, "lead_card": self.lead_card, "lead_player": self.lead_player,
            "last_trick": self.last_trick,
            "trump": self.trump, "trump_card": self.trump_card,
            "stock_count": len(self.stock), "talon_open": self.talon_open,
            "closed_by": self.closed_by, "points": [self.points[i] + (self.meld_points[i] if self.won_trick[i] else 0) for i in range(2)],
            "tricks": self.tricks, "finished": self.finished, "winner": self.winner,
            "end_reason": self.end_reason, "message": self.message,
            "can_close": can_close, "close_reason": close_reason,
            "can_exchange": can_exchange, "exchange_reason": exchange_reason,
            "marriages": marriages,
        }
