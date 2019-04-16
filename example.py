from pypokerengine.api.game import setup_config, start_poker
from randomplayer import RandomPlayer
from raise_player import RaisedPlayer

#TODO:config the config as our wish
config = setup_config(max_round=20, initial_stack=10000, small_blind_amount=10)



config.register_player(name="test", algorithm=RandomPlayer())
config.register_player(name="runable", algorithm=RaisedPlayer())

game_result = start_poker(config, verbose=1)
print game_result
