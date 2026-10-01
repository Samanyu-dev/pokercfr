import itertools
import unittest

from kuhn_poker.env import Card, KuhnPokerState
from poker import LADDER, GameConfig, PokerState, deal_outcomes


class TestPokerGame(unittest.TestCase):
    def test_kuhn_config_matches_reference_kuhn_env(self):
        histories = ("pp", "bp", "bb", "pbp", "pbb")
        for c0, c1 in itertools.permutations(Card, 2):
            ref = KuhnPokerState(cards=(c0, c1))
            new = PokerState(LADDER["kuhn"], ((int(c0),), (int(c1),)))
            for h in histories:
                r, n = ref, new
                for a in h:
                    r, n = r.apply_action(a), n.apply_action(a)
                self.assertTrue(n.is_terminal())
                self.assertEqual(n.utilities(), [r.utility(0), r.utility(1)])
                self.assertEqual(n.information_set_key(0), r.information_set_key(0))

    def test_deal_counts_match_formula(self):
        for name, cfg in LADDER.items():
            if cfg.num_deals() < 10_000:
                self.assertEqual(len(deal_outcomes(cfg)), cfg.num_deals(), name)

    def test_three_player_bet_then_responses(self):
        cfg = GameConfig(ranks=4, players=3)
        s = PokerState(cfg, ((3,), (2,), (0,)))  # A, K, J
        for a in "pb":  # p0 checks, p1 bets
            s = s.apply_action(a)
        self.assertEqual(s.current_player(), 2)
        s = s.apply_action("p").apply_action("b")  # p2 folds, p0 calls
        self.assertTrue(s.is_terminal())
        self.assertEqual(s.utilities(), [3, -2, -1])  # A beats K; pot 5

    def test_pair_beats_high_card_and_ties_split(self):
        cfg = GameConfig(ranks=4, suits=2, cards_dealt=2)
        pair_of_jacks, ace_king = (0, 1), (7, 5)
        s = PokerState(cfg, (pair_of_jacks, ace_king), "pp")
        self.assertEqual(s.utilities(), [1, -1])
        tie = PokerState(cfg, ((7, 4), (6, 5)), "bb")  # A-Q vs A-Q, different suits
        self.assertEqual(tie.utilities(), [0, 0])


if __name__ == "__main__":
    unittest.main()
