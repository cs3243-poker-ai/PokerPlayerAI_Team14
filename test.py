from gameTree import Node, Tree
import msgpack
with open('rate_2c.msgpack') as data_file:
    rate = msgpack.unpack(data_file)

root = Node("SB", None, 10, 20, ["S2", "H3"], 2, rate.get("23d"))
tree = Tree(root)
tree.set_my_role("SB")
print "building"
tree.build_tree()
print "pruning"
from AlphaBeta import AlphaBeta
prun = AlphaBeta(tree)
result = prun.alpha_beta_search(root, rate.get("AAd"))
# print prun.getUtility("SB", root.children[0], prun.factors)
# print prun.getUtility("SB", root.children[1], prun.factors)
# print prun.getUtility("SB", root.children[2], prun.factors)
print result
