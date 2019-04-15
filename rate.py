#to generate the winning rate of holding two cards only, card are in alphbet order, colors are s r d
from pypokerengine.utils.card_utils import estimate_hole_card_win_rate
from pypokerengine.utils.card_utils import gen_cards
pattern = ['H', 'D', 'C', 'S']
number = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
all_cards = []
for p in pattern:
    for n in number:
        all_cards.append(p + n)
from itertools import combinations
combs = list(combinations(all_cards, 2))
rate = {}
from tqdm import tqdm
for comb in tqdm(combs):
    card1 = comb[0][1]
    card2 = comb[1][1]
    assert card1 != "" or card2 != ""
    if card1 > card2:
        card1, card2 = card2, card1
    f = "s" if comb[0][0] == comb[1][0] else "d"
    key = card1 + card2 + f
    if rate.get(key) is None:
        win_rate = estimate_hole_card_win_rate(
            1000, 2, gen_cards(comb))
        rate.update({key: win_rate})

import msgpack
with open('rate_2c.msgpack', 'w') as outfile:
    msgpack.pack(rate, outfile)
# code for unpacking rate
# import msgpack
# with open('rate_2c.msgpack') as data_file:
#     rate = msgpack.unpack(data_file)