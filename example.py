from pypokerengine.api.game import setup_config, start_poker
from randomplayer import RandomPlayer
from raise_player import RaisedPlayer
from rate_player import RatePlayer
from all_raise_player import AllRaisePlayer
from search_player import SearchPlayer
from simulation_player import ProbabilityPlayer

# config.register_player(name="call_player", algorithm=CallPlayer())
# config.register_player(name="random", algorithm=RandomPlayer())
RaisedPlayer = RaisedPlayer()

for i in range(20):
	config = setup_config(max_round=10, initial_stack=10000, small_blind_amount=10)
	config.register_player(name="runable", algorithm=RaisedPlayer)
	config.register_player(name="allraise", algorithm=AllRaisePlayer())
	#TODO:config the config as our wish
	game_result = start_poker(config, verbose=1)
	print RaisedPlayer.root
	import cPickle
	# result = open('result' + str(i) + '.pkl', 'w')
	# cPickle.dump(RaisedPlayer.result, result)
	print RaisedPlayer.result
	ouf = open('tree.pkl', 'w')
	cPickle.dump(RaisedPlayer.tree, ouf)
	print game_result