import unittest

from cfr.vanilla import VanillaCFR, expected_values
from poker import LADDER, deal_outcomes


class TestVanillaCFRKuhn(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.outcomes = deal_outcomes(LADDER["kuhn"])
        cls.solver = VanillaCFR(cls.outcomes)
        cls.solver.train(20_000)
        cls.avg = cls.solver.average_strategy()

    def test_twelve_information_sets(self):
        self.assertEqual(len(self.avg), 12)

    def test_game_value_is_minus_one_eighteenth(self):
        # Kuhn 1950: player 0's equilibrium value is -1/18.
        self.assertAlmostEqual(expected_values(self.avg, self.outcomes)[0], -1 / 18, places=3)

    def test_player1_equilibrium_is_unique(self):
        # Player 1's Nash strategy in Kuhn is unique (unlike player 0's α-family).
        b = lambda key: self.avg[key]["b"]
        self.assertAlmostEqual(b("Jp"), 1 / 3, delta=0.02)  # bluff with J after a check
        self.assertAlmostEqual(b("Qb"), 1 / 3, delta=0.02)  # call with Q facing a bet
        self.assertLess(b("Jb"), 0.01)  # always fold J to a bet
        self.assertLess(b("Qp"), 0.01)  # never bet Q after a check
        self.assertGreater(b("Kb"), 0.99)
        self.assertGreater(b("Kp"), 0.99)

    def test_player0_lies_on_alpha_family(self):
        # Player 0: bet J with α ∈ [0, 1/3], bet K with 3α, call Q with α + 1/3.
        b = lambda key: self.avg[key]["b"]
        alpha = b("J")
        self.assertLessEqual(alpha, 1 / 3 + 0.01)
        self.assertAlmostEqual(b("K"), 3 * alpha, delta=0.02)
        self.assertAlmostEqual(b("Qpb"), alpha + 1 / 3, delta=0.02)
        self.assertLess(b("Q"), 0.01)


class TestVanillaCFRLadder(unittest.TestCase):
    def test_runs_on_every_small_rung(self):
        for name in ("4rank-2suit-2dealt", "kuhn-3p", "4rank-2suit-4p"):
            cfg = LADDER[name]
            outcomes = deal_outcomes(cfg)
            solver = VanillaCFR(outcomes)
            solver.train(3)
            self.assertEqual(len(solver.average_strategy()), cfg.num_info_sets(), name)
            values = expected_values(solver.average_strategy(), outcomes)
            self.assertAlmostEqual(sum(values), 0, places=9, msg=name)  # zero-sum


if __name__ == "__main__":
    unittest.main()
