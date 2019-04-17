from pypokerengine.players import BasePokerPlayer
from time import sleep
import pprint
from pypokerengine.utils import card_utils
from pypokerengine.engine.card import Card

class SearchPlayer(BasePokerPlayer):
  LEVEL_DEEPER = 1

  def look_up_probability(self, hole_card, community_card):
    return 0.5

  def get_probability(self, hole_card, community_card):
    if len(hole_card) + len(community_card) <= 1:
      return self.look_up_probability(hole_card, community_card)
    elif len(hole_card) + len(community_card) == 7:
      return card_utils.evaluate_hand(hole_card, community_card)
    else:
      used_card = hole_card + community_card
      used = [card.to_id() for card in used_card]
      unused = [card_id for card_id in range(1, 53) if card_id not in used]
      new_commu = community_card
      sum = 0.0
      count = 0
      for item in unused:
        new_commu.append(Card.from_id(item))
        prob = card_utils.estimate_hole_card_win_rate(20, 2, hole_card, new_commu)
        sum += prob
        count += 1
        new_commu.pop()
      return sum / count


  def declare_action(self, valid_actions, hole_card, round_state):
    print valid_actions
    prob = self.get_probability(card_utils.gen_cards(hole_card), card_utils.gen_cards(round_state['community_card']))
    print prob
    for i in valid_actions:
      if i["action"] == "raise":
        if prob > 0.7:
          return i["action"]
    if prob < 0.3:
      return "fold"
    return "call"

  def receive_game_start_message(self, game_info):
    pass

  def receive_round_start_message(self, round_count, hole_card, seats):
    pass

  def receive_street_start_message(self, street, round_state):
    pass

  def receive_game_update_message(self, action, round_state):
    pass

  def receive_round_result_message(self, winners, hand_info, round_state):
    pass

def setup_ai():
  return SearchPlayer()
