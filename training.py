from pypokerengine.api.game import setup_config, start_poker
from randomplayer import RandomPlayer
from raise_player import RaisedPlayer
from rate_player import RatePlayer
from all_raise_player import AllRaisePlayer
from AlphaBeta import AlphaBeta 
from raise_player import RaisedPlayer 

# This training only attempt to obtain the value of factors[0]
	
def trainingFactor(initialValue, adjustingSize, trainingTimes, numOfValues):

	RaisedPlayer.foldThreshold = initialValue	
	maxValue = 0
	for j in range(0, numOfValues):
		totalResult = 0
		print("The factor:", RaisedPlayer.foldThreshold)

		for k in range(0, trainingTimes):
			config = setup_config(max_round=100, initial_stack=10000, small_blind_amount=10)
			# config.register_player(name="call_player", algorithm=CallPlayer())
			# config.register_player(name="random", algorithm=RandomPlayer())
			config.register_player(name="runable", algorithm=RaisedPlayer())
			config.register_player(name="allraise", algorithm=AllRaisePlayer())
			game_result = start_poker(config, verbose=1)
			print game_result
			totalResult += game_result['players'][0]['stack'] 
			
			# To change the variables of the function	
	
		# print("The factor:", AlphaBeta.factors[0])
		aveResult = totalResult/trainingTimes
		print("The aveResult:", aveResult)
		maxValue = max(aveResult, maxValue)
		if (aveResult == maxValue): 
			optimalFactor = RaisedPlayer.foldThreshold
		print("Current Max", maxValue, "current optimalFactor:", optimalFactor)
		trainingResult = "foldThreshold value:" + str(RaisedPlayer.foldThreshold) + "aveResult:" + str(aveResult) 
		import cPickle
		result = open('trainingResult' + ' foldThreshold' + str(RaisedPlayer.foldThreshold)+ '.pkl', 'w')
		cPickle.dump(trainingResult, result)
		print game_result
		RaisedPlayer.foldThreshold += adjustingSize
	return optimalFactor

# For rough adjusting, adjusting size = 0.1, check the range from 0.1 to 0.3
theOptimalFactor =	trainingFactor(0, 0.05, 5, 8)
print theOptimalFactor

# For accurate adjusting, adjusting size is 0.01
theFinalOptimalFactor = trainingFactor(theOptimalFactor, 0.01, 1, 5)
print theFinalOptimalFactor