# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 13:54:27 2019

@author: eric.qian
"""

from collections import Counter
from itertools import combinations

# Numeric hand rankings, higher integer value is stronger hand
HAND_RANKINGS = {0: 'High Card',
                 1: 'One Pair',
                 2: 'Two Pair',
                 3: 'Trips', 
                 4: 'Straight', 
                 5: 'Flush',
                 6: 'Full House',
                 7: 'Quads',
                 8: 'Straight Flush'}

# Card values mapped to integer strengths, higher integer value stronger
CARD_VALS =   {'2':1,
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
# Cache mapper
REVERSE_VALS = {v:k for k,v in CARD_VALS.items()}


def check_flush(suits):
    
    # If count of suits equals length of hand
    if suits.count(suits[0]) == len(suits):
        return True
    

def check_strt(card_vals):
    
    # Edge case of A,2,3,4,5 straight
    if sorted(card_vals) == [1,2,3,4,13]:
        return True
    
    # If sorted(hand) - min evaluates to 0,1,2,3,4
    if [i - min(card_vals) for i in sorted(card_vals)] == [0,1,2,3,4]:
        return True
        
    
def read_hand(hand):
    
    """
    hand :: list of str :: unordered str hand value representation, i.e. ['As','As','2h','2s','Ks']
    =========
    returns
    hand_strength :: list of int :: sequential integer representation of hand strs, 
    [HAND_RANKINGS, HIGH_CARD_1, HIGH_CARD_2, HIGH_CARD_3, HIGH_CARD_4] in descending strength priority
    For example, if we have Two pairs Aces and 2s w/ K high:
    [2,13,1,12] -> [Two Pair int val, Ace int val, 2 int val, K int val]
    
    desc :: str :: full description of hand
    """
    
    # Initialize ranking and descriptiong 
    ranking = 0
    desc = ''
    
    # Split card vals and suits. 10 is edge case
    suits = [i[1] if '10' not in i else i[2] for i in hand]
    card_vals = [CARD_VALS[i[0]] if '10' not in i else CARD_VALS['10'] for i in hand]
    
    # Unique card counts, hands are easily evaluated with dict of count of cards
    card_counter = Counter(card_vals)
    
    # Straight flush ranking
    if check_flush(suits) and check_strt(card_vals):    
        ranking = 8
    # Flush ranking
    elif check_flush(suits):
        ranking = 5
    # Straight ranking
    elif check_strt(card_vals):
        ranking = 4
    # If there are only 2 unique cards, must be quads or full house
    elif len(card_counter) == 2:
        # If 2 cards and counts are 3,2 is full house
        if 3 in card_counter.values():
            ranking = 6
        # Otherwise, quads
        else:
            ranking = 7
    # Must be trips or two pairs
    elif len(card_counter) == 3:
        if 3 in card_counter.values():
            ranking = 3
        else:
            ranking = 2
    # Must be one pairs
    elif len(card_counter) == 4:
        ranking = 1
    # High card
    else:
        ranking = 0
    
    # Init hand strength vector
    hand_strength = [ranking]
    
    # Add hand strength data 
    # Sort card counter dict by count, card integer value, and add data.  This is enough info to rank hands
    sorted_high_cards = sorted(card_counter.items(), key=lambda x: (x[1],x[0]), reverse=True)
    for i in range(len(sorted_high_cards)):
        hand_strength.append(sorted_high_cards.pop(0)[0])
    
    # Logic to describe hand
    desc_vals = [str(REVERSE_VALS[i]) if idx > 0 else 'None' for idx, i in enumerate(hand_strength)]
    
    if ranking == 8:
        if 13 in hand_strength and 4 in hand_strength:
            return 'Straight Flush 5 high'
        else:
            desc = 'Straight Flush ' + desc_vals[1] + ' high' 
    elif ranking == 7:
        desc = 'Quad ' + desc_vals[1] + ' ' + desc_vals[2] + ' high' 
    elif ranking == 6:
        desc = 'Full House ' + desc_vals[1] + ' full of ' + desc_vals[2]
    elif ranking == 5:
        desc = 'Flush ' + desc_vals[1] + ' high'
    elif ranking == 4:
        desc = 'Straight ' + desc_vals[1] + ' high'
    elif ranking == 3:
        desc = 'Trip ' + desc_vals[1] 
    elif ranking == 2:
        desc = 'Two Pairs ' + desc_vals[1] + ' and '+desc_vals[2]+' '+desc_vals[3]+' high'
    elif ranking == 1:
        desc = 'One Pair ' + desc_vals[1] + ' ' + desc_vals[2] + desc_vals[3] + desc_vals[4] + ' high' 
    elif ranking == 0:
        desc = 'High Card ' + desc_vals[1] + ' ' + desc_vals[2] + desc_vals[3] + desc_vals[4] + desc_vals[5] +' high' 

        
    return hand_strength, desc
    
    
def eval_hands(hands):
    
    """
    hands :: list :: list of int hand_strength, 1st output of read_hand
    =======
    Returns
    candidates :: iterable :: strongest hand(s), may be more than 1 hand if there is a split
    """
    
    card = 0 
    candidates = [i for i in range(len(hands))]
    
    # Evaluates hands
    # Looks at first index of each hand in hands, retains largest
    # Iterates over indices, each time retaining largest int (strongest hand hierarchically)
    
    while len(candidates) != 1:
        
        try:
            strongest = max([hands[hand][card] for hand in candidates])
            keep = []
            for i in range(len(candidates)):
                if strongest == hands[candidates[i]][card]:
                    keep.append(i)
                    
            candidates = [candidates[i] for i in keep]
            card += 1
        except:
            # If there is more than 1 strongest hand, splits
            break
        
    return candidates[0]
    
    
def eval_combos(hands):
    
    # Given several hands, find the strongest hand with our evaluation engine above
    
    hand_strs = []
    descs = []
    
    for hand in hands:
        hand_str, desc = read_hand(hand)
        hand_strs.append(hand_str)
        descs.append(desc)
    
    strongest_hand = eval_hands(hand_strs)
    
    return hands[strongest_hand], hand_strs[strongest_hand], descs[strongest_hand]


def combos(cards, n = 5):
    
    # Create hand combos    
    return [list(combo) for combo in combinations(cards, n)]



