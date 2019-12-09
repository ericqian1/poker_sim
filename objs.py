# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 13:31:37 2019

@author: eric.qian
"""
import numpy as np
from utils import *

class Deck:
    
    def __init__(self):
        
        # Cached data to describe 52 card deck
        self.suits = ['h','c','d','s']
        self.card_values = {'2':1,
                           '3':2,
                           '4':3,
                           '5':4,
                           '6':5,
                           '7':6,
                           '8':7,
                           '9':8,
                           '10':9,
                           'J':10,
                           'Q':11,
                           'K':12,
                           'A':13}
        
        # Read in cards
        self.cards = {}
        for k,v in self.card_values.items():
            for s in self.suits:
                self.cards[k+s] = v
        
        # Draws from static_deck, curr_deck is used in games
        self.static_deck = [k for k in self.cards.keys()]
        self.curr_deck = [k for k in self.cards.keys()]

    
    def new_draw(self, shuffle = True):
        
        # Generate new deck and shuffle
        self.curr_deck = self.static_deck.copy()
        
        if shuffle:
            self.shuffle()
        
        
    def shuffle(self):
        
        np.random.shuffle(self.curr_deck)
                
    
    def draw(self, cards):
        
        # Pop cards as draw
        hand = []
        
        for i in range(cards):    
            hand.append(self.curr_deck.pop(0))
            
        return hand
    
    
class Player:

    
    def __init__(self, stack = 100):
        
        """
        stack :: int :: big blind representation of hand
        """
        
        # The players' card data
        self.cards = []
        self.strongest = []
        self.strongest_desc = ''
        self.strongest_strength = []
        self.stack = stack
        self.curr_bet = 0
        
        # Game meta information
        self.id = None
        

    def eval_cards(self):        
        
        # Evaluates strongest hand based on cards
        self.strongest, self.strongest_strength, self.strongest_desc = eval_combos(combos(self.cards))
    

    def bet(self,val):
        
        val = min(val, self.stack)
        self.stack += self.curr_bet
        last_bet = self.curr_bet
        self.stack -= val
        self.curr_bet = val
            
        return val - last_bet


    def fold(self):
        
        # Reinitiliaze data for next hand on fold
        self.cards = []
        self.strongest = []
        self.strongest_desc = ''
        self.strongest_strength = []
        self.curr_bet = 0
    
    
        
        
        
        