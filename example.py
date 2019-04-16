from pypokerengine.api.game import setup_config, start_poker
from randomplayer import RandomPlayer
from raise_player import RaisedPlayer
from rate_player import RatePlayer
from all_raise_player import AllRaisePlayer
from search_player import SearchPlayer
from simulation_player import ProbabilityPlayer

#TODO:config the config as our wish
config = setup_config(max_round=100, initial_stack=10000, small_blind_amount=10)

# config.register_player(name="call_player", algorithm=CallPlayer())
# config.register_player(name="random", algorithm=RandomPlayer())
config.register_player(name="runable", algorithm=ProbabilityPlayer())
config.register_player(name="allraise", algorithm=SearchPlayer())
game_result = start_poker(config, verbose=1)
print game_result