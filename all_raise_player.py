from pypokerengine.players import BasePokerPlayer
from pypokerengine.utils.card_utils import estimate_hole_card_win_rate
from pypokerengine.utils.card_utils import gen_cards
import random as rand
import pprint

class AllRaisePlayer(BasePokerPlayer):

  def declare_action(self, valid_actions, hole_card, round_state):
    # valid_actions format => [raise_action_pp = pprint.PrettyPrinter(indent=2)
    #pp = pprint.PrettyPrinter(indent=2)
    #print("------------ROUND_STATE(RANDOM)--------")
    #pp.pprint(round_state)
    #print("------------HOLE_CARD----------")
    #pp.pprint(hole_card)
    #print("------------VALID_ACTIONS----------")
    #pp.pprint(valid_actions)
    #print("-------------------------------")
<<<<<<< HEAD
    print "information of all_raise"
    print len(round_state["action_histories"]["preflop"])
=======
>>>>>>> 923b4eefec9714b8fe142d58554f254612e30c4f
    win_rate = estimate_hole_card_win_rate(1000, 2, gen_cards(hole_card), gen_cards(round_state['community_card']))
    # if win_rate <= 0.5:
    #   call_action_info = valid_actions[1]
    # elif r<= 0.9 and len(valid_actions ) == 3:
    #   call_action_info = valid_actions[2]
    # else:
    #   call_action_info = valid_actions[0]
    # action = call_action_info["action"]
    # return action  # action returned here is sent to the poker engine
    if len(valid_actions) == 3:
        action = call_action_info = valid_actions[2]["action"]
    else:
        action = call_action_info = valid_actions[1]["action"]
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
  return AllRaisePlayer()
