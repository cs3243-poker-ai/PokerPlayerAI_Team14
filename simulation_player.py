from pypokerengine.players import BasePokerPlayer
from time import sleep
import pprint

from pypokerengine.utils.card_utils import estimate_hole_card_win_rate
from pypokerengine.utils.card_utils import gen_cards


# This player reacts based on mathmatical expectation calculated by the current probability.
# The playing idea base is when the money is on the table, those money will no longer be your money.
class ProbabilityPlayer(BasePokerPlayer):
    def declare_action(self, valid_actions, hole_card, round_state):

        moneyOnTable = round_state['pot']['main']['amount']
        moneyToCall = 20
        moneyToRaise = 20
        wining_probability = estimate_hole_card_win_rate(300, 2, gen_cards(hole_card),
                                                         gen_cards(round_state['community_card']));
        # the mathmatical expectation of Fold is 0
        ex_call = wining_probability * (moneyOnTable + moneyToCall) - moneyToCall;  # math expectation for calling
        ex_raise = wining_probability * (
        moneyOnTable + 2 * moneyToRaise + moneyToCall) - moneyToRaise - moneyToCall;  # math expectation for raising
        # if max(0, ex_call, ex_raise) == 0

        has_action_raise = False
        has_action_flod = False
        has_action_call = False
        for i in valid_actions:
            if i["action"] == "raise":
                # action_raise = i["action"]
                has_action_raise = True
                # return action  # action returned here is sent to the poker engine
            if i["action"] == "fold":
                # action_fold = i["action"]
                has_action_fold = True
            if i["action"] == "call":
                # action_call = i["action"]
                has_action_call = True

        if wining_probability > 0.23 and has_action_raise == True:
            action = 'raise'
        elif has_action_call == True:
            action = 'call'
        else:
            action = 'fold'
            # if max(ex_call, ex_raise, 0) == ex_raise and has_action_raise == True:
            #     action = 'raise'
            # elif max(ex_raise, ex_call, 0) == ex_call and has_action_call == True:
            #     action = 'call'
            # else:
            action = 'fold'
        '''
        print(wining_probability)
        print("\n")
        print(round_state)
        print("\n")
        print(valid_actions)
        print("\n")
        print(moneyOnTable)
        print("\n")
        print(ex_call)
        print("\n")
        print(ex_raise)
        '''
        return action  # action returned here is sent to the poker engine

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
    return ProbabilityPlayer()