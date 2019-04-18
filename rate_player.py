from pypokerengine.players import BasePokerPlayer
from pypokerengine.utils.card_utils import estimate_hole_card_win_rate
from pypokerengine.utils.card_utils import gen_cards
import random as rand
import pprint

class RatePlayer(BasePokerPlayer):

  def declare_action(self, valid_actions, hole_card, round_state):
    win_rate = estimate_hole_card_win_rate(1000, 2, gen_cards(hole_card), gen_cards(round_state['community_card']))
    if win_rate > 0.75 and len(valid_actions) == 3:
        action = call_action_info = valid_actions[2]["action"]
    elif win_rate > 0.25:
        action = call_action_info = valid_actions[1]["action"]
    else:
        action = call_action_info = valid_actions[0]["action"]
    return action

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
  return RatePlayer()
