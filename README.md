# poker_sim
Full No Limit Hold-Em game simulator with evaluation engine and full game specs

Version 0.0.1

Initialization:

from poker_sim import NoLimitHoldEm

game = NoLimitHoldEm(n_players) 
where n_players = numer of players 

Deal cards and wait for action:
game.deal()

Deal community and wait for action:
game.flop()
game.turn()
game.river()
