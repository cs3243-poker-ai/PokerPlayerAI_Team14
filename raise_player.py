from pypokerengine.players import BasePokerPlayer
from time import sleep
import pprint
from random import choice
from pypokerengine.utils.card_utils import estimate_hole_card_win_rate
from pypokerengine.utils.card_utils import gen_cards
from gameTree import Node, Tree

class RaisedPlayer(BasePokerPlayer):

  def explore_game_tree(self, hole_card, round_state, actions):
    return choice(list(filter(lambda x: x != None, actions)))

  def declare_action(self, valid_actions, hole_card, round_state):
#    print round_state
    fold_action, raise_action, call_action = list(map(lambda valid_action: valid_action['action'], valid_actions)) + [None] * (3 - len(valid_actions))
    win_rate = estimate_hole_card_win_rate(1000, 2, gen_cards(hole_card + round_state['community_card']))
    if win_rate < 0.25 and fold_action != None:
        return fold_action
    elif win_rate > 0.75 and raise_action != None:
        return raise_action
    else:
#        return call_action
        remaining_actions = [raise_action, call_action]
        return self.explore_game_tree(hole_card, round_state, remaining_actions)

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
  return RandomPlayer()
