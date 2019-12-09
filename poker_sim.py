# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 13:30:31 2019

@author: eric.qian
"""

from utils import *
from objs import *
import numpy as np


class NoLimitHoldEm:
    
    
    def __init__(self, n_players = 7):
        
        # Instantiate players wit ID
        self.players = {}
        self.n_players = n_players
        
        # Random seat draw
        self.seats = [i for i in range(n_players)]
        np.random.shuffle(self.seats)
        
        for i, seat in enumerate(self.seats):
            
            self.players[seat] = Player()
            self.players[seat].id = i
            self.players[seat].seat = seat
            
        # Random button draw
        self.button = np.random.randint(0,self.n_players)
        self.small = (self.button + 1)%self.n_players
        self.big = (self.small + 1)%self.n_players
        self.utg = (self.big + 1)%self.n_players
                
        # Community cards
        self.field = []
        
        # Deck
        self.cards = Deck()
        
        # Pot variable
        self.pot = 0
        
        # Reset seats
        self.in_pot = [(seat+self.small)%self.n_players for seat in range(self.n_players)]
        
        print(f'Big blind: {self.big}')
        print(f'Small blind: {self.small}')
        print(f'Button: {self.button}')

        return
    
    
    def new_hand(self):
        
        
        print(f'Big blind: {self.big}')
        print(f'Small blind: {self.small}')
        print(f'Button: {self.button}')


        # Use the fold function to refresh player hands 
        for i in range(self.n_players):
            self.players[i].fold()
        
        # Move button
        self.button = (self.button+1)%self.n_players
        self.small = (self.button + 1)%self.n_players
        self.big = (self.small + 1)%self.n_players
        self.utg = (self.big + 1)%self.n_players

        # Clear community cards
        self.field = []
        
        # Reset pot 
        self.pot = 0
        
        # Reset seats
        self.in_pot = [(seat+self.small)%self.n_players for seat in range(self.n_players)]

            
    def deal(self):

        # Shuffle and deal new hand
        self.cards.new_draw()        
        
        # Deal hole cards
        for j in range(2):
            for i in range(self.n_players):                   
                seat = (i + self.small)%self.n_players
                self.players[seat].cards.extend(self.cards.draw(1))
        
        # Assess action
        self.action(is_deal = True)


    def burn(self):
        # Burn cards
        self.cards.draw(1)
        
        
    def river(self):
        # Burn deal river, assess action, showdown
        self.burn()
        self.field.extend(self.cards.draw(1))
        self.update_player_cards()
        self.action()
        self.showdown()
        
    def turn(self):
        # Burn deal turn, assess action
        self.burn()
        self.field.extend(self.cards.draw(1))
        self.update_player_cards()
        self.action()

        
    def flop(self):
        # Burn deal flop, assess action
        self.burn()        
        self.field.extend(self.cards.draw(3))
        self.update_player_cards()
        self.action()
        
        
    def action(self, is_deal = False):        
        # Defines action
        # Action stays the same, is applied in all streets
        
        closed = False
        
        if is_deal:
            current_bet = 2
            # Blinds
            self.pot = 3
            self.players[self.small].bet(1)
            self.players[self.big].bet(2)
        else:
            current_bet = 0
            for seat in self.in_pot:
                self.players[seat].curr_bet = 0
            
            
        user_input = ''
        folded = []
        
        orbits = -1
        while not closed:
            
            orbits += 1
            for i, seat in enumerate(self.in_pot):
                
                if is_deal and orbits == 0:
                    if i == 0 or i == 1:
                        continue
                
                if is_deal and orbits == 1:
                    if i == 2:
                        break
                
                print(i)
                print(f'Player {seat}')
                print(f'Players in hands {self.in_pot}')
                print(f'Current pot size {self.pot}')
                print(f'Current stack size {self.players[seat].stack}')
                print(f'Current bet is {self.players[seat].curr_bet}')
                print(f'To play: {current_bet - self.players[seat].curr_bet}')
                print(f'Your hand is {self.players[seat].cards}')
                
                user_input = input(f'The current bet is {current_bet}, Raise/Call/Fold?: ')
                parse_dat  = user_input.split()
                user_action = parse_dat[0].lower()                 
                        
                if len(parse_dat) == 2:
                    bet_amount = int(parse_dat[1])
                else:
                    bet_amount = current_bet
                    
                if user_action == 'fold':
                    folded.append(seat)
                    self.players[seat].fold()
                
                if user_action == 'break':
                    closed = True
                    break
                    
                if user_action == 'bet' or user_action == 'raise' or user_action == 'call' or user_action == 'check':
                    current_bet = bet_amount
                    self.pot += self.players[seat].bet(current_bet)
                
                if orbits >= 1:
                    for seat in self.in_pot:
                        if self.players[seat].curr_bet != current_bet:
                            break
                        else:
                            closed = True
                    
                    if closed: 
                        break

            self.in_pot = [seat for seat in self.in_pot if seat not in folded]
            
            for seat in self.in_pot:
                if self.players[seat].curr_bet != current_bet:
                    break
                else:
                    closed = True
                    
        return None
    
    
    def showdown(self):
        
        hands = []
        # Unfolded players
        for seat in self.in_pot:
            self.players[seat].eval_cards()
            hands.append(self.players[seat].strongest_strength)
        
        # Evaluate winning seat strongest hand
        winning_seat = self.in_pot[eval_hands(hands)]
        strongest_hand = self.players[winning_seat].strongest_strength
        strongest_desc = self.players[winning_seat].strongest_desc
        
        # Evaluate splits
        winning_seats = []
        for seat in self.in_pot:
            if self.players[seat].strongest_strength == strongest_hand:
                winning_seats.append(seat)
                
                
        print('Seat(s) ' + str(winning_seats) + ' have won the pot of ' + str(self.pot) + ' with ' + strongest_desc)

        self.issue_pot(winning_seats)
        
        
    def issue_pot(self, winning_seats):
        
        # Issue pot, divide to winning seats
        
        n_winners = len(winning_seats)
        for seat in winning_seats: 
            self.players[seat].stack += self.pot/n_winners


    def update_player_cards(self):
        
        for seat in self.in_pot:
            self.players[seat].cards = self.players[seat].cards[0:2]
            self.players[seat].cards.extend(self.field) 
            
            
            