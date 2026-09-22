import unittest
from fractions import Fraction

from kuhn_poker.env import Card, KuhnPokerState, deal, deal_outcomes


def play_out(state: KuhnPokerState, actions: str) -> KuhnPokerState:
    for a in actions:
        state = state.apply_action(a)
    return state


class TestKuhnPokerEnv(unittest.TestCase):
    def test_deal_is_deterministic_given_seed(self):
        self.assertEqual(deal(seed=42).cards, deal(seed=42).cards)

    def test_deal_uses_two_distinct_cards(self):
        state = deal(seed=1)
        self.assertNotEqual(state.cards[0], state.cards[1])

    def test_current_player_alternates(self):
        state = KuhnPokerState(cards=(Card.KING, Card.JACK))
        self.assertEqual(state.current_player(), 0)
        self.assertEqual(state.apply_action("p").current_player(), 1)

    def test_terminal_histories(self):
        base = KuhnPokerState(cards=(Card.KING, Card.JACK))
        for actions in ("pp", "bp", "bb", "pbp", "pbb"):
            self.assertTrue(play_out(base, actions).is_terminal())
        for actions in ("p", "b", "pb"):
            self.assertFalse(play_out(base, actions).is_terminal())

    def test_utility_zero_sum(self):
        base = KuhnPokerState(cards=(Card.KING, Card.JACK))
        for actions in ("pp", "bp", "bb", "pbp", "pbb"):
            state = play_out(base, actions)
            self.assertEqual(state.utility(0) + state.utility(1), 0)

    def test_utility_showdown_winner_is_higher_card(self):
        # p0 has King (higher) vs p1 Jack: p0 should win every showdown.
        state = play_out(KuhnPokerState(cards=(Card.KING, Card.JACK)), "pp")
        self.assertEqual(state.utility(0), 1)
        self.assertEqual(state.utility(1), -1)

    def test_utility_fold_awards_pot_to_non_folder(self):
        state = play_out(KuhnPokerState(cards=(Card.JACK, Card.KING)), "bp")
        # p0 bet with the worse hand, p1 folded anyway -> p0 still wins.
        self.assertEqual(state.utility(0), 1)
        self.assertEqual(state.utility(1), -1)

    def test_bet_pot_is_double_check_pot(self):
        cc = play_out(KuhnPokerState(cards=(Card.KING, Card.JACK)), "pp")
        bb = play_out(KuhnPokerState(cards=(Card.KING, Card.JACK)), "bb")
        self.assertEqual(abs(bb.utility(0)), 2 * abs(cc.utility(0)))

    def test_information_set_key_encodes_card_and_history(self):
        state = play_out(KuhnPokerState(cards=(Card.QUEEN, Card.JACK)), "p")
        self.assertEqual(state.information_set_key(0), "Qp")
        self.assertEqual(state.information_set_key(1), "Jp")

    def test_apply_action_rejects_action_after_terminal(self):
        state = play_out(KuhnPokerState(cards=(Card.KING, Card.JACK)), "pp")
        with self.assertRaises(ValueError):
            state.apply_action("p")

    def test_deal_outcomes_enumerates_every_ordered_deal_uniformly(self):
        outcomes = deal_outcomes()
        self.assertEqual(len(outcomes), 6)  # 3 cards, ordered, choose 2
        for _, prob in outcomes:
            self.assertEqual(prob, Fraction(1, 6))
        self.assertEqual(sum(prob for _, prob in outcomes), 1)
        dealt_hands = {state.cards for state, _ in outcomes}
        self.assertEqual(len(dealt_hands), 6)  # all distinct ordered pairs


if __name__ == "__main__":
    unittest.main()
