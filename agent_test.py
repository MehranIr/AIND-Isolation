"""This file is provided as a starting template for writing your own unit
tests to run and debug your minimax and alphabeta agents locally.  The test
cases used by the project assistant are not public.
"""

import unittest

import isolation
import game_agent

from importlib import reload


class IsolationTest(unittest.TestCase):
    """Unit tests for isolation agents"""

    def setUp(self):
        reload(game_agent)
        self.player1 = "Player1"
        self.player2 = "Player2"
        self.game = isolation.Board(self.player1, self.player2)
        self.minimaxPlayer = game_agent.MinimaxPlayer()
        self.isoPlayer= game_agent.IsolationPlayer(2,game_agent.custom_score,10)
#         self.minimaxPlayer2 = self.isoPlayer.MinimaxPlayer()
    
    def timer(self):
        return 150
    
    def test_minimax(self):
        self.assertEqual(self.minimaxPlayer.get_move(self.game, self.timer),)


if __name__ == '__main__':
    unittest.main()
#     game_agent.minimax(game, 3)
