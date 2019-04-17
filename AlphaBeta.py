from gameTree import Tree
class AlphaBeta:
    count_layer = 1
    limit_layer = 1
    factors = [1.5, 0.2, 0.5]  # win_rate, raise_rate, last_action

    # print utility value of root node (assuming it is max)
    # print names of all nodes visited during search
    def __init__(self, game_tree):
        self.game_tree = game_tree  # GameTree
        self.root = game_tree.root  # GameNode
        self.win_rate = 0
        self.opponent_num = 0
        return

    def set_limit(self, limit):
        self.limit_layer = limit


    def alpha_beta_search(self, node, win_rate, opponent_num):
        self.opponent_num = opponent_num
        node.win_rate = win_rate
        self.win_rate = win_rate
        infinity = float('inf')
        best_val = -infinity
        beta = infinity
        successors = self.getSuccessors(node)
        best_state = None
        for state in successors:
            # case for having host in successors
            # if "Host" in state.role:
            #     return self.max_value(state, best_val, beta)
            self.count_layer += 1
            value = self.min_value(state, best_val, beta)
            if value > best_val:
                best_val = value
                best_state = state
        #        print "AlphaBeta:  Utility Value of Root Node: = " + str(best_val)
        #        print "AlphaBeta:  Best State is: " + best_state.Name
        #        return best_state
        return best_state.action

    def max_value(self, node, alpha, beta):
#        print "AlphaBeta-->MAX: Visited Node :: " + node.Name
        if self.isTerminal(node):
            self.count_layer -= 1
            my_role = self.game_tree.my_role
            return self.getUtility(my_role, node, self.factors)
        infinity = float('inf')
        value = -infinity
        successors = self.getSuccessors(node)
        for state in successors:
            self.count_layer += 1
            if "Host" in state.role:
                tmp = 0
                for child in state.children:
                    tmp += self.max_value(child, alpha, beta)
                value = max(value, tmp / 3)
            else:
                value = max(value, self.min_value(state, alpha, beta))
            if value >= beta:
                self.count_layer -= 1
                return value
            alpha = max(alpha, value)
        self.count_layer -= 1
        return value

    def min_value(self, node, alpha, beta):
#        print "AlphaBeta-->MIN: Visited Node :: " + node.Name
        if self.isTerminal(node):
            self.count_layer -= 1
            my_role = self.game_tree.my_role
            return self.getUtility(my_role, node, self.factors)
        infinity = float('inf')
        value = infinity
        successors = self.getSuccessors(node)
        for state in successors:
            self.count_layer += 1
            if "Host" in state.role:
                tmp = 0
                for child in state.children:
                    tmp += self.min_value(child, alpha, beta)
                value = min(value, tmp / 3)
            else:
                value = min(value, self.max_value(state, alpha, beta))
            if value <= alpha:
                self.count_layer -= 1
                return value
            beta = min(beta, value)
        self.count_layer -= 1
        return value
    #                     #
    #   UTILITY METHODS   #
    #                     #

    # successor states in a game tree are the child nodes...
    def getSuccessors(self, node):
        assert node is not None
        children = []
        if "Host" not in node.role:
            for child in node.children:
                child.win_rate = self.win_rate
                children.append(child)
        else:
            #generate children for host
            estimation = self.game_tree.generate_host_win_rate(node)
            children = node.children
            # for child in children: print child
            # print estimation
            assert len(estimation) == len(children)
            for i in range(len(children)):
                children[i].win_rate = estimation[i]
#        return filter(lambda c: c.action != "fold", children)
        import random
        return random.sample(children, len(children))

    # return true if the node has NO children (successor states)
    # return false if the node has children (successor states)
    def isTerminal(self, node):
        assert node is not None
        return self.count_layer >= self.limit_layer or len(node.children) == 0
#        assert node is not None
#        return len(node.children) == 0


    def getUtility(self, role, node, factors):
        #assert node.role in ["SB", "BB"]
        #check whether player raise 5 times alr
        # factor1 = factors[0]
        raise_num = node.SB_raise if role == "BB" else node.BB_raise
        raise_rate = -1 * (raise_num / self.opponent_num)
        #check the last 5 actions
        #actions = get_actions(node, node.role, 5)
        if raise_num == 4:
            last_action = -0.5
        else:
            last_action = -1 if node.action == "raise" else 0.2
        #the total money on table
        if role == "SB":
            my_money, op_money = node.SB_bet, node.BB_bet
        else:
            my_money, op_money = node.BB_bet, node.SB_bet
        win_rate = node.win_rate
        win_rate = factors[0] * win_rate + factors[1] * raise_rate + factors[2] * last_action
        if node.action == "fold":
            win_rate = 0 if node.role != role else 1
            # last_action = 0
        expectation = win_rate * (my_money + op_money) - my_money
        # result = sum(map(lambda x, y: x * y, factors, [last_action, expectation]))
        # return result
        return expectation