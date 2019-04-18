from pypokerengine.utils.card_utils import estimate_hole_card_win_rate
from pypokerengine.utils.card_utils import gen_cards
pattern = ['H', 'D', 'C', 'S']
number = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
all_cards = []
for p in pattern:
    for n in number:
        all_cards.append(p + n)
from itertools import combinations
combs = list(combinations(all_cards, 5))
rate = {}
f = open("rate", "r")
lines = f.readlines()
for line in lines:
    key = line[:2]
    value = int(line[8:10]) / 100.0
    rate.update({key: value})
for comb in combs:
    card = "".join(list(comb))
    win_rate = estimate_hole_card_win_rate(
        10000, 2, gen_cards(list(comb)[:2]), gen_cards(list(comb)[2:]))
    rate.update({card: win_rate})
import msgpack
with open('rate.msgpack', 'w') as outfile:
    msgpack.pack(rate, outfile)
