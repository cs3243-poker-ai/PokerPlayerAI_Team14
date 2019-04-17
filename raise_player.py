from pypokerengine.players import BasePokerPlayer
from pypokerengine.utils.card_utils import estimate_hole_card_win_rate
from pypokerengine.utils.card_utils import gen_cards
from gameTree import Node, Tree
from AlphaBeta import AlphaBeta

class RaisedPlayer(BasePokerPlayer):
  def __init__(self):
      self.root = Node("SB", None, 10, 20, ["HA", "S5"], 2)
      self.tree = Tree(self.root)
      self.tree.build_tree()
      self.alpha_beta = None
      self.seat = None
      self.my_uuid = None

  def explore_game_tree(self, round_state, win_rate):
    # print round_state
    self.current_node = self.root
    actions = []
    # print len(round_state['action_histories']), "***"
    if len(round_state['action_histories']) == 1:
        actions = round_state['action_histories']['preflop']
    elif len(round_state['action_histories']) == 2:
        actions = round_state['action_histories']['preflop'] + round_state['action_histories']['flop']
    elif len(round_state['action_histories']) == 3:
        actions = round_state['action_histories']['preflop'] + round_state['action_histories']['flop'] + \
                  round_state['action_histories']['turn']
    elif len(round_state['action_histories']) == 4:
        actions = round_state['action_histories']['preflop'] + round_state['action_histories']['flop'] + \
                  round_state['action_histories']['turn'] + round_state['action_histories']['river']
    opponent_num = 0
    for action in actions:
      if action['action'] == 'FOLD':
          self.current_node = self.current_node.children[0]
      elif action['action'] == 'CALL':
          pos = 0
          if "Host" in self.current_node.children[1].role:
              if win_rate > 0.66:
                  pos = 2
              elif win_rate > 0.33:
                  pos = 1
          self.current_node = self.current_node.children[1].children[pos] if "Host" in self.current_node.children[1].role else self.current_node.children[1]
      elif action['action'] == 'RAISE':
          # print actions
          self.current_node = self.current_node.children[2]
          # if action['uuid'] != self.my_uuid:
          #     raise_num += 1
      if self.my_uuid != action['uuid']:
          opponent_num += 1
    print self.tree.my_role, win_rate
    # print self.current_node
    final_action = self.alpha_beta.alpha_beta_search(self.current_node, win_rate, opponent_num)
    # print final_action, " !!!!!"
    return final_action

  def declare_action(self, valid_actions, hole_card, round_state):
#    print "declare action!!!!"
#     print round_state
    if len(round_state['action_histories']['preflop']) == 2:
        my_role = "SB"
        self.my_uuid = round_state['action_histories']['preflop'][0]['uuid']
    elif len(round_state['action_histories']['preflop']) == 3:
        my_role = "BB"
        self.my_uuid = round_state['action_histories']['preflop'][1]['uuid']
        
    if len(round_state['action_histories']['preflop']) <= 3:
        # print round_state
        # print my_role, "!!!"
        self.tree.set_my_role(my_role)
        # print my_role
        self.alpha_beta = AlphaBeta(self.tree)
    # fold_action, raise_action, call_action = list(map(lambda valid_action: valid_action['action'], valid_actions)) + [None] * (3 - len(valid_actions))
    win_rate = estimate_hole_card_win_rate(1000, 2, gen_cards(hole_card), gen_cards(round_state['community_card']))
    # print "my win rate: ", win_rate
    # if win_rate < 0.25 and fold_action != None:
    #     return fold_action
    # # elif win_rate > 0.65 and raise_action != None:
    # #     return raise_action
    # else:
#        return call_action
#        remaining_actions = [raise_action, call_action]
    return self.explore_game_tree(round_state, win_rate)

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
  return RaisedPlayer()
