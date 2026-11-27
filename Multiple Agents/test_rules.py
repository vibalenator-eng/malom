"""Focused rule checks for the húzós snapszer prototype."""
import unittest

from rules import Game, make_deck


def c(suit, rank):
    return next(card for card in make_deck() if card["suit"] == suit and card["rank"] == rank)


def game(hands, stock=None, trump_card=None, trump="makk", **kwargs):
    return Game(hands=hands, stock=stock or [], trump_card=trump_card, trump=trump,
                points=[0, 0], meld_points=[0, 0], won_trick=[False, False], tricks=[0, 0],
                last_trick=[], **kwargs)


class SnapszerRulesTests(unittest.TestCase):
    def test_deck_and_initial_deal(self):
        self.assertEqual(len(make_deck()), 20)
        self.assertEqual(len({card["id"] for card in make_deck()}), 20)
        match = Game.new(seed=5)
        self.assertEqual([len(hand) for hand in match.hands], [5, 5])
        self.assertEqual(len(match.stock), 9)
        self.assertIsNotNone(match.trump_card)

    def test_talon_open_allows_any_card_and_winner_draws_first(self):
        stock_a, stock_b = c("zold", "A"), c("tok", "A")
        match = game([[c("piros", "A"), c("piros", "K")], [c("makk", "A"), c("zold", "K")]], [stock_a, stock_b], c("tok", "10"), "tok")
        match.play(0, "piros.A")
        match.play(1, "makk.A")
        self.assertEqual(match.turn, 0)
        self.assertEqual(match.hands[0][-1]["id"], stock_a["id"])
        self.assertEqual(match.hands[1][-1]["id"], stock_b["id"])
        self.assertEqual(match.points[0], 22)

    def test_each_trick_winner_gets_both_played_cards_points(self):
        match = game([[c("piros", "A"), c("tok", "10")],
                      [c("makk", "A"), c("tok", "K")]], trump="makk")
        # The trumping player scores both their own trump and the lead card.
        match.play(0, "piros.A")
        match.play(1, "makk.A")
        self.assertEqual(match.points, [0, 22])
        # On the next trick, the player who wins by rank scores both cards.
        match.play(1, "tok.K")
        match.play(0, "tok.10")
        self.assertEqual(match.points, [14, 22])

    def test_closed_talon_requires_follow_and_beat_when_possible(self):
        match = game([[c("piros", "A")], [c("piros", "K"), c("piros", "10"), c("makk", "A")]], trump="makk", closed_by=0)
        match.lead_card = c("piros", "K")
        match.lead_player = 0
        self.assertEqual([x["rank"] for x in match.legal_cards(1)], ["10"])

    def test_closed_talon_requires_trump_if_void(self):
        match = game([[c("piros", "A")], [c("tok", "K"), c("makk", "A")]], trump="makk", closed_by=0)
        match.lead_card = c("piros", "K")
        match.lead_player = 0
        self.assertEqual([x["id"] for x in match.legal_cards(1)], ["makk.A"])

    def test_meld_is_credited_only_after_owner_wins_a_trick(self):
        match = game([[c("piros", "K"), c("piros", "F"), c("zold", "A")],
                      [c("makk", "A"), c("tok", "A"), c("zold", "K"), c("zold", "10")]],
                     stock=[c("tok", "10"), c("tok", "K"), c("zold", "10")], trump="makk")
        match.play(0, "piros.K", "piros")
        self.assertEqual(match.points[0], 0)
        self.assertEqual(match.meld_points[0], 20)
        match.play(1, "makk.A")
        self.assertEqual(match.points[1], 15)
        self.assertEqual(match.meld_points[0], 20)
        # Player one leads a green ten; player zero beats it with the green ace.
        match.play(1, "zold.10")
        match.play(0, "zold.A")
        self.assertTrue(match.won_trick[0])
        self.assertEqual(match.meld_points[0], 0)
        self.assertGreaterEqual(match.points[0], 41)

    def test_view_only_includes_requesting_players_hand(self):
        match = Game.new(seed=3)
        view = match.view(0, "", "ABCD", "online", ["Piros", "Kék"])
        self.assertEqual(view["hand"], match.hands[0])
        self.assertNotIn("hands", view)
        self.assertNotIn(match.hands[1][0]["id"], view["legal_ids"])

    def test_view_gives_close_and_exchange_reasons(self):
        match = game([[c("piros", "A")], [c("makk", "A")]], stock=[c("tok", "A")],
                     trump_card=c("zold", "10"), trump="zold")
        view = match.view(0, "", "ABCD", "online", ["Piros", "Kék"])
        self.assertFalse(view["can_close"])
        self.assertIn("lejátszott", view["close_reason"])
        self.assertFalse(view["can_exchange"])
        self.assertIn("adu Alsó", view["exchange_reason"])

        match.tricks[0] = 1
        view = match.view(0, "", "ABCD", "online", ["Piros", "Kék"])
        self.assertIn("két lefordított", view["close_reason"])

    def test_view_allows_cover_on_lead_after_a_trick_with_two_hidden_cards(self):
        match = game([[c("piros", "A")], [c("makk", "A")]],
                     stock=[c("tok", "A"), c("zold", "10")],
                     trump_card=c("tok", "K"), trump="tok", turn=0)
        match.tricks[0] = 1
        view = match.view(0, "", "ABCD", "ai", ["Piros", "Számítógép"])
        self.assertTrue(view["can_close"])
        self.assertEqual(view["close_reason"], "")

    def test_view_offers_both_marriage_cards_only_on_own_lead(self):
        match = game([[c("piros", "K"), c("piros", "F")], [c("makk", "A")]],
                     stock=[c("tok", "A")], trump="tok")
        view = match.view(0, "", "ABCD", "online", ["Piros", "Kék"])
        self.assertEqual(len(view["marriages"]), 1)
        marriage = view["marriages"][0]
        self.assertEqual(marriage["points"], 20)
        self.assertEqual({c["rank"] for c in marriage["cards"]}, {"K", "F"})
        self.assertTrue(all(card["id"] in view["legal_ids"] for card in marriage["cards"]))
        self.assertEqual(match.view(1, "", "ABCD", "online", ["Piros", "Kék"])["marriages"], [])

        match.lead_card = c("tok", "K")
        match.lead_player = 0
        self.assertEqual(match.view(0, "", "ABCD", "online", ["Piros", "Kék"])["marriages"], [])

    def test_marriage_options_remain_available_after_talon_cover(self):
        match = game([[c("piros", "K"), c("piros", "F")], [c("makk", "A")]],
                     trump="piros", closed_by=0)
        view = match.view(0, "", "ABCD", "online", ["Piros", "Kék"])
        self.assertEqual(view["marriages"][0]["points"], 40)

    def test_declared_marriage_must_be_one_of_its_two_cards(self):
        match = game([[c("piros", "K"), c("piros", "F"), c("zold", "A")],
                      [c("makk", "A")]], trump="tok")
        with self.assertRaises(ValueError):
            match.play(0, "zold.A", "piros")

    def test_closed_talon_fails_for_closer_who_does_not_reach_66(self):
        match = game([[c("piros", "A")], [c("makk", "A")]], trump="makk", closed_by=0)
        match.play(0, "piros.A")
        match.play(1, "makk.A")
        self.assertTrue(match.finished)
        self.assertEqual(match.winner, 1)

    def test_closed_talon_stops_drawing(self):
        match = game([[c("piros", "A"), c("zold", "K")],
                      [c("makk", "A"), c("tok", "K")]],
                     stock=[c("zold", "A")], trump="makk", closed_by=0)
        match.play(0, "piros.A")
        match.play(1, "makk.A")
        self.assertEqual(len(match.stock), 1)
        self.assertEqual([len(hand) for hand in match.hands], [1, 1])


if __name__ == "__main__":
    unittest.main()
