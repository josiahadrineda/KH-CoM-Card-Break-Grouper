"""
GOAL: Group the cards in threes so as to maximize CP

HEURISTICS:
1. Each of the three cards must be of different types
2. Above rule must still apply after the removal of the first card in each grouping of three
3. Prioritize lowest CP
"""

def order(cards, attack_range, CP):
    print("Order of Types:\n['K', 'O', 'LL']\n['LL', 'K', 'O']\n['O', 'LL', 'K']\n")

    groups = []
    i = 0
    while CP > 0:
        first = min_max(cards)
        remaining_two = two_sum(first, cards, attack_range)
        while not remaining_two:
            try:
                cards['LL'].pop(0)
            except:
                return groups, CP

            first = min_max(cards)
            remaining_two = two_sum(first, cards, attack_range)

        if first == None or remaining_two == None:
            break
        else:
            CP -= sum([first[0][1], remaining_two[0][1], remaining_two[1][1]])
        
        if i % 3 == 0:
            groups.append([remaining_two[0], remaining_two[1], first[0]])
        elif i % 3 == 1:
            groups.append([first[0], remaining_two[0], remaining_two[1]])
        else:
            groups.append([remaining_two[1], first[0], remaining_two[0]])
        i += 1

    if CP < 0:
        while CP < 0:
            min_card = min(groups[-1])
            CP += min_card[1]
            groups[-1].remove(min_card)

            if len(groups[-1]) == 0:
                groups.pop()
    return groups, CP

def min_max(cards):
    try:
        first = min(cards['LL'])
        cards['LL'].remove(first)
        return [first]
    except:
        return None

def two_sum(first, cards, attack_range):
    remaining_two = []
    k_set = sorted([list(card) for card in set(tuple(card) for card in cards['K'])])
    o_set = sorted([list(card) for card in set(tuple(card) for card in cards['O'])])
    for i in range(len(o_set)):
        for j in range(len(k_set)):
            try:
                if attack_range[0] <= sum([o_set[i][0], k_set[j][0], first[0][0]]) <= attack_range[1]:
                    remaining_two.append(k_set[j])
                    remaining_two.append(o_set[i])
                    cards['K'].remove(k_set[j])
                    cards['O'].remove(o_set[i])
                    return remaining_two
            except:
                return None

"""
1. Take smallest valued card for most expensive type (don't pop. if there is no combo that falls in the specified range, move on to the next highest card)
2. Two sum for two smallest types (if one of these two smallest types have no elements, move on to the next expensive type)
3. If a grouping has been found, return
"""

#Setup
import collections
import csv

cards = collections.defaultdict(list)
reader = csv.DictReader(open('/home/osboxes/Desktop/Programming/Python/Projects/KH: CoM Card Grouper/KH_ CoM Card List - Sheet1.csv', 'r'))
for row in reader:
    for _ in range(int(row['Count'])):
        cards[row['Type']].append([int(row['Number']), int(row['CP'])])

attack_range = [15,15]
CP = 620

#Driver code
from pprint import pprint

pprint(order(cards, attack_range, CP))