from pypokerengine.players import BasePokerPlayer
from pypokerengine.utils.card_utils import estimate_hole_card_win_rate
from pypokerengine.utils.card_utils import gen_cards
from gameTree import Node, Tree
from AlphaBeta import AlphaBeta

class RaisedPlayer(BasePokerPlayer):
  start_stack = 0
  end_stack = 0
  result = []

  def __init__(self):
      import cPickle
      # self.root = Node("SB", None, 10, 20, ["HA", "S5"], 2)
      # self.tree = Tree(self.root)
      # self.tree.build_tree()
      inf = open('tree.pkl')
      self.tree = cPickle.load(inf)
      self.root = self.tree.root
      self.alpha_beta = None
      self.seat = None
      self.my_uuid = None
      self.current_node = self.root
      

  def explore_game_tree(self, round_state, win_rate):
    # print round_state
    self.current_node = self.root
    actions = []
    if round_state['street'] == 'preflop':
        actions = round_state['action_histories']['preflop']
    elif round_state['street'] == 'flop':
        actions = round_state['action_histories']['preflop'] + round_state['action_histories']['flop']
    elif round_state['street'] == 'turn':
        actions = round_state['action_histories']['preflop'] + round_state['action_histories']['flop'] + \
                  round_state['action_histories']['turn']
    elif round_state['street'] == 'river':
        actions = round_state['action_histories']['preflop'] + round_state['action_histories']['flop'] + \
                  round_state['action_histories']['turn'] + round_state['action_histories']['river']
    opponent_num = 0
    for action in actions:
      if self.my_uuid != action['uuid']:
          opponent_num += 1
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
          self.current_node = self.current_node.children[2]
      # print "----------------------"
      # print self.current_node
      # print "----------------------"
    final_action = self.alpha_beta.alpha_beta_search(self.current_node, win_rate, opponent_num)
    return final_action

  def declare_action(self, valid_actions, hole_card, round_state):
    fold_action, call_action, raise_action = list(map(lambda valid_action: valid_action['action'], valid_actions)) + [None] * (3 - len(valid_actions))
    if len(round_state['action_histories']['preflop']) == 2:
        my_role = "SB"
        self.my_uuid = round_state['action_histories']['preflop'][0]['uuid']
    elif len(round_state['action_histories']['preflop']) == 3:
        my_role = "BB"
        self.my_uuid = round_state['action_histories']['preflop'][1]['uuid']
    if len(round_state['action_histories']['preflop']) <= 3:
        self.tree.set_my_role(my_role)
        self.alpha_beta = AlphaBeta(self.tree)
    win_rate = estimate_hole_card_win_rate(1000, 2, gen_cards(hole_card), gen_cards(round_state['community_card']))
    print self.tree.my_role, win_rate
    if win_rate < 0.35 and fold_action is not None:
        return fold_action
    elif win_rate > 0.80 and raise_action is not None:
        return raise_action
    else:
        return self.explore_game_tree(round_state, win_rate)

  def receive_game_start_message(self, game_info):
    pass
  
  def receive_round_start_message(self, round_count, hole_card, seats):
    self.start_stack = seats[0]["stack"] if seats[0]["uuid"] == self.uuid else seats[1]["stack"]
    # print self.start_stack
    pass

  def receive_street_start_message(self, street, round_state):
    pass

  def receive_game_update_message(self, action, round_state):
    pass

  def receive_round_result_message(self, winners, hand_info, round_state):
    seats = round_state["seats"]
    self.end_stack = seats[0]["stack"] if seats[0]["uuid"] == self.uuid else seats[1]["stack"]
    self.update_node_weight(self.current_node)
    # print self.end_stack
    # print self.current_node
    pass

  def update_node_weight(self, node):
    win_money = self.end_stack - self.start_stack
    self.result.append(win_money)
    while node.parent != None and node.parent != "":
      node.weight += win_money / 1000
      node = node.parent

def setup_ai():
  return RaisedPlayer()
