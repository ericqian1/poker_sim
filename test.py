# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 15:08:29 2019

@author: eric.qian
"""

from poker_sim import NoLimitHoldEm


game = NoLimitHoldEm(5)

for i in range(1):
    
    game.deal()
    game.flop()
    game.turn()
    game.river()
    
    print('Button: ' + str(game.button))
    
    for i in range(5):
        print(game.players[i].strongest_desc)
        print(game.players[i].stack)

    game.new_hand()