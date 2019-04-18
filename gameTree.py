class Node:

    def __init__(self, role, parent=None, SB_bet=10, BB_bet=20, card_known=[], card_count=2, win_rate=0, action="", raise_count=0, SB_raise=0, BB_raise=0, depth_count=0):
        self.role = role
        self.parent = parent
        self.SB_bet = SB_bet
        self.BB_bet = BB_bet
        self.card_known = card_known
        self.card_count = card_count
        self.win_rate = win_rate
        self.action = action
        self.children = []
        self.raise_count = raise_count
        self.description = self.role + " " + \
            self.action + " " + str(self.card_known)
        self.SB_raise = SB_raise
        self.BB_raise = BB_raise
        self.depth_count = depth_count
        self.weight = 1

    def add_child(self, *children):
        for child in children:
            self.children.append(child)

    def add_children(self, children):
        self.children.extend(children)

    def getChild(self, action):
        if action == "host":
            return self.children[0]
        else:
            for child in self.children:
                if child.action == action:
                    return child
    def add_depth(self):
        self.depth_count += 1

    def clear_depth(self):
        self.depth_count = 0

    def __str__(self):  # used for print node
        return ("role is " + self.role + " SB's bet is " + str(self.SB_bet) +
                " BB's bet is " + str(self.BB_bet) + " card known = " + str(self.card_known) +
                " action is " + self.action)


class Tree:
    count = 0
    pattern = ['H', 'D', 'C', 'S']
    number = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
    all_cards = []
    for p in pattern:
        for n in number:
            all_cards.append(p + n)
    raise_limit = 4
    my_role = ""

    def __init__(self, root=None):
        self.root = root
        self.steps = 0

    def set_my_role(self, role):
        self.my_role = role

    def generate_SB_children(self, node):
        fold_child = Node("BB", node, node.SB_bet, node.BB_bet, node.card_known, node.card_count, node.win_rate, "fold",
                          node.raise_count, node.SB_raise, node.BB_raise, node.depth_count + 1)
        call_child = Node("BB", node, node.BB_bet, node.BB_bet, node.card_known, node.card_count, node.win_rate, "call",
                          node.raise_count, node.SB_raise, node.BB_raise, node.depth_count + 1)
        raise_amount = 20 if node.card_count <= 5 else 40
        raise_child = Node("BB", node, node.BB_bet + raise_amount, node.BB_bet, node.card_known, node.card_count, node.win_rate, "raise",
                           node.raise_count + 1, node.SB_raise + 1, node.BB_raise, node.depth_count + 1)
        # condition for hosting, parent is not host node
        if node.parent is not None and node.parent.role not in ["SBHost", "BBHost"]:
            if node.card_count >= 7 and node.parent.parent is not None and node.parent.parent.role not in ["SBHost", "BBHost"]\
                    and node.action == "call":
                return []
            if node.card_count < 7:
                call_child = Node("SBHost", node, node.BB_bet, node.BB_bet, node.card_known, node.card_count, node.win_rate, "call",
                                  node.raise_count, node.SB_raise, node.BB_raise, node.depth_count + 1)
        if node.raise_count >= self.raise_limit or node.SB_raise >= self.raise_limit:
            return [fold_child, call_child]
        return [fold_child, call_child, raise_child]

    def generate_BB_children(self, node):
        fold_child = Node("SB", node, node.SB_bet, node.BB_bet, node.card_known, node.card_count, node.win_rate, "fold",
                          node.raise_count, node.SB_raise, node.BB_raise, node.depth_count + 1)
        call_child = Node("SB", node, node.SB_bet, node.SB_bet, node.card_known, node.card_count, node.win_rate, "call",
                          node.raise_count, node.SB_raise, node.BB_raise, node.depth_count + 1)
        raise_amount = 20 if node.card_count <= 5 else 40
        raise_child = Node("SB", node, node.SB_bet, node.SB_bet + raise_amount, node.card_known, node.card_count, node.win_rate, "raise",
                           node.raise_count + 1, node.SB_raise, node.BB_raise + 1, node.depth_count + 1)
        # condition for hosting, parent is not host node
        if node.parent is not None and node.parent.role not in ["SBHost", "BBHost"]:
            if node.card_count >= 7 and node.parent.parent is not None and node.parent.parent.role not in ["SBHost", "BBHost"] \
                    and node.action == "call":
                return []
            if node.card_count < 7:
                call_child = Node("BBHost", node, node.SB_bet, node.SB_bet, node.card_known, node.card_count, node.win_rate, "call",
                                  node.raise_count, node.SB_raise, node.BB_raise, node.depth_count + 1)
        if node.raise_count >= self.raise_limit or node.BB_raise >= self.raise_limit:
            return [fold_child, call_child]
        return [fold_child, call_child, raise_child]

    def generate_host_nodes(self, node):
        all_win_rates = self.generate_host_win_rate(node)
        children = []
        role = "SB" if node.role == "BBHost" else "BB"
        for win_rate in all_win_rates:
            children.append(Node(role, node, node.SB_bet, node.BB_bet, node.card_known, 5 if node.card_count == 2 else (
                node.card_count + 1), win_rate, "host", 0, node.SB_raise, node.BB_raise, node.depth_count + 1))
        return children

    def generate_host_win_rate(self, node):
        import random
        assert node.role == "BBHost" or node.role == "SBHost"
        oppo_actions = []
        current = node.parent
        while True:
            if current.role == "SB" or current.role == "BB":
                if current.role != self.my_role:
                    oppo_actions.append(current.action)
                if current.parent is None:
                    break
                else:
                    current = current.parent
            else:
                break
        default_win_rate = [0.25, 0.5, 0.75]
        influence_factor = 0.8 - (6 - node.card_count) * 0.12
        bias_factor = 1
        oppo_tendency = 1.2
        for item in oppo_actions:
            if item is "raise":
                bias_factor = bias_factor * oppo_tendency
            else:
                if bias_factor != 1:
                    oppo_tendency = 1 + (oppo_tendency - 1) * 0.7
        estimate_win_rate = []
        for item in default_win_rate:
            estimation = (node.win_rate / bias_factor *
                          influence_factor) + (1 - influence_factor) * item
            estimate_win_rate.append(estimation)
        return estimate_win_rate

    def generate_children(self, node):
        children = []
        # print node
        if node.role != "SBHost" and node.role != "BBHost":
            if node.action == "fold":
                return []
            elif node.role == "SB":
                new_children = self.generate_SB_children(node)
            else:
                assert node.role == "BB"
                new_children = self.generate_BB_children(node)
        else:
            assert node.role == "SBHost" or node.role == "BBHost"
            new_children = self.generate_host_nodes(node)
        node.add_children(new_children)
        children.extend(new_children)
        # print "chilrens"
        # for child in children: print child
        return new_children

    def build_tree(self):
        root = self.root
        children = self.generate_children(root)
        # leaves = []
        while len(children) != 0:
            # print len(children)
            current = children.pop(0)
            self.count += 1
            # print "this is current"
            # print current
            new_children = self.generate_children(current)
            children.extend(new_children)
            # print "this is new"
            # print new
            # for child in new_children:
            #     if child.depth_count < limit:
            #         children.append(child)
            #     else:
            #         child.clear_depth()
            #         leaves.append(child)
        # time.sleep(0.1)
        # print "Finish!"
        # return leaves

# import time
# start = time.time()
# node = Node("SB", None, 10, 20, ['H3', 'H2'])
# my_role = "BB"
# # print node
# tree = Tree()
# children = tree.build_tree(node, my_role, tree.generate_children(node), 11)
# end = time.time()
# print end - start
# start = time.time()
# children = tree.build_tree(node, my_role, children, 1, True)
# end = time.time()
# print end - start
# start = time.time()
# children = tree.build_tree(node, my_role, children, 1, True)
# end = time.time()
# print end - start
# from pptree import *
# print_tree(node, "children", "description")
# # import pickle
# with open('tree.pkl', 'wb') as output:
#     pickle.dump(node, output)
