from pypokerengine.utils.card_utils import estimate_hole_card_win_rate
from pypokerengine.utils.card_utils import gen_cards
from tqdm import tqdm as tqdm
import pandas as pd

pattern = ['H', 'D', 'C', 'S']
number = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
card = []
win_rate_list = []
for p in pattern:
    for n in number:
        card.append(p + n)
for i in tqdm(range(len(card))):
    for j in range(i + 1, len(card)):
        pair = [card[i], card[j]]
        win_rate = estimate_hole_card_win_rate(1000, 2, gen_cards(pair))
        win_rate_list.append([pair, win_rate])

data_frame = pd.DataFrame(win_rate_list);
data_frame.to_csv("win_rate_list_for_two cards");
